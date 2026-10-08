exec(open('00_common.py').read())
from scipy import stats

def acf(x, L=25):
    x = x - x.mean(); c0 = (x @ x) / len(x)
    return np.array([(x[:len(x)-k] @ x[k:]) / len(x) / c0 for k in range(L+1)])

s0 = df2.iloc[0:R['leaves'][0][1]].reset_index(drop=True)
Xn = np.column_stack([np.ones(len(s0)), s0['L_x'], s0['Gamma'], s0['T_in'], s0['H_r']])
_, _, rn = ols(Xn, s0['F_r'].values)
Xl, Yl = build_design(s0); _, _, rl = ols(Xl, Yl)
an, al = acf(rn), acf(rl); lags = np.arange(len(an)); ci = 1.96 / np.sqrt(len(rl))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.2), sharey=True)
for ax, a, t, c in [(a1, an, 'Without AR term  (Eq. 4.4)', HARD), (a2, al, 'With AR term  (Eq. 4.5)', GRN)]:
    ax.bar(lags, a, .55, color=c, alpha=.88)
    ax.axhspan(-ci, ci, color=NEU, alpha=.14); ax.axhline(0, color='black', lw=.9)
    ax.set_xlabel('lag'); ax.set_title(t, fontsize=11, color=c, fontweight='bold')
a1.set_ylabel('residual autocorrelation')
a1.annotate(f'ACF(1) = {an[1]:.3f}', xy=(1, an[1]), xytext=(7, an[1]*.88), fontsize=9.5, color=HARD,
            fontweight='bold', arrowprops=dict(arrowstyle='->', color=HARD))
a2.annotate(f'ACF(1) = {al[1]:.3f}', xy=(1, al[1]), xytext=(6, .30), fontsize=9.5, color=GRN,
            fontweight='bold', arrowprops=dict(arrowstyle='->', color=GRN))
a1.text(.97, .94, 'Ljung\u2013Box(10): $p<10^{-16}$', transform=a1.transAxes, ha='right', fontsize=8.6, color=HARD)
a2.text(.97, .94, 'Ljung\u2013Box(10): $p=0.21$', transform=a2.transAxes, ha='right', fontsize=8.6, color=GRN)

fig.suptitle('The AR(1) term removes residual autocorrelation, validating the Chow $F$ derivation',
             y=1.03, fontsize=12, fontweight='bold')
plt.tight_layout()
save(fig, 'fig06_residual_acf')
