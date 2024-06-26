# top-100 位までの精度保証の度に更新したε の値と Δ の関係 ω の関係


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


# /usr/bin/python3 /Users/tyama/tyama_exp/cpp/plot/plot_eps_min.py

#------------------------------------------------------------------

#------------------------------------------------------------------
# 事前準備
delta_list = [1.00E-01, 1.00E-02, 1.00E-03, 1.00E-04, 1.00E-05]

eps_list = [0.1, 0.1, 0.00265777, 6.29E-05, 1.62E-05]

omega_list = [21498, 21498, 30432255, 54333493462, 8.19104E+11]


#------------------------------------------------------------------


#------------------------------------------------------------------
# plot 

# delta と ε の値

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

ax.set_xscale('log')
ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("$\u0394$", fontsize=20)
ax.set_ylabel("Update $\u03b5$", fontsize=20)


ax.scatter(delta_list, eps_list)
ax.plot(delta_list, eps_list)

# 反転 大きいのが左
ax.invert_xaxis()


#x_labels = ["0", "1", "2", "3", "4"]

# ラベルの設定
#plt.xticks(x, x_labels)

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------

#------------------------------------------------------------------
# plot 

# ε と ω の関係

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
ax.set_xlabel("$\u03b5$", fontsize=20)
ax.set_ylabel("$\u03c9$", fontsize=20)

x_list = [i for i in range(len(omega_list))]

ax.bar(x_list, omega_list)

# 反転 大きいのが左
#ax.invert_xaxis()

pos = [1, 10, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7, 10**8, 10**9, 10**10, 10**11, 10**12, 10**13, 10**14]
ax.set_yticks(pos)

plt.ylim(0,10**14)


#x_labels = ["0", "1", "2", "3", "4"]

# ラベルの設定
plt.xticks(x_list, eps_list)

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

#plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------