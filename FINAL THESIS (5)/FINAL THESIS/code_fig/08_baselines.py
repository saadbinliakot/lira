exec(open('00_common.py').read())

names = ['LIRA\n(this work)\n$K$ not supplied', 'KMeans\nraw features\n($K{=}2$ given)',
         'KMeans\nstandardised\n($K{=}2$ given)', 'KMeans\nrolling means\n($K{=}2$ given)',
         'KMeans\nrolling $F_R$ std\n($K{=}2$ given)']
vals = [0.9984, 0.0011, 0.0009, 0.0112, 0.5867]
cols = [GRN, '#9AA0AA', '#9AA0AA', '#9AA0AA', ACC]

fig, ax = plt.subplots(figsize=(9.4, 4.9))
b = ax.bar(names, vals, .58, color=cols, alpha=.93, edgecolor='none')
for r, v in zip(b, vals):
    ax.text(r.get_x()+r.get_width()/2, v+.022, f'{v:.4f}', ha='center', fontsize=10, fontweight='bold',
            color=GRN if v > .9 else (ACC if v > .3 else NEU))
ax.set_ylabel('Adjusted Rand Index'); ax.set_ylim(0, 1.12)
ax.axhline(1.0, color=NEU, ls=':', lw=1, alpha=.6)
ax.text(4.4, 1.02, 'perfect', fontsize=8, color=NEU, ha='right')
ax.set_title('Regime recovery: LIRA versus $k$-means clustering baselines',
             fontsize=12, fontweight='bold', pad=12)
ax.text(.5, -.30, 'Means are equalised across regimes by construction, so only causal-mechanism change distinguishes them.\n'
        '$k$-means is given the true number of regimes ($K{=}2$) directly; LIRA determines $K$ on its own.',
        transform=ax.transAxes, ha='center', fontsize=8.4, color=NEU)
plt.subplots_adjust(bottom=.28)
save(fig, 'fig08_baselines')
