import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from data_loader import DataLoader
from walk import RandomWalk

# データ読み込み
dataset_name = input("Enter the dataset name: ")
data_loader = DataLoader(dataset_name)
data_loader.load_graph()
data_loader.load_community()
G = data_loader.get_graph()
c_id, id_c = data_loader.get_communities()

print(G)
print(len(c_id))