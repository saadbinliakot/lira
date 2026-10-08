exec(open('00_common.py').read())

X, Y = build_design(df2); n = len(Y)
grid = np.arange(2*Q, n-2*Q, 5)
F = np.array([chowF(X, Y, int(t)) for t in grid])
TR = 5000
TAU_DISCOVERED = int(R['nodes'][0]['tau_global'])
F_DISCOVERED = chowF(X, Y, TAU_DISCOVERED)

fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={'width_ratios': [2, 1]})
a1.plot(grid, F, lw=1.0, color=PUR); a1.fill_between(grid, 0, F, color=PUR, alpha=.16)
a1.axvline(TR, color='black', ls='--', lw=1.3, label=f'true boundary ($t$={TR})')
a1.plot(TAU_DISCOVERED, F_DISCOVERED, 'o', ms=8, color=GRN, zorder=5,
        label=f'$\\tau^*$={TAU_DISCOVERED}  ($F$={F_DISCOVERED:.0f})')
a1.set_xlabel('candidate split index $\\tau$'); a1.set_ylabel('lagged Chow $F_{lag}(\\tau)$')
a1.set_title('Full sweep over candidate splits', fontsize=11); a1.legend(fontsize=8.5)

w = 260; m = (grid > TR-w) & (grid < TR+w)
a2.plot(grid[m], F[m], lw=1.5, color=PUR, marker='o', ms=2.5)
a2.axvline(TR, color='black', ls='--', lw=1.3)
a2.set_xlabel('$\\tau$'); a2.set_title(f'Detail near boundary (\u00b1{w})', fontsize=11)
a2.set_ylabel('$F_{lag}$')

fig.suptitle('Lagged Chow $F$-statistic across candidate split points', y=1.02, fontsize=12, fontweight='bold')
plt.tight_layout()
save(fig, 'fig04_chow_F_curve')
