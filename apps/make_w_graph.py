import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from utils import*

# /usr/bin/python3 /Users/tyama/tyama_exp/apps/make_w_graph.py

# ---------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
G = data_loader.get_graph()

print(G) # グラフのノード数、エッジ数出力
print("-----------------------------------")
# ---------------------------------------------------

psi_obj = PSI(G)

#edge_weight = psi_obj.calc_psi()
#print(edge_weight)
#psi_obj.out_put_psi_graph(dataset_name)
psi_obj.out_put_reverse_psi_graph(dataset_name)


print("--- END ---")
# ---------------------------------------------------
