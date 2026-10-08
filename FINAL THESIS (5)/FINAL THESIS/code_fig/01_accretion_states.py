exec(open('00_common.py').read())
from matplotlib.patches import Ellipse, Circle

fig, axes = plt.subplots(1, 2, figsize=(11, 4.9))
for ax, st in zip(axes, ['hard', 'soft']):
    ax.set_xlim(-5, 5); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.axis('off')
    c = HARD if st == 'hard' else SOFT
    if st == 'hard':
        for r, a in [(2.6, .10), (2.2, .14), (1.8, .18)]:
            ax.add_patch(Ellipse((0, 0), r*2, r*0.62, facecolor=ACC, alpha=a, edgecolor='none'))
        ax.add_patch(Ellipse((0, 0), 3.0, 0.95, facecolor=HARD, alpha=.30, edgecolor='none'))
        ax.annotate('', xy=(0, 2.7), xytext=(0, .4), arrowprops=dict(arrowstyle='-|>', lw=3.4, color=HARD, alpha=.92))
        ax.annotate('', xy=(0, -2.7), xytext=(0, -.4), arrowprops=dict(arrowstyle='-|>', lw=3.4, color=HARD, alpha=.92))
        ax.text(1.0, 2.25, 'steady radio jet', color=HARD, fontsize=9.5, fontweight='bold')
        ax.text(-4.6, -2.5, 'disk truncated \u00b7 hot corona\n\u0393\u22481.4\u20131.7 \u00b7 HR high \u00b7 $T_{in}$ low', fontsize=8.6, color=NEU)
        ttl = 'Hard State  (jet-dominated)'
    else:
        for r, a in [(4.2, .12), (3.4, .18), (2.6, .26), (1.8, .36)]:
            ax.add_patch(Ellipse((0, 0), r*2, r*0.52, facecolor=SOFT, alpha=a, edgecolor='none'))
        ax.add_patch(Ellipse((0, 0), 1.5, 0.42, facecolor='#BFE3FF', alpha=.95, edgecolor='none'))
        ax.text(1.2, 2.15, 'jet quenched', color=NEU, fontsize=9.5, fontweight='bold', style='italic')
        ax.plot([0, 0], [.45, 1.7], color=NEU, lw=2.2, ls=':', alpha=.55)
        ax.plot([-.32, .32], [1.45, 1.95], color=NEU, lw=2.0)
        ax.plot([-.32, .32], [1.95, 1.45], color=NEU, lw=2.0)
        ax.text(-4.6, -2.5, 'disk reaches ISCO\n\u0393\u22482.0\u20132.5 \u00b7 HR low \u00b7 $T_{in}$ high', fontsize=8.6, color=NEU)
        ttl = 'Soft State  (disk-dominated)'
    ax.add_patch(Circle((0, 0), 0.42, facecolor='black', zorder=6))
    ax.add_patch(Circle((0, 0), 0.50, facecolor='none', edgecolor=ACC, lw=1.5, alpha=.85, zorder=6))
    ax.set_title(ttl, fontsize=11.5, fontweight='bold', color=c, pad=8)

fig.suptitle('Accretion geometry of the two spectral states', y=0.98, fontsize=12, fontweight='bold')
plt.subplots_adjust(top=0.80, bottom=0.05)
save(fig, 'fig01_accretion_states')
