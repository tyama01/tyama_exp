# イプシロンを変えた場合の実行時間計測


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


# /usr/bin/python3 /Users/tyama/tyama_exp/cpp/apps/plot_time.py

#------------------------------------------------------------------
# 事前準備

x_labels = ["0.1", "0.3", "0.5", "0.7", "0.9"]
eps_list = [0.1, 0.3, 0.5, 0.7, 0.9]
labels_series = ["SSPPR", "BATON", "Proposed_1", "Proposed_2"]

data_dic = dict()

data_dic["SSPPR"] = [154.697,84.4277,58.4563,43.6799,35.1101]
data_dic["BATON"] = [69.0186,25.783,15.007,9.28438,6.01645]
data_dic["Proposed_1"] = [8.417,1.2943,0.585752,0.353088,0.252964]
data_dic["Proposed_2"] = [8.2097,1.2687,0.571037,0.349626,0.249211]

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
ax.set_ylabel("実行時間 (sec)", fontsize=14)

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