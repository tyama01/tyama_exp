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


# /usr/bin/python3 /Users/tyama/tyama_exp/cpp/plot/plot_acc_time.py

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
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
#ax.set_xlabel("$\u03b5$", fontsize=14)
ax.set_ylabel("実行時間 (sec)", fontsize=20)

x = [1, 2]
y = [8.2097, 4.74548]

ax.bar(x, y, color=["blue", "red"])

x_labels = ["$\u03b5$=0.1で\n全ノードの\n還流度を計算", "top-100の\n精度保証 $\u0394$=1e$^-4$"]

# ラベルの設定
plt.xticks(x, x_labels, fontsize = 18)

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------