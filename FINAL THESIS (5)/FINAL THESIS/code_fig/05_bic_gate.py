exec(open('00_common.py').read())

root = [x for x in R['nodes'] if x['path'] == 'root'][0]
kids = [x for x in R['nodes'] if x['path'] in ('rootL', 'rootR')]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.9))
lbl = ['root\n(n=9999)'] + [f"{'left' if k['path']=='rootL' else 'right'} leaf\n(n={k['n']})" for k in kids]
b1 = [root['BIC1']] + [k.get('BIC1', np.nan) for k in kids]
b2 = [root['BIC2']] + [k.get('BIC2', np.nan) for k in kids]
xx = np.arange(len(lbl)); wd = .36

bars1 = a1.bar(xx-wd/2, b1, wd, label='$BIC_1$ (one model)', color=NEU, alpha=.85)
bars2 = a1.bar(xx+wd/2, b2, wd, label='$BIC_2$ (two models)', color=ACC, alpha=.92)
a1.set_xticks(xx); a1.set_xticklabels(lbl, fontsize=8.5); a1.set_ylabel('BIC')
a1.set_title('BIC at each recursion node', fontsize=11, pad=10)
# legend placed ABOVE the axes entirely, out of the way of every bar/label
a1.legend(fontsize=8.5, loc='lower center', bbox_to_anchor=(0.5, 1.06), ncol=2, frameon=False)

ymin = min(b1 + b2); ymax = max(b1 + b2); span = ymax - ymin
a1.set_ylim(ymin - span*0.16, ymax + span*0.06)
for i, (u, v) in enumerate(zip(b1, b2)):
    if np.isnan(v): continue
    txt = 'SPLIT' if v < u else 'STOP'
    col = GRN if v < u else HARD
    a1.annotate(txt, xy=(i, min(u, v)), xytext=(0, -14), textcoords='offset points',
                ha='center', va='top', fontsize=8.5, fontweight='bold', color=col)

d = [u - v for u, v in zip(b1, b2)]
a2.bar(xx, d, .5, color=[GRN if x > 0 else HARD for x in d], alpha=.9)
a2.axhline(0, color='black', lw=1)
a2.set_xticks(xx); a2.set_xticklabels(lbl, fontsize=8.5)
a2.set_ylabel('$BIC_1 - BIC_2$'); a2.set_title('Split accepted when $BIC_1-BIC_2>0$', fontsize=11, pad=10)

fig.suptitle('BIC stopping rule: complexity penalty gates every candidate split',
             y=1.06, fontsize=12, fontweight='bold')
plt.tight_layout()
save(fig, 'fig05_bic_gate')
