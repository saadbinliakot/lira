"""Shared style setup + data loading, imported by every figure script."""
import numpy as np, pandas as pd, json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

plt.rcParams.update({
    'font.family':'DejaVu Sans','font.size':10,'axes.linewidth':0.9,
    'axes.spines.top':False,'axes.spines.right':False,
    'figure.dpi':150,'savefig.dpi':200,'savefig.bbox':'tight',
    'axes.grid':True,'grid.alpha':0.22,'grid.linewidth':0.6,'axes.axisbelow':True,
})

HARD='#D64541'; SOFT='#2E7FBF'; ACC='#F2A03D'; NEU='#4A4A55'; GRN='#3EA96B'; PUR='#8B5FBF'; GREY='#9AA0AA'

def save(fig, name):
    """Save both PNG (for viewing/embedding) and SVG (vector, editable)."""
    fig.savefig(f'out/{name}.png')
    fig.savefig(f'out/{name}.svg')
    plt.close(fig)
    print(f'  saved {name}.png + {name}.svg')

import os
BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE, 'out'), exist_ok=True)

df2 = pd.read_csv(os.path.join(BASE, 'data_v2.csv'))
R = json.load(open(os.path.join(BASE, 'results_v2.json')))
Q = 6

def build_design(sub):
    s = sub.reset_index(drop=True)
    X = np.column_stack([np.ones(len(s)-1), s['L_x'].values[1:], s['Gamma'].values[1:],
                          s['T_in'].values[1:], s['H_r'].values[1:], s['F_r'].values[:-1]])
    return X, s['F_r'].values[1:]

def ols(X, Y):
    w, *_ = np.linalg.lstsq(X, Y, rcond=None)
    r = Y - X @ w
    return w, float(r @ r), r

def chowF(X, Y, tau):
    n = len(Y)
    if tau < 2*Q or n-tau < 2*Q: return np.nan
    _, rg, _ = ols(X, Y); _, ra, _ = ols(X[:tau], Y[:tau]); _, rb, _ = ols(X[tau:], Y[tau:])
    d = (ra+rb)/(n-2*Q)
    return np.nan if d <= 0 else ((rg-(ra+rb))/Q)/d
