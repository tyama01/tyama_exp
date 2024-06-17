# イプシロンを変えた場合の1ノード辺りの平均 RWer 数


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


# /usr/bin/python3 /Users/tyama/tyama_exp/cpp/apps/plot_omega.py

#------------------------------------------------------------------
# 事前準備

x_labels = ["0.1", "0.3", "0.5", "0.7", "0.9"]
eps_list = [0.1, 0.3, 0.5, 0.7, 0.9]
labels_series = ["SSPPR", "BATON", "Proposed_1", "Proposed_2"]

data_dic = dict()

data_dic["SSPPR"] = [13415543,1490616,536622,273787,165624]
data_dic["BATON"] = [1138195,126467,45529,23229,14053]
data_dic["Proposed_1"] = [22144,2461,886,452,274]
data_dic["Proposed_2"] = [21498,2390,861,440,266]

data = []

for key in data_dic:
    data.append(data_dic[key])


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
ax.set_xlabel("$\u03b5$", fontsize=14)
ax.set_ylabel("RWer 数", fontsize=14)

# マージンを設定
margin = 0.2  #0 <margin< 1
totoal_width = 1 - margin

x = np.array([1, 2, 3, 4, 5])
 
# 棒の幅を変数widthで保持する。
width = (1 - .2) / len(data)
# 棒グラフのオブジェクトのリストを変数barsで保持する。
bars = []
# データを描画する。
for i in range(len(data)):
    bars.append(ax.bar(x + (i - .5 * (len(data) - 1)) * width, data[i], width, label = labels_series[i], color=cmap(i)))

 
# ラベルの設定
plt.xticks(x, x_labels)


#plt.xlim(0.0002, 0.0005)

#plt.xlim(0, 10**-3)


#plt.xticks(x)
#plt.ylim(0,1)


# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()


#------------------------------------------------------------------