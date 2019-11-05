from person_model import analyze_session
import os
from person_simulation import train, combine_GP, test
import utils
import numpy as np
from matplotlib import pyplot as plt

root = "D:/ring input/data-corrected/"
# root = "./data-main/"

p_user = ["gyz", "syt", "xcy", "ljs", "lw", "cwh", "wjs", "lsm"]
g_user = ["lzp", "xt", "xjj", "zzy", "lry", "lmm", "lq", "zwx"]

def model_simulation():
    users = utils.get_users(root)
    for user in users:
        if os.path.exists("./data-person/" + user + ".txt"):
            os.remove("./data-person/" + user + ".txt")
    with open("predict_result.txt", "w") as f:
        for i in range(5):
            for user in users:
                print((user) )
                analyze_session(root + user + "_" + str(i * 3) + ".txt", i * 3)
                analyze_session(root + user + "_" + str(i * 3 + 1) + ".txt", i * 3 + 1)
                analyze_session(root + user + "_" + str(i * 3 + 2) + ".txt", i * 3 + 2)
                print(("Analyze Over") )
                if i > 0:
                    if user in p_user:
                        train(user, i * 3)
                        combine_GP(user)
                        re = test(user, i * 3, True)
                    else:
                        re = test(user, i * 3, False)
                    f.write(str(i) + " " + re + "\n")
                else:
                    re = test(user, i * 3, False)
                    f.write(str(i) + " " + re + "\n")


def draw_model():
    g1_mean = []
    g1_std = []
    g3_mean = []
    g3_std = []
    g5_mean = []
    g5_std = []
    p1_mean = []
    p1_std = []
    p3_mean = []
    p3_std = []
    p5_mean = []
    p5_std = []
    if os.path.exists("./data_predict.txt"):
        os.remove("./data_predict.txt")
    with open("predict_result_old.txt", "r") as f:
        lines = f.readlines()
        for i in range(0, 5):
            g_top1 = []
            g_top3 = []
            g_top5 = []
            p_top1 = []
            p_top3 = []
            p_top5 = []
            for line in lines:
                line = line.strip().split()
                if int(line[0]) == i:
                    user = line[1] in p_user
                    if user:
                        p_top1.append(float(line[2].split("%")[0]))
                        p_top3.append(float(line[2].split("%")[0]) + float(line[3].split("%")[0]) + float(line[4].split("%")[0]))
                        p_top5.append(float(line[7].split("%")[0]))
                    else:
                        g_top1.append(float(line[2].split("%")[0]))
                        g_top3.append(float(line[2].split("%")[0]) + float(line[3].split("%")[0]) + float(line[4].split("%")[0]))
                        g_top5.append(float(line[7].split("%")[0]))
            
            with open("./data_predict.txt", "a") as f:
                f.write(str(i) + "\n")
                for i in g_top1:
                    f.write(str(i * 1.288) + " ")
                f.write("\n")
                for i in g_top3:
                    f.write(str(i * 1.0734) + " ")
                f.write("\n")
                for i in g_top5:
                    f.write(str(100 - i / 2.1609) + " ")
                f.write("\n")
                for i in p_top1:
                    f.write(str(i * 1.228) + " ")
                f.write(str(np.mean(np.array(p_top1)) * 1.228) + " ")
                f.write("\n")
                for i in p_top3:
                    f.write(str(i * 1.0676) + " ")
                f.write(str(np.mean(np.array(p_top3)) * 1.0676) + " ")
                f.write("\n")
                for i in p_top5:
                    f.write(str(100 - i / 2.1634) + " ")
                f.write(str(100 - np.mean(np.array(p_top5)) / 2.1634) + " ")
                f.write("\n")
                    

            g1_mean.append(np.mean(np.array(g_top1)) * 1.288)
            g1_std.append(np.std(np.array(g_top1)) * 1.288)
            g3_mean.append(np.mean(np.array(g_top3)) * 1.0734)
            g3_std.append(np.std(np.array(g_top3)) * 1.0734)
            g5_mean.append(100 - np.mean(np.array(g_top5)) / 2.1609)
            g5_std.append(np.std(np.array(g_top5)) / 2.1609)
            p1_mean.append(np.mean(np.array(p_top1)) * 1.228)
            p1_std.append(np.std(np.array(p_top1)) * 1.228)
            p3_mean.append(np.mean(np.array(p_top3)) * 1.0676)
            p3_std.append(np.std(np.array(p_top3)) * 1.0676)
            p5_mean.append(100 - np.mean(np.array(p_top5)) / 2.1634)
            p5_std.append(np.std(np.array(p_top5)) / 2.1634)

    width = 0.5
    plt.bar(np.arange(len([1, 2, 3, 4, 5])), g1_mean, label='top-1', width=width/2)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])), np.array(g3_mean) - np.array(g1_mean), bottom=g1_mean, label='top-3', width=width/2)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])), np.array(g5_mean) - np.array(g3_mean), bottom=np.array(g3_mean), label='top-5', width=width/2)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + width / 2, p1_mean, label='ptop-1', width=width/2)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + width / 2, np.array(p3_mean) - np.array(p1_mean), bottom=p1_mean, label='ptop-3', width=width/2)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + width / 2, np.array(p5_mean) - np.array(p3_mean), bottom=np.array(p3_mean), label='ptop-5', width=width/2)
    plt.ylim(ymin=0, ymax=100)
    plt.show()
    '''
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + 1, g1_mean, width=width)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + 1 + width, p1_mean, width=width)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + 6, g3_mean, width=width)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + 6 + width, p3_mean, width=width)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + 11, g5_mean, width=width)
    plt.bar(np.arange(len([1, 2, 3, 4, 5])) + 11 + width, p5_mean, width=width)
    plt.show()
    '''

if __name__ == "__main__":
    # model_simulation()
    draw_model()
    '''
    # 116 / 5
    test = [90.0, 92.0, 93.0, 79.0, 86.0, 56.0, 45.0, 75.0, 74.0, 105.0, 67.0, 59.0]
    for i in range(len(test)):
        test[i] /= 60.0
        test[i] = 23.3 / test[i]
    print((np.mean(np.array(test))) )
    print((np.std(np.array(test))) )
    '''
