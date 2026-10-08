"""
LICP — Latent Environment Discovery via Invariance-Based Causal Partitioning
============================================================================
Fixed: search-first, BIC-validate approach.
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import adjusted_rand_score
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


# DATA GENERATOR 

def generate_accretion_disk_data(n_per_regime=400, noise_std=0.15, seed=42):
    rng = np.random.default_rng(seed)

    L_X1   = rng.normal(37.5, 0.5,  n_per_regime)
    Gamma1 = rng.normal(1.6,  0.15, n_per_regime)
    T_in1  = rng.normal(0.3,  0.05, n_per_regime)
    HR1    = rng.normal(0.75, 0.08, n_per_regime)
    F_R1   = 0.70*L_X1 - 0.30*Gamma1 + 0.10*T_in1 - 0.40*HR1 + rng.normal(0, noise_std, n_per_regime)

    L_X2   = rng.normal(38.2, 0.4,  n_per_regime)
    Gamma2 = rng.normal(2.5,  0.2,  n_per_regime)
    T_in2  = rng.normal(1.1,  0.1,  n_per_regime)
    HR2    = rng.normal(0.2,  0.06, n_per_regime)
    F_R2   = 0.18*L_X2 + 0.20*Gamma2 - 0.40*T_in2 + 0.10*HR2 + rng.normal(0, noise_std, n_per_regime)

    df = pd.DataFrame({
        'L_X': np.concatenate([L_X1, L_X2]),
        'Gamma': np.concatenate([Gamma1, Gamma2]),
        'T_in': np.concatenate([T_in1, T_in2]),
        'HR': np.concatenate([HR1, HR2]),
        'F_R': np.concatenate([F_R1, F_R2]),
        'true_regime': [0]*n_per_regime + [1]*n_per_regime
    }).sample(frac=1, random_state=seed).reset_index(drop=True)

    print(f"[DATA] n={len(df)} observations | 2 hidden regimes")
    print(f"       Regime 0 beta = [ 0.70, -0.30,  0.10, -0.40]")
    print(f"       Regime 1 beta = [ 0.18,  0.20, -0.40,  0.10]")
    return df


# OLS

def fit_ols(X, y):
    Xd = np.column_stack([np.ones(len(X)), X])
    beta, _, _, _ = np.linalg.lstsq(Xd, y, rcond=None)
    resid = y - Xd @ beta
    rss = float(resid @ resid)
    return beta, resid, rss


# ── CHOW TEST ─────────────────────────────────────────────────────────────────

def chow_f(X, y, idxA, idxB):
    p = X.shape[1] + 1
    n = len(y)
    if len(idxA) <= p or len(idxB) <= p:
        return 0.0, 1.0
    _, _, rss_g = fit_ols(X, y)
    _, _, rss_A = fit_ols(X[idxA], y[idxA])
    _, _, rss_B = fit_ols(X[idxB], y[idxB])
    df1 = p
    df2 = n - 2*p
    if df2 <= 0: return 0.0, 1.0
    num = (rss_g - (rss_A + rss_B)) / df1
    den = (rss_A + rss_B) / df2
    if den < 1e-12: return 0.0, 1.0
    F = max(0.0, num / den)
    return float(F), float(1 - stats.f.cdf(F, df1, df2))


# ── BIC ACCEPTANCE ────────────────────────────────────────────────────────────

def bic_accepts_split(X, y, idx_all, idxA, idxB):
    p = X.shape[1] + 1
    n = len(idx_all)
    nA, nB = len(idxA), len(idxB)
    if nA <= p or nB <= p: return False
    eps = 1e-10
    _, _, rss_all = fit_ols(X[idx_all], y[idx_all])
    _, _, rss_A   = fit_ols(X[idxA],   y[idxA])
    _, _, rss_B   = fit_ols(X[idxB],   y[idxB])
    bic_parent = n  * np.log(rss_all/n  + eps) + p * np.log(n)
    bic_split  = (nA * np.log(rss_A/nA + eps)
                + nB * np.log(rss_B/nB + eps)
                + 2*p * np.log(n))
    return bool(bic_split < bic_parent)


# ── SPLIT SEARCH ──────────────────────────────────────────────────────────────

def search_best_split(X, y, indices, n_min, feature_names):
    best_F, best_j, best_tau = -np.inf, None, None
    best_idxA, best_idxB = None, None
    Xn, yn = X[indices], y[indices]

    for j in range(Xn.shape[1]):
        vals = np.sort(np.unique(Xn[:, j]))
        thresholds = (vals[:-1] + vals[1:]) / 2.0
        for tau in thresholds:
            idxA = indices[Xn[:, j] <= tau]
            idxB = indices[Xn[:, j] >  tau]
            if len(idxA) < n_min or len(idxB) < n_min:
                continue
            F, _ = chow_f(X, y, idxA, idxB)
            if F > best_F:
                best_F, best_j, best_tau = F, j, tau
                best_idxA, best_idxB = idxA, idxB

    return best_j, best_tau, best_F, best_idxA, best_idxB


# ── TREE NODE ─────────────────────────────────────────────────────────────────

class LICPNode:
    def __init__(self, indices, depth, beta, rss):
        self.indices = indices
        self.depth = depth
        self.beta = beta
        self.rss = rss
        self.is_leaf = True
        self.split_feature = None
        self.split_tau = None
        self.feature_name = None
        self.left = None
        self.right = None
        self.regime_id = None


# ── LICP CORE ─────────────────────────────────────────────────────────────────

class LICP:
    def __init__(self, n_min=50, d_max=4, verbose=True):
        self.n_min = n_min
        self.d_max = d_max
        self.verbose = verbose
        self.root = None
        self.leaves = []
        self.X = self.y = self.feature_names = None

    def fit(self, X, y, feature_names=None):
        self.X = X
        self.y = y
        self.feature_names = feature_names or [f'X{j}' for j in range(X.shape[1])]

        self._log("\n" + "="*60)
        self._log("LICP — Latent Environment Discovery")
        self._log(f"n={len(y)} | p={X.shape[1]} | n_min={self.n_min} | d_max={self.d_max}")
        self._log("="*60)

        beta_g, _, rss_g = fit_ols(X, y)
        self._log(f"\n[STEP 1] Global OLS fitted")
        self._log(f"  beta_global = {np.round(beta_g[1:], 3)}")
        self._log(f"  RSS_global  = {rss_g:.4f}")
        self._log(f"\n[STEP 2] Recursive splitting (search-first, BIC-validate)")

        self.root = LICPNode(np.arange(len(y)), 0, beta_g, rss_g)
        self._recurse(self.root)

        self.leaves = []
        self._collect_leaves(self.root)
        for i, leaf in enumerate(self.leaves):
            leaf.regime_id = i

        self._log(f"\n{'='*60}")
        self._log(f"[RESULT] K = {len(self.leaves)} regime(s) discovered")
        for leaf in self.leaves:
            self._log(f"  Regime {leaf.regime_id}: n={len(leaf.indices)} | "
                      f"beta={np.round(leaf.beta[1:], 3)}")
        return self

    def predict_regime(self):
        labels = np.full(len(self.y), -1, dtype=int)
        for leaf in self.leaves:
            labels[leaf.indices] = leaf.regime_id
        return labels

    def get_regime_data(self, k):
        leaf = self.leaves[k]
        return self.X[leaf.indices], self.y[leaf.indices]

    def _log(self, msg):
        if self.verbose: print(msg)

    def _recurse(self, node):
        n, depth = len(node.indices), node.depth
        pad = "  " * depth

        if depth >= self.d_max:
            self._log(f"{pad}[LEAF] depth={depth} reached")
            return
        if n < 2 * self.n_min:
            self._log(f"{pad}[LEAF] n={n} < 2*n_min")
            return

        feat, tau, F_best, idxA, idxB = search_best_split(
            self.X, self.y, node.indices, self.n_min, self.feature_names)

        if feat is None:
            self._log(f"{pad}[LEAF] no valid split found")
            return

        fname = self.feature_names[feat]
        if not bic_accepts_split(self.X, self.y, node.indices, idxA, idxB):
            self._log(f"{pad}[LEAF] n={n} | best split {fname}<={tau:.3f} "
                      f"F={F_best:.2f} rejected by BIC")
            return

        self._log(f"{pad}[SPLIT] depth={depth} | n={n} | "
                  f"{fname} <= {tau:.4f} | nA={len(idxA)} nB={len(idxB)} | F={F_best:.2f}")

        node.is_leaf = False
        node.split_feature = feat
        node.split_tau = tau
        node.feature_name = fname

        beta_A, _, rss_A = fit_ols(self.X[idxA], self.y[idxA])
        beta_B, _, rss_B = fit_ols(self.X[idxB], self.y[idxB])

        node.left  = LICPNode(idxA, depth+1, beta_A, rss_A)
        node.right = LICPNode(idxB, depth+1, beta_B, rss_B)

        self._recurse(node.left)
        self._recurse(node.right)

    def _collect_leaves(self, node):
        if node is None: return
        if node.is_leaf:
            self.leaves.append(node)
        else:
            self._collect_leaves(node.left)
            self._collect_leaves(node.right)


# ── CAUSAL GRAPHS ─────────────────────────────────────────────────────────────

def run_causal_graphs(model, all_features, alpha=0.05):
    try:
        from causallearn.search.ConstraintBased.PC import pc
        from causallearn.utils.cit import fisherz
    except ImportError:
        print("\n[GRAPH] pip install causal-learn"); return

    print(f"\n{'='*60}")
    print("[STAGE 2] Causal graph per regime (PC algorithm)")
    print(f"{'='*60}")

    for leaf in model.leaves:
        k = leaf.regime_id
        Xr, yr = model.get_regime_data(k)
        data_r = np.column_stack([Xr, yr])
        print(f"\n  Regime {k} | n={len(data_r)}")
        print(f"  beta = {np.round(leaf.beta[1:], 3)}")
        if len(data_r) < 30:
            print(f"  too small — skipping"); continue
        try:
            cg = pc(data_r, alpha=alpha, indep_test=fisherz, verbose=False)
            G = cg.G
            print(f"  Edges:")
            found = False
            for i in range(len(all_features)):
                for j in range(len(all_features)):
                    if i == j: continue
                    if G.graph[i,j]==-1 and G.graph[j,i]==1:
                        print(f"    {all_features[i]} -> {all_features[j]}"); found=True
                    elif G.graph[i,j]==-1 and G.graph[j,i]==-1 and i<j:
                        print(f"    {all_features[i]} -- {all_features[j]}  (undirected)"); found=True
            if not found: print(f"    (none at alpha={alpha})")
        except Exception as e:
            print(f"  PC error: {e}")


# ── EVALUATION ────────────────────────────────────────────────────────────────

def evaluate(true_labels, pred_labels, model):
    ari = adjusted_rand_score(true_labels, pred_labels)
    print(f"\n{'='*60}")
    print(f"[EVALUATION]")
    print(f"  Discovered K = {len(model.leaves)}  |  True K = {len(np.unique(true_labels))}")
    print(f"  ARI = {ari:.4f}  (1.0=perfect | 0.0=random)")
    print(f"\n  Discovered betas:")
    for leaf in model.leaves:
        print(f"    Regime {leaf.regime_id}: {np.round(leaf.beta[1:], 3)}")
    print(f"\n  True betas:")
    print(f"    Regime 0: [ 0.70 -0.30  0.10 -0.40]")
    print(f"    Regime 1: [ 0.18  0.20 -0.40  0.10]")
    return ari


# ── PLOT ──────────────────────────────────────────────────────────────────────

def plot_results(df, pred_labels, feature_names, model):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("LICP — Accretion Disk Latent Regime Discovery",
                 fontsize=13, fontweight='bold')

    colors_t = ['#2E9E6B', '#7C6AF7', '#E07B39']
    colors_p = ['#F59E0B', '#2563EB', '#DC2626', '#059669']
    xf, yf = 'Gamma', 'L_X'

    ax = axes[0]
    for r in sorted(df['true_regime'].unique()):
        m = df['true_regime'] == r
        ax.scatter(df.loc[m, xf], df.loc[m, yf],
                   c=colors_t[r], alpha=0.45, s=14, label=f'True {r}')
    ax.set_xlabel(xf); ax.set_ylabel(yf)
    ax.set_title('Ground Truth (hidden from LICP)')
    ax.legend(fontsize=9)

    ax = axes[1]
    for r in sorted(np.unique(pred_labels)):
        if r < 0: continue
        m = pred_labels == r
        ax.scatter(df.loc[m, xf], df.loc[m, yf],
                   c=colors_p[r % len(colors_p)], alpha=0.45, s=14,
                   label=f'Discovered {r}')

    def draw_splits(node):
        if node is None or node.is_leaf: return
        if node.feature_name == xf:
            ax.axvline(node.split_tau, color='k', ls='--', lw=1.5, alpha=0.8)
        elif node.feature_name == yf:
            ax.axhline(node.split_tau, color='k', ls='--', lw=1.5, alpha=0.8)
        draw_splits(node.left); draw_splits(node.right)

    draw_splits(model.root)
    ax.set_xlabel(xf); ax.set_ylabel(yf)
    ax.set_title(f'LICP Discovered (K={len(model.leaves)})')
    ax.legend(fontsize=9)

    plt.tight_layout()
    out = r'E:\Study\BRACU\Thesis\licp_results.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    print(f"\n[PLOT] Saved: licp_results.png")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    df = generate_accretion_disk_data(n_per_regime=400, noise_std=0.15)
    feature_cols = ['L_X', 'Gamma', 'T_in', 'HR']
    X = df[feature_cols].values
    y = df['F_R'].values
    true_labels = df['true_regime'].values

    model = LICP(n_min=50, d_max=4, verbose=True)
    model.fit(X, y, feature_names=feature_cols)

    pred_labels = model.predict_regime()
    ari = evaluate(true_labels, pred_labels, model)

    run_causal_graphs(model, feature_cols + ['F_R'], alpha=0.05)
    plot_results(df, pred_labels, feature_cols, model)

    print(f"\n{'='*60}")
    print(f"DONE  |  ARI={ari:.4f}  |  K={len(model.leaves)}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()