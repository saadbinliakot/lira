exec(open('00_common.py').read())

TR = 5000; DET = R['leaves'][0][1]
fig, axes = plt.subplots(5, 1, figsize=(11, 8.6), sharex=True)
COLS = [('L_x', '#7A5C9E', '$\\log L_X$'), ('Gamma', '#C98A2B', '$\\Gamma$'),
        ('T_in', '#2E9B8F', '$\\log T_{in}$'), ('H_r', '#B5543F', '$HR$'),
        ('F_r', '#2E5FA3', '$\\log F_R$')]
for ax, (c, col, ylab) in zip(axes, COLS):
    ax.plot(df2['t'], df2[c], lw=.35, color=col, alpha=.85)
    ax.axvline(TR, color='black', lw=1.4, ls='--', alpha=.8)
    ax.axvline(DET, color=GRN, lw=1.4, ls='-', alpha=.9)
    ax.set_ylabel(ylab, fontsize=10)
    ax.axvspan(0, TR, color=HARD, alpha=.045)
    ax.axvspan(TR, 10000, color=SOFT, alpha=.045)
    # extra headroom above the data so state labels never crowd the top spine
    lo, hi = df2[c].min(), df2[c].max()
    pad = (hi-lo) * 0.28
    ax.set_ylim(lo - pad*0.15, hi + pad)

axes[0].text(2500, axes[0].get_ylim()[1]*0.90, 'Hard State', ha='center', fontsize=10,
             color=HARD, fontweight='bold')
axes[0].text(7500, axes[0].get_ylim()[1]*0.90, 'Soft State', ha='center', fontsize=10,
             color=SOFT, fontweight='bold')
axes[-1].set_xlabel('time index $t$')
axes[2].plot([], [], color='black', ls='--', label=f'true boundary (t={TR})')
axes[2].plot([], [], color=GRN, label=f'LIRA boundary (t={DET})')
axes[2].legend(loc='upper right', fontsize=8, framealpha=.95)

fig.suptitle('Synthetic accretion series with true and discovered regime boundary',
             y=0.995, fontsize=12, fontweight='bold')
plt.tight_layout()
save(fig, 'fig03_timeseries')
