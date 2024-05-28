# ダンベルグラフで簡易実験 自ノードに帰ってくる累積 RWer 数 をプロット
# 同じような振る舞いをするかをチェック

from utils import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams as rcp


# /usr/bin/python3 /Users/tyama/tyama_exp/apps6/test_plot_cumlative_r.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name, is_directed=False)
G = data_loader.get_graph()
print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")

node_list = list(G.nodes)
n = len(node_list)

# -----------------------------------------------

# -----------------------------------------------
# 着目ノードリスト
focus_id_list = [100, 101, 102, 103, 104, 105, 106]

# {forcus_id : [hop数ごとの RWer 数の累積和]}
self_rw_dic = {}

self_rw_obj = SelfRW_Reach(G)

for forcus_id in focus_id_list:
    self_rw_dic[forcus_id] = self_rw_obj.calc_cumulative_sum_by_self_rw(source_node=forcus_id, rwer_num=1000, hop_num=20)


id_100_list = self_rw_obj.calc_area(self_rw_dic[100])
print(len(id_100_list))
print(id_100_list)

# -----------------------------------------------

# -----------------------------------------------
# プロット

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
ax.set_xlabel("Hop num", fontsize=14)
ax.set_ylabel("Sum of RWer num", fontsize=14)



x = [i for i in range(21)]

plt.xticks(x)
plt.ylim(0,1)


for forcus_id in self_rw_dic:
    ax.scatter(x, self_rw_dic[forcus_id], label= str(forcus_id))
    ax.plot(x, self_rw_dic[forcus_id])



# グリッドを表示する。
ax.set_axisbelow(True)
ax.grid(True, "major", "x", linestyle="--")
ax.grid(True, "major", "y", linestyle="--")

plt.legend()
plt.tight_layout()
plt.show()


# -----------------------------------------------



