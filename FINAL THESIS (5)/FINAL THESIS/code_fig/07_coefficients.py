exec(open('00_common.py').read())

VARS = ['L_x', 'Gamma', 'T_in', 'H_r', 'phi']
VL = ['$L_X$', '$\\Gamma$', '$T_{in}$', '$HR$', '$\\phi$']
TRUE = {'0': [0.70, -0.30, 0.00, -0.40, 0.50], '1': [0.18, 0.20, -0.40, 0.00, 0.50]}

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
for ax, rg, col, nm in [(axes[0], '0', HARD, 'Hard State'), (axes[1], '1', SOFT, 'Soft State')]:
    rec = [R['per'][rg][v] for v in VARS]; tru = TRUE[rg]
    x = np.arange(len(VARS)); w = .37
    ax.bar(x-w/2, tru, w, label='true', color=NEU, alpha=.55, edgecolor='none')
    ax.bar(x+w/2, rec, w, label='LIRA recovered', color=col, alpha=.92, edgecolor='none')
    ax.axhline(0, color='black', lw=.9); ax.set_xticks(x); ax.set_xticklabels(VL)
    ax.set_title(f'{nm}  (regime {int(rg) + 1})', fontsize=11, color=col, fontweight='bold', pad=10)
    ax.set_ylabel('coefficient'); ax.legend(fontsize=8.5, loc='upper right')
    for i, (t, r) in enumerate(zip(tru, rec)):
        if abs(t) < 1e-9:
            ax.text(i+w/2, r+.045, '\u22480 \u2713', ha='center', fontsize=8, color=GRN, fontweight='bold')
    ax.set_ylim(-.55, .92)

p = R['pooled']; rec = [p[v] for v in VARS]
x = np.arange(len(VARS)); w = .26
axes[2].bar(x-w, TRUE['0'], w, label='true (Hard)', color=HARD, alpha=.5)
axes[2].bar(x, TRUE['1'], w, label='true (Soft)', color=SOFT, alpha=.5)
axes[2].bar(x+w, rec, w, label='pooled fit', color='#3A3A44', alpha=.95)
axes[2].axhline(0, color='black', lw=.9); axes[2].set_xticks(x); axes[2].set_xticklabels(VL)
axes[2].set_title('Baseline: no segmentation', fontsize=11, color='#3A3A44', fontweight='bold', pad=10)
axes[2].legend(fontsize=8); axes[2].set_ylim(-.55, .95)
axes[2].text(.5, .93, 'pooled model matches\nNEITHER regime', transform=axes[2].transAxes, ha='center',
             fontsize=9, color=HARD, fontweight='bold',
             bbox=dict(boxstyle='round,pad=.35', fc='#FFF0EF', ec=HARD, lw=1))

fig.suptitle('Recovered structural coefficients per regime, versus a single pooled model',
             y=1.03, fontsize=12, fontweight='bold')
plt.tight_layout()
save(fig, 'fig07_coefficients')
