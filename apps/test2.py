from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from utils import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/test2.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader_W(dataset_name)
data_loader.load_graph()
#data_loader.load_community()
wG = data_loader.get_graph()

print(wG) # グラフのノード数、エッジ数出力
#print(f"community_num : {len(c_id)}") # コミュニティ数出力
print("-----------------------------------")
# ---------------------------------------------------

w_rw_obj = WeightRandomWalk()
walk = w_rw_obj.weighted_random_walk(wG, 1, 5)
print(walk)

print("--- END ---")
# ---------------------------------------------------
