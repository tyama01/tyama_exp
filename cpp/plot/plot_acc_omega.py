# top-100 位までの精度保証に必要な実行時間プロット


import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import matplotlib as mpl
from matplotlib import rcParams as rcp
from scipy.stats import kendalltau

import pandas as pd


# /usr/bin/python3 /Users/tyama/tyama_exp/cpp/plot/plot_acc_omega.py

#------------------------------------------------------------------

#------------------------------------------------------------------
# plot 

# フォントを設定する。
rcp['font.family'] = 'sans-serif'
rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# カラーマップを用意する。
cmap = plt.get_cmap("tab10")

# Figureを作成する。
fig = plt.figure()
# Axesを作成する。
ax = fig.add_subplot(111)

# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

#ax.set_xscale('log')
ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
#ax.set_xlabel("$\u03b5$", fontsize=14)
ax.set_ylabel("1ノード当たりに必要な平均RWer数", fontsize=18)

x = [1, 2, 3]
y = [3.39084E+13, 2.87684E+12, 54333493462]

ax.bar(x, y, color=["blue", "orange", "red"])

x_labels = ["SSPPR", "BATON", "Proposed"]

# ラベルの設定
plt.xticks(x, x_labels, fontsize=18)

pos = [1, 10, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10, 10**11, 10**12, 10**13, 10**14]
ax.set_yticks(pos)

plt.ylim(0,10**14)


# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------