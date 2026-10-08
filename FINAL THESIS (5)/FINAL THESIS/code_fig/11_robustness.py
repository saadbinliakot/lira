exec(open('00_common.py').read())

EFF = [('Hard','$L_X$',.7111,.68,(0,14)),('Hard','$\\Gamma$',-.2964,.47,(0,14)),
       ('Hard','$HR$',-.3981,.56,(0,14)),('Hard','$F_R(t\\!-\\!1)$',.4983,.73,(-42,10)),
       ('Soft','$L_X$',.1799,.33,(-6,-22)),('Soft','$\\Gamma$',.1994,.34,(18,12)),
       ('Soft','$T_{in}$',-.3833,.51,(4,-22)),('Soft','$F_R(t\\!-\\!1)$',.5062,.73,(44,10))]

fig, ax = plt.subplots(figsize=(8.6, 5.4))
for r, t, e, rv, off in EFF:
    c = HARD if r == 'Hard' else SOFT
    ax.scatter(abs(e), rv, s=150, color=c, alpha=.88, edgecolor='white', lw=1.4, zorder=4)
    ax.annotate(t, (abs(e), rv), textcoords='offset points', xytext=off, ha='center', fontsize=9,
                color=c, zorder=5, path_effects=[pe.withStroke(linewidth=2.5, foreground='white')])
ae = np.array([abs(e[2]) for e in EFF]); rv = np.array([e[3] for e in EFF])
z = np.polyfit(ae, rv, 1); xs = np.linspace(.12, .78, 50)
ax.plot(xs, np.polyval(z, xs), ls='--', color=NEU, lw=1.3, alpha=.75, zorder=2)
ax.text(.04, .93, f'Pearson $r$ = {np.corrcoef(ae, rv)[0,1]:.3f}', transform=ax.transAxes, fontsize=10,
        fontweight='bold', color=NEU, bbox=dict(boxstyle='round,pad=.35', fc='#F4F4F6', ec=NEU, lw=.8))
ax.scatter([], [], s=110, color=HARD, label='Hard State'); ax.scatter([], [], s=110, color=SOFT, label='Soft State')
ax.legend(fontsize=9, loc='lower right'); ax.set_ylim(.24, .84); ax.set_xlim(.08, .80)
ax.set_xlabel('|estimated causal effect|'); ax.set_ylabel('robustness value  (Cinelli\u2013Hazlett)')
ax.set_title('Robustness to unobserved confounding scales with effect magnitude',
             fontsize=12, fontweight='bold', pad=12)
ax.text(.5, -.20, 'Weaker couplings require a substantially smaller hidden confounder to explain away \u2014 the Soft State\u2019s\n'
        'results therefore warrant correspondingly weaker claims than the Hard State\u2019s.',
        transform=ax.transAxes, ha='center', fontsize=8.4, color=NEU)
plt.subplots_adjust(bottom=.22)
save(fig, 'fig11_robustness')
