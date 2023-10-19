import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from utils import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/pr_rw.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()

# {所属するコミュニティ：頂点idのリスト}, {頂点id:所属するコミュニティ}
c_id, id_c = data_loader.get_communities() 

print(G) # グラフのノード数、エッジ数出力
print(f"community_num : {len(c_id)}") # コミュニティ数出力
print("-----------------------------------")
# ---------------------------------------------------

# RandomWalkクラスのインスタンスを作成
random_walk_obj = RandomWalk()
prwk = random_walk_obj.pagerank(G, rwer_num=100, walk_length=100, d=0.85)

prwk_sort = sorted(prwk.items(), key=lambda x:x[1], reverse=True)



# ------------- PageRank 演算 ------------------------
pr = nx.pagerank(G, alpha=0.85)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

labels_data = []
for item in pr_sort:
    labels_data.append(item[0])

# ------------- Plot ------------------------
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

# x軸とy軸のラベルを設定する。
ax.set_xlabel("node ID", fontsize=14)
ax.set_ylabel("walk nums", fontsize=14)

x = np.arange(len(labels_data))

com_label_size = []
for i in range((len(c_id))):
    com_label_size.append(len(c_id[i]))

com_label_size_sort = np.argsort(com_label_size)[::-1]
common_com_list = com_label_size_sort[:11]
small_com_list = com_label_size_sort[10:]

common_com_y = np.array([])
small_com_y = np.array([])
for id in labels_data:
    if(id_c[id] in common_com_list):
        if(id in prwk):
            common_com_y = np.append(common_com_y, prwk[id])
        else:
            common_com_y = np.append(common_com_y, 0)
    else:
        common_com_y = np.append(common_com_y, np.nan)
        
for id in labels_data:
    if(id_c[id] in small_com_list):
        if(id in prwk):
            small_com_y = np.append(small_com_y, prwk[id])
        else:
            small_com_y = np.append(small_com_y, 0)
    else:
        small_com_y = np.append(small_com_y, np.nan)

        
# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
#ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))
#ax.xaxis.set_visible(False)
ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

# y軸の範囲を設定する。
#ax.set_ylim(0, 25000)
# y軸の目盛の位置を設定する。
#ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(2500))


#ax.scatter(x, y)

ax.scatter(x, common_com_y, label="common community")
ax.scatter(x, small_com_y, label="small community")

#ax.set_xscale('log')
#ax.set_yscale('log')

plt.legend()
plt.show()
# ---------------------------------------------------
