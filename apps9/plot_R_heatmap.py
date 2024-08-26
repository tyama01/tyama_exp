# αを変えた場合の R ベクトル内のコミュニティ所属確率をヒートマップでプロッt

from utils import *
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

from sklearn.preprocessing import normalize

import pandas as pd

# /usr/bin/python3 /Users/tyama/tyama_exp/apps9/plot_R_heatmap.py

#------------------------------------------------------------------
# Rベクトル格納

# alpha 0.05, 0.1, 0.15
S_Rvec = [[6.09E-283,2.80E-02,9.72E-01], [1.47E-135,2.23E-02,9.78E-01], [3.14E-273,2.10E-02,9.79E-01]]

P_Rvec = [[0.00280592,0.02443698,0.9727571], [2.16E-05,2.43E-02,9.76E-01], [1.22E-06,2.44E-02,9.76E-01]]

A_Rvec = [[0.01605224,0.47622931,0.50771845]]


#------------------------------------------------------------------

#------------------------------------------------------------------
# ヒートマッププロット 数値も入れる

lst_y = ["0.05", "0.1", "0.15"]

plt.figure()
sns.heatmap(S_Rvec, square=True, cmap='coolwarm', vmin=0, vmax=1, annot=True, linewidths=True, yticklabels=lst_y)
#sns.heatmap(A_Rvec, square=True, cmap='coolwarm', vmin=0, vmax=1, annot=True, linewidths=True)

plt.show()


#------------------------------------------------------------------

