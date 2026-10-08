exec(open('00_common.py').read())

EFF = [('Hard','$L_X$',0.7111,0.70,0.68,0.7110,0.0016,0.7116),
       ('Hard','$\\Gamma$',-0.2964,-0.30,0.47,-0.2964,-0.0003,-0.2963),
       ('Hard','$HR$',-0.3981,-0.40,0.56,-0.3981,0.0011,-0.3985),
       ('Hard','$F_R(t\\!-\\!1)$',0.4983,0.50,0.73,0.4983,-0.0006,0.4979),
       ('Soft','$L_X$',0.1799,0.18,0.33,0.1800,-0.0006,0.1800),
       ('Soft','$\\Gamma$',0.1994,0.20,0.34,0.1993,-0.0005,0.1999),
       ('Soft','$T_{in}$',-0.3833,-0.40,0.51,-0.3833,-0.0001,-0.3829),
       ('Soft','$F_R(t\\!-\\!1)$',0.5062,0.50,0.73,0.5063,-0.0007,0.5059)]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={'width_ratios': [1.15, 1]})
lbl = [f'{r}\n{t}' for r, t, *_ in EFF]; est = [e[2] for e in EFF]; tru = [e[3] for e in EFF]
x = np.arange(len(EFF)); w = .37
cols = [HARD if e[0] == 'Hard' else SOFT for e in EFF]
a1.bar(x-w/2, tru, w, label='true coefficient', color=NEU, alpha=.5)
a1.bar(x+w/2, est, w, label='DoWhy estimate', color=cols, alpha=.93)
a1.axhline(0, color='black', lw=.9); a1.set_xticks(x); a1.set_xticklabels(lbl, fontsize=7.6)
a1.set_ylabel('causal effect'); a1.legend(fontsize=8.5)
a1.set_title('Estimated causal effects vs. generating coefficients', fontsize=11, pad=10)

# FIX: "random common cause" (green circle) and "80% data subset" (purple
# square) land at nearly identical (x,y) since both refuters barely move
# the estimate -- the previous version drew them at the same zorder, so
# the later-drawn purple squares completely hid the green circles beneath
# them. Fixed three ways at once: (1) make markers hollow/open so an
# underlying marker is visible through an overlapping one, (2) give each
# series a distinct marker size so edges don't fully coincide, (3) apply
# a small deliberate jitter so exact coincidences separate visually.
rng = np.random.default_rng(0)
jitter = lambda arr, s: np.array(arr) + rng.normal(0, s, len(arr))

rc = jitter([e[5] for e in EFF], 0.004)
ds = jitter([e[7] for e in EFF], 0.004)
pl = [e[6] for e in EFF]

a2.scatter(est, rc, s=150, facecolors='none', edgecolors=GRN, linewidths=2.2,
           label='random common cause', zorder=5)
a2.scatter(est, ds, s=80, facecolors=PUR, edgecolors='white', linewidths=1.0, marker='s',
           label='80% data subset', zorder=4, alpha=.9)
a2.scatter(est, pl, s=70, facecolors=HARD, edgecolors='white', linewidths=1.0, marker='^',
           label='placebo treatment', zorder=6)
lim = [-.55, .85]
a2.plot(lim, lim, ls='--', color=NEU, lw=1, alpha=.7, label='unchanged (y = x)', zorder=1)
a2.axhline(0, color=HARD, ls=':', lw=1, alpha=.7, zorder=1)
a2.set_xlim(lim); a2.set_ylim(lim); a2.set_xlabel('original estimate'); a2.set_ylabel('estimate after refutation')
a2.legend(fontsize=8, loc='upper left'); a2.set_title('Refutation tests', fontsize=11, pad=10)
a2.text(.52, .12, 'placebo collapses\nto \u2248 0  \u2713', transform=a2.transAxes, fontsize=8.6, color=HARD, fontweight='bold')

fig.suptitle('Causal effect estimation and refutation battery (all tests passed)',
             y=1.03, fontsize=12, fontweight='bold')
plt.tight_layout()
save(fig, 'fig10_effects_refutation')
