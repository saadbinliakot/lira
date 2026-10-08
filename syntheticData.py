import numpy as np
import pandas as pd

def generate_data(n_per_regime=5000, noise_std=0.10, seed=42):
    """
    Two-regime synthetic accretion data.
    - L_x, Gamma, T_in, H_r: independent mean-reverting AR(1) series (phi = 0.90)
    - F_r: mean-reverting AR(1) (phi = 0.50) plus the CENTRED predictors
      (X - mu), so E[F_r] = mu_F in both regimes, for any beta.
    - Only the betas differ between regimes.
    """
    rng = np.random.default_rng(seed)

    mu = {'L_x': 37.5, 'Gamma': 1.6, 'T_in': 0.3, 'H_r': 0.75, 'F_r': 28.0}
    phi_x = 0.90     # persistence of the four predictors
    phi_f = 0.50     # persistence of F_r

    def make_regime(n, beta):
        L = np.zeros(n); G = np.zeros(n); T = np.zeros(n)
        H = np.zeros(n); F = np.zeros(n)
        L[0], G[0], T[0], H[0], F[0] = (mu['L_x'], mu['Gamma'], mu['T_in'],
                                        mu['H_r'], mu['F_r'])
        for t in range(1, n):
            L[t] = mu['L_x']   + phi_x*(L[t-1] - mu['L_x'])   + rng.normal(0, noise_std)
            G[t] = mu['Gamma'] + phi_x*(G[t-1] - mu['Gamma']) + rng.normal(0, noise_std)
            T[t] = mu['T_in']  + phi_x*(T[t-1] - mu['T_in'])  + rng.normal(0, noise_std)
            H[t] = mu['H_r']   + phi_x*(H[t-1] - mu['H_r'])   + rng.normal(0, noise_std)
            F[t] = (mu['F_r'] + phi_f*(F[t-1] - mu['F_r'])
                    + beta['L_x']  * (L[t] - mu['L_x'])
                    + beta['Gamma']* (G[t] - mu['Gamma'])
                    + beta['T_in'] * (T[t] - mu['T_in'])
                    + beta['H_r']  * (H[t] - mu['H_r'])
                    + rng.normal(0, noise_std))
        return pd.DataFrame({'L_x': L, 'Gamma': G, 'T_in': T, 'H_r': H, 'F_r': F})

    beta_hard = {'L_x': 0.70, 'Gamma': -0.30, 'T_in': 0.00, 'H_r': -0.40}
    beta_soft = {'L_x': 0.18, 'Gamma':  0.20, 'T_in': -0.40, 'H_r': 0.00}

    hard = make_regime(n_per_regime, beta_hard); hard['true_regime'] = 0
    soft = make_regime(n_per_regime, beta_soft); soft['true_regime'] = 1

    df = pd.concat([hard, soft], ignore_index=True)
    df['t'] = np.arange(len(df))
    return df

if __name__ == "__main__":
    df = generate_data()
    df.to_csv('regime_dataset_v2.csv', index=False)
    print("saved", df.shape)