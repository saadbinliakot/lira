exec(open('00_common.py').read())
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch

POS = {'L_x': (-2.5, 1.6), 'Gamma': (-0.85, 1.6), 'T_in': (0.85, 1.6), 'H_r': (2.5, 1.6),
       'F_r': (0, -1.1), 'F_lag': (3.0, -1.1)}
LBL = {'L_x': '$\\log L_X$', 'Gamma': '$\\Gamma$', 'T_in': '$\\log T_{in}$', 'H_r': '$HR$',
       'F_r': '$\\log F_R$', 'F_lag': '$\\log F_R(t\\!-\\!1)$'}
FRAC = {'L_x': 0.36, 'Gamma': 0.58, 'T_in': 0.74, 'H_r': 0.36}
OFF  = {'L_x': 0.30, 'Gamma': 0.26, 'T_in': -0.28, 'H_r': -0.30}
SPEC = {'Hard State  ($G_1$)': (HARD, {'L_x': 0.70, 'Gamma': -0.30, 'H_r': -0.40}, 'T_in'),
        'Soft State  ($G_2$)': (SOFT, {'L_x': 0.18, 'Gamma': 0.20, 'T_in': -0.40}, 'H_r')}

fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))
for ax, (ttl, (col, edges, absent)) in zip(axes, SPEC.items()):
    ax.set_xlim(-3.6, 4.3); ax.set_ylim(-2.2, 2.5); ax.axis('off')
    for v, w in edges.items():
        ec = GRN if w > 0 else '#C0392B'
        ax.add_patch(FancyArrowPatch(POS[v], POS['F_r'], arrowstyle='-|>', mutation_scale=16,
            lw=1.0+2.6*abs(w), color=ec, alpha=.9, shrinkA=24, shrinkB=26))
        x0, y0 = POS[v]; x1, y1 = POS['F_r']; f = FRAC[v]
        mx, my = x0+f*(x1-x0), y0+f*(y1-y0)
        dx, dy = x1-x0, y1-y0; L = np.hypot(dx, dy); px, py = -dy/L, dx/L
        off = OFF[v]
        ax.text(mx+px*off, my+py*off, f'{w:+.2f}', fontsize=9, color=ec, fontweight='bold',
                ha='center', va='center', path_effects=[pe.withStroke(linewidth=3, foreground='white')])
    ax.add_patch(FancyArrowPatch(POS['F_lag'], POS['F_r'], arrowstyle='-|>', mutation_scale=16,
        lw=2.3, color=PUR, alpha=.9, shrinkA=36, shrinkB=26))
    ax.text(1.62, -0.80, '$\\phi=+0.50$', fontsize=9, color=PUR, fontweight='bold', ha='center',
            path_effects=[pe.withStroke(linewidth=3, foreground='white')])
    for v, (x, y) in POS.items():
        if v == absent:
            ax.add_patch(Circle((x, y), 0.44, facecolor='#F0F0F2', edgecolor='#B8B8C0', lw=1.4, ls='--', zorder=5))
            ax.text(x, y, LBL[v], ha='center', va='center', fontsize=8.8, color='#9A9AA4', zorder=6)
            ax.text(x, y-0.70, 'isolated', ha='center', fontsize=7.8, color='#9A9AA4', style='italic')
        elif v == 'F_r':
            ax.add_patch(Circle((x, y), 0.48, facecolor=col, edgecolor='none', alpha=.93, zorder=5))
            ax.text(x, y, LBL[v], ha='center', va='center', fontsize=9.5, color='white', fontweight='bold', zorder=6)
        elif v == 'F_lag':
            ax.add_patch(FancyBboxPatch((x-0.66, y-0.27), 1.32, 0.54, boxstyle='round,pad=0.06',
                facecolor='#EDE4F7', edgecolor=PUR, lw=1.2, zorder=5))
            ax.text(x, y, LBL[v], ha='center', va='center', fontsize=8.2, color=PUR, zorder=6)
        else:
            ax.add_patch(Circle((x, y), 0.44, facecolor='white', edgecolor=col, lw=2.0, zorder=5))
            ax.text(x, y, LBL[v], ha='center', va='center', fontsize=8.8, color=NEU, zorder=6)
    ax.set_title(ttl, fontsize=11.5, fontweight='bold', color=col, pad=2)

fig.text(0.5, 0.02, 'Green = positive coefficient   \u00b7   Red = negative   \u00b7   edge width \u221d |coefficient|',
          ha='center', fontsize=8.6, color=NEU)
fig.suptitle('Hypothesised regime-specific causal structures (ground truth)',
             y=1.00, fontsize=12, fontweight='bold')
plt.subplots_adjust(bottom=0.08, top=0.86)
save(fig, 'fig02_ground_truth_dags')
