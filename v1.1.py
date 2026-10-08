import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import adjusted_rand_score


df = pd.read_csv('regime_dataset.csv')

print(df.head())

print(df.tail())


print(df.info())
print(df.describe())


features = ["L_x", "Gamma", "T_in", "H_r", "F_r"]

plt.figure(figsize=(14,8))

for i, col in enumerate(features):
    plt.subplot(3,2,i+1)
    plt.plot(df["t"], df[col])
    plt.axvline(400, linestyle="--")
    plt.title(col)
    plt.xlabel("Observation")

plt.tight_layout()
plt.show()
