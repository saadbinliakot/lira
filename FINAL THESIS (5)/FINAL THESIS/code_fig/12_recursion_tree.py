exec(open('00_common.py').read())
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

root = [n for n in R['nodes'] if n['path'] == 'root'][0]
L = [n for n in R['nodes'] if n['path'] == 'rootL'][0]; Rt = [n for n in R['nodes'] if n['path'] == 'rootR'][0]

fig, ax = plt.subplots(figsize=(11, 6.8)); ax.axis('off'); ax.set_xlim(0, 10); ax.set_ylim(0, 8.2)

def box(x, y, w, h, txt, fc, ec, fs=8.6):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle='round,pad=.1', fc=fc, ec=ec, lw=1.6, zorder=3))
    ax.text(x, y, txt, ha='center', va='center', fontsize=fs, zorder=4)

box(5, 7.2, 5.0, 1.2, f"ROOT   $n$ = {root['n']}\n"
    f"GATE 1  $F_{{lag}}$ = {root['F']:.0f},  $p<10^{{-16}}$  \u2713\n"
    f"GATE 2  $BIC_1$={root['BIC1']:.0f}  >  $BIC_2$={root['BIC2']:.0f}  \u2713", '#FFF6E8', ACC)
ax.text(5, 6.28, f"both gates passed  \u2192  SPLIT at $t$ = {root['tau_global']}", ha='center', fontsize=9.5,
        color=GRN, fontweight='bold')
for xx, nd, c, nm, gi in [(2.6, L, HARD, 'HARD', 0), (7.4, Rt, SOFT, 'SOFT', 1)]:
    ax.add_patch(FancyArrowPatch((5, 6.58), (xx, 4.85), arrowstyle='-|>', mutation_scale=16, lw=1.8, color=GRN, zorder=2))
    box(xx, 4.25, 4.3, 1.45, f"{nm} LEAF   $n$ = {nd['n']}\nrows {nd['lo']}\u2013{nd['hi']}\n"
        f"GATE 1  $F_{{lag}}$={nd['F']:.2f},  $p$={nd['p']:.3f}  \u2713\n"
        f"GATE 2  $BIC_1$={nd['BIC1']:.0f}  <  $BIC_2$={nd['BIC2']:.0f}  \u2717",
        '#FFF0EF' if c == HARD else '#EEF5FC', c)
    ax.text(xx, 3.18, 'Chow passes, BIC rejects  \u2192  STOP', ha='center', fontsize=8.8, color=HARD, fontweight='bold')
    ax.add_patch(FancyArrowPatch((xx, 2.92), (xx, 2.05), arrowstyle='-|>', mutation_scale=16, lw=1.8, color=c, zorder=2))
    box(xx, 1.50, 4.3, 1.0, f"DYNOTEARS  \u2192  $(W^{{({gi})}},\\, A^{{({gi})}})$\nregime-specific causal graph", 'white', c, fs=8.8)
ax.text(5, .40, '$K = 2$ regimes discovered \u2014 not specified in advance', ha='center', fontsize=10.5,
        fontweight='bold', color=NEU)
ax.text(5, -.05, 'At both leaves the Chow test alone would have over-split ($p<0.05$); the BIC gate is what stops it.',
        ha='center', fontsize=8.6, color=HARD, style='italic')
ax.set_title('Realised recursion tree on the synthetic series', fontsize=12, fontweight='bold', pad=4)
save(fig, 'fig12_recursion_tree')
