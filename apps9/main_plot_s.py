# コミュニティ内エッジ還流度の標準偏差を箱ひげ図でプロット
# コミュニティサイズと相関係数をプロット

from utils import *
import networkx as nx
import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import statistics
import matplotlib as mpl
from matplotlib import rcParams as rcp
from scipy.stats import kendalltau

from sklearn.preprocessing import normalize

import pandas as pd

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/main_plot_s.py

#------------------------------------------------------------------
# コミュニティサイズのリスト

L_com_size_list = [548,	535,436,426,423,350,328,237,226,206,128,73,	60,	25,	19,	19]

A_com_size_list = [1239,561,468,410,231,222,206,102,97,96,91,84,74,68,48,42]

P_com_size_list = [526,	514,513,332,327,300,265,239,207,170,169,164,130,76,	60,	47]

S_com_size_list = [1019,764,750,545,325,203,153,129,57,32,25,10,9,8,6,4]

#------------------------------------------------------------------

#------------------------------------------------------------------
# コミュニティ内エッジ還流度の標準偏差

L_s_list = [3.79E-05,3.58E-05,1.57E-05,3.24E-05,2.03E-05,6.87E-05,5.15E-06,5.36E-07,5.32E-06,5.92E-05,2.83E-05,1.16E-06,0.000137878,1.28E-06,5.74E-06,3.74E-06]

A_s_list = [4.06E-05,3.67E-05,5.96E-05,6.20E-05,4.12E-05,4.13E-06,5.78E-07,1.82E-06,5.48E-07,5.91E-07,4.35E-06,8.88E-08,4.68E-07,9.15E-08,9.93E-08,	7.37E-06]

P_s_list = [3.23E-05,1.95E-05,2.88E-05,3.69E-05,5.38E-07,4.93E-05,2.47E-05,9.00E-07,5.93E-05,1.91E-05,0.000107628,6.70E-07,4.54E-06,1.59E-05,0.000137878,1.31E-05]

S_s_list = [1.61E-05,2.15E-05,1.28E-05,3.78E-05,6.16E-05,4.60E-05,5.80E-05,3.59E-05,9.86E-05,0.000177867,2.28E-05,9.47E-06,1.87E-05,9.34E-06,2.98E-06,2.28E-06]


#------------------------------------------------------------------

#------------------------------------------------------------------

# 箱ひげ図プロット

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
#mpl.style.use('seaborn-darkgrid')

fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

#ax.set_xscale('log')
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("コミュニティ抽出手法", fontsize=20)
ax.set_ylabel("コミュニティ内エッジ還流度の標準偏差", fontsize=20)

data = [L_s_list, A_s_list, P_s_list, S_s_list]

ax.boxplot(data)


# ラベル表示
ax.set_xticklabels(['Louvain', '隣接行列', 'PR行列', '還流度行列'], fontsize=20)

# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")


plt.tight_layout()
plt.show()

#------------------------------------------------------------------

#------------------------------------------------------------------
# コミュニティサイズと標準偏差 プロット

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
#mpl.style.use('seaborn-darkgrid')

fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

#ax.set_xscale('log')
#ax.set_yscale('log')

# x軸とy軸のラベルを設定する。
ax.set_xlabel("コミュニティサイズ", fontsize=20)
ax.set_ylabel("標準偏差", fontsize=20)

ax.scatter(L_com_size_list, L_s_list, label="Louvain", c="r")
ax.plot(L_com_size_list, L_s_list, c= "r")

ax.scatter(A_com_size_list, A_s_list, label="隣接行列", c="m")
ax.plot(A_com_size_list, A_s_list, c="m")

ax.scatter(P_com_size_list, P_s_list, label="PR行列", c="g")
ax.plot(P_com_size_list, P_s_list, c="g")

ax.scatter(S_com_size_list, S_s_list, label="還流度行列", c="b")
ax.plot(S_com_size_list, S_s_list, c="b")


# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")


plt.legend()
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()
plt.show()

#------------------------------------------------------------------