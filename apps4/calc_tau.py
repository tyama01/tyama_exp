# self PPR で重みづけをした PR 演算　のランキング変化を tau で比較
# データセット複数

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


# /usr/bin/python3 /Users/tyama/tyama_exp/apps4/calc_tau.py