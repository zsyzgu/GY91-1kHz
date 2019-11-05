from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def transpose(X):
    m, n = len(X), len(X[0])
    return [[X[i][j] for i in range(m)] for j in range(n)]

if __name__ == "__main__":
    sub_speed_g_1 = [4, 1, 2, 4, 4, 4, 1]
    sub_acc_g_1 = [6, 5, 7, 3, 4, 3, 1]
    phy_g_1 = [3, 3, 5, 3, 5, 3, 3]
    men_g_1 = [3, 2, 5, 4, 5, 4, 6]
    prefer_g_1 = [7, 6, 4, 5, 5, 5, 5]

    sub_speed_g_5 = [6, 5, 6, 7, 7, 6, 3]
    sub_acc_g_5 = [5, 6, 6, 6, 6, 6, 3]
    phy_g_5 = [2, 3, 7, 4, 6, 5, 5]
    men_g_5 = [6, 6, 7, 4, 6, 6, 4]
    prefer_g_5 = [7, 6, 6, 7, 5, 7, 5]

    sub_speed_p_1 = [3, 4, 2, 5, 4] 
    sub_acc_p_1 = [4, 4, 2, 5, 3]
    phy_p_1 = [4, 4, 3, 6, 3]
    men_p_1 = [4, 5, 4, 5, 4]
    prefer_p_1 = [5, 5, 2, 6, 4]
    
    sub_speed_p_5 = [6, 5, 7, 5, 6]
    sub_acc_p_5 = [6, 4, 5, 6, 7]
    phy_p_5 = [4, 4, 5, 5, 2]
    men_p_5 = [5, 6, 3, 5, 4]
    prefer_p_5 = [5, 7, 6, 7, 6]

    g_data = pd.DataFrame([sub_speed_g_1, sub_speed_g_5, sub_acc_g_1, sub_acc_g_5, phy_g_1, phy_g_5, prefer_g_1, prefer_g_5])
    p_data = pd.DataFrame([sub_speed_p_1, sub_speed_p_5, sub_acc_p_1, sub_acc_p_5, phy_p_1, phy_p_5, prefer_p_1, prefer_p_5])

    pos = [0, 1, 5, 6, 10, 11, 15, 16]
    plt.figure(figsize=(8, 5))
    plt.subplot(1, 2, 1)
    x = plt.boxplot(x=g_data, patch_artist=True, positions=pos, showfliers=False)
    cnt = 0
    for box in x["boxes"]:
        if cnt % 2 == 0:
            box.set(facecolor='#B0C915')
        else:
            box.set(facecolor='#FB9100')
        cnt += 1
    plt.legend([x["boxes"][0], x["boxes"][1]], ["Day 1", "Day 5"])
    
    
    plt.subplot(1, 2, 2)
    x = plt.boxplot(x=p_data, patch_artist=True, positions=pos, showfliers=False)
    cnt = 0
    for box in x["boxes"]:
        if cnt % 2 == 0:
            box.set(facecolor='#B0C915')
        else:
            box.set(facecolor='#FB9100')
        cnt += 1
    plt.legend([x["boxes"][0], x["boxes"][1]], ["Day 1", "Day 5"])
    plt.show()
