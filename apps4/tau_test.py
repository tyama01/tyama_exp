from scipy.stats import kendalltau

# /usr/bin/python3 /Users/tyama/tyama_exp/apps4/tau_test.py


# 統計学入門 - 東京大学出版会  p55 表3.9 を参考に作成  
x = [1,2,3,4]
#y = [3,1,2,4]
y = [5,3,4,6]

correlation, pvalue = kendalltau(x,y)
print("相関係数", correlation)
print("p値",pvalue)