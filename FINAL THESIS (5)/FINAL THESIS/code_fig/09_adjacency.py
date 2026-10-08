exec(open('00_common.py').read())

VL = ['$L_X$', '$\\Gamma$', '$T_{in}$', '$HR$', '$F_R$']
W0 = np.zeros((5,5)); W0[4,0]=.315; W0[4,1]=-.100; W0[4,3]=-.157
W1 = np.zeros((5,5)); W1[4,0]=.079; W1[4,1]=.090; W1[4,2]=-.212
A0 = np.diag([.851,.854,.843,.854,.527]); A1 = np.diag([.851,.839,.838,.847,.495])
T0 = np.zeros((5,5)); T0[4,0]=.70; T0[4,1]=-.30; T0[4,3]=-.40
T1 = np.zeros((5,5)); T1[4,0]=.18; T1[4,1]=.20; T1[4,2]=-.40

# Explicit GridSpec: 6 plot columns worth of width, reserving a clearly
# separate narrow column on the right for the colorbar so it can never
# overlap the 3rd heatmap column, regardless of figure size.
fig = plt.figure(figsize=(14.2, 8.2))
gs = fig.add_gridspec(2, 4, width_ratios=[1, 1, 1, 0.06], wspace=0.55, hspace=0.55,
                       left=0.06, right=0.93, top=0.84, bottom=0.08)
axes = np.array([[fig.add_subplot(gs[r, c]) for c in range(3)] for r in range(2)])
cax = fig.add_subplot(gs[:, 3])

sets = [(T0,'True $W$ \u2014 Hard',HARD), (W0,'DYNOTEARS $\\hat{W}$ \u2014 Hard',HARD), (A0,'DYNOTEARS $\\hat{A}$ \u2014 Hard',HARD),
        (T1,'True $W$ \u2014 Soft',SOFT), (W1,'DYNOTEARS $\\hat{W}$ \u2014 Soft',SOFT), (A1,'DYNOTEARS $\\hat{A}$ \u2014 Soft',SOFT)]
for ax, (M, t, c) in zip(axes.ravel(), sets):
    im = ax.imshow(M, cmap='RdYlGn', vmin=-.9, vmax=.9); ax.grid(False)
    ax.set_xticks(range(5)); ax.set_xticklabels(VL, fontsize=9)
    ax.set_yticks(range(5)); ax.set_yticklabels(VL, fontsize=9)
    ax.set_title(t, fontsize=10.5, color=c, fontweight='bold', pad=9)
    ax.set_xlabel('parent  $j$', fontsize=8.5, labelpad=2); ax.set_ylabel('child  $i$', fontsize=8.5)
    for i in range(5):
        for j in range(5):
            if abs(M[i,j]) > 1e-9:
                ax.text(j, i, f'{M[i,j]:.2f}', ha='center', va='center', fontsize=8.0, fontweight='bold',
                        color='black', clip_on=False,
                        path_effects=[pe.withStroke(linewidth=2, foreground='white')])

fig.colorbar(im, cax=cax, label='edge weight')
fig.suptitle('Recovered DYNOTEARS adjacency matrices versus ground truth\n'
             '$W$ = contemporaneous ($t\\!\\to\\!t$),   $A$ = lagged ($t\\!-\\!1\\!\\to\\!t$)',
             y=0.97, fontsize=12, fontweight='bold')
save(fig, 'fig09_adjacency')
