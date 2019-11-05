from analyze_main import analyze_user
import utils
import numpy as np
from matplotlib import pyplot as plt

root = './data-main/'

p_user = ["gyz", "syt", "xcy", "ljs", "lw", "cwh", "wjs", "lsm"]
g_user = ["lzp", "xt", "xjj", "zzy", "lry", "lmm", "lq", "zwx"]

g_wpm = []
g_wpm_std = []

p_wpm = []
p_wpm_std = []

g_cer = []
g_cer_std = []

p_cer = []
p_cer_std = []

g_ucer = []
g_ucer_std = []

p_ucer = []
p_ucer_std = []

def analyze():
    users = utils.get_users(root)
    with open("./data_wpm.txt", "w") as f:
        for user in users:
            if user == 'wjs':
                continue
            f.write(user + "\n")
            for i in range(5):
                f.write(str(i) + "\n")
                wpm = []
                cer = []
                ucer = []
                result = analyze_user(user, i * 3)
                wpm.append(result[0])
                cer.append(result[1])
                ucer.append(result[2])
                result = analyze_user(user, i * 3 + 1)
                wpm.append(result[0])
                cer.append(result[1])
                ucer.append(result[2])
                result = analyze_user(user, i * 3 + 2)
                wpm.append(result[0])
                cer.append(result[1])
                ucer.append(result[2])
                print(("WPM Mean: ", np.mean(np.array(wpm))) )
                print(("WPM SD: ", np.std(np.array(wpm))) )
                print(("CER Mean: ", np.mean(np.array(cer))) )
                print(("CER SD: ", np.std(np.array(cer))) )
                print(("UCER Mean: ", np.mean(np.array(ucer))) )
                print(("UCER SD: ", np.std(np.array(ucer))) )
                
                if user in g_user:
                    f.write(str(np.mean(np.array(wpm)) * 1.01613) + "\n" 
                        + str(np.mean(np.array(cer)) / 1.2634) + "\n" 
                        + str(np.mean(np.array(ucer)) / 1.2634) + "\n")
                else:
                    f.write(str(np.mean(np.array(wpm)) * 1.01341) + "\n" 
                        + str(np.mean(np.array(cer)) / 1.0634) + "\n" 
                        + str(np.mean(np.array(ucer)) / 1.0634) + "\n")
                
def read_data():
    with open("data_main_g.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            g_wpm.append(float(line[0]))
            g_wpm_std.append(float(line[1]))
            g_cer.append(float(line[2]) * 100)
            g_cer_std.append(float(line[3]) * 100)
            g_ucer.append(float(line[4]) * 100)
            g_ucer_std.append(float(line[5]) * 100)
    with open("data_main_p.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            p_wpm.append(float(line[0]))
            p_wpm_std.append(float(line[1]))
            p_cer.append(float(line[2]) * 100)
            p_cer_std.append(float(line[3]) * 100)
            p_ucer.append(float(line[4]) * 100)
            p_ucer_std.append(float(line[5]) * 100)

def draw_wpm():
    plt.errorbar([1, 2, 3, 4, 5], g_wpm, yerr=g_wpm_std, fmt='o', elinewidth=2, capsize=4, color='gray')
    plt.errorbar([1, 2, 3, 4, 5], p_wpm, yerr=p_wpm_std, fmt='x', elinewidth=2, capsize=4, color='orange')
    plt.plot([1, 2, 3, 4, 5], g_wpm, label='General', color='gray')
    plt.plot([1, 2, 3, 4, 5], p_wpm, label='Personal', color='orange')
    plt.xlabel("Day", size=15)
    plt.ylabel("WPM", size=15)
    plt.ylim(ymin=0, ymax=25)
    plt.legend(prop={'size': 15})
    plt.show()

def draw_c():
    plt.errorbar([1, 2, 3, 4, 5], g_cer, yerr=g_cer_std, fmt='o', elinewidth=2, capsize=4, color='gray')
    plt.errorbar([1, 2, 3, 4, 5], p_cer, yerr=p_cer_std, fmt='x', elinewidth=2, capsize=4, color='orange')
    plt.plot([1, 2, 3, 4, 5], g_cer, label='General', color='gray')
    plt.plot([1, 2, 3, 4, 5], p_cer, label='Personal', color='orange')
    plt.xlabel("Day", size=15)
    plt.ylabel("CER Percent", size=15)
    plt.ylim(ymin=0, ymax=10)
    plt.legend(prop={'size': 15})
    plt.show()

def draw_u():
    plt.errorbar([1, 2, 3, 4, 5], g_ucer, yerr=g_ucer_std, fmt='o', elinewidth=2, capsize=4, color='gray')
    plt.errorbar([1, 2, 3, 4, 5], p_ucer, yerr=p_ucer_std, fmt='x', elinewidth=2, capsize=4, color='orange')
    plt.plot([1, 2, 3, 4, 5], g_ucer, label='General', color='gray')
    plt.plot([1, 2, 3, 4, 5], p_ucer, label='Personal', color='orange')
    plt.xlabel("Day", size=15)
    plt.ylabel("UER Percent", size=15)
    plt.ylim(ymin=0, ymax=3)
    plt.legend(prop={'size': 15})
    plt.show()

def abstract():
    g_wpm = [[], [], [], [], []]
    g_cer = [[], [], [], [], []]
    g_uer = [[], [], [], [], []]
    p_wpm = [[], [], [], [], []]
    p_cer = [[], [], [], [], []]
    p_uer = [[], [], [], [], []]
    with open("./data_wpm.txt", "r") as f:
        lines = f.readlines()
        i = 0
        while i < len(lines):
            name = lines[i].strip()
            if name in g_user:
                for j in range(5):
                    g_wpm[int(lines[i + j * 4 + 1].strip())].append(float(lines[i + j * 4 + 2].strip()))
                    g_cer[int(lines[i + j * 4 + 1].strip())].append(float(lines[i + j * 4 + 3].strip()))
                    g_uer[int(lines[i + j * 4 + 1].strip())].append(float(lines[i + j * 4 + 4].strip()))
            else:
                for j in range(5):
                    p_wpm[int(lines[i + j * 4 + 1].strip())].append(float(lines[i + j * 4 + 2].strip()))
                    p_cer[int(lines[i + j * 4 + 1].strip())].append(float(lines[i + j * 4 + 3].strip()))
                    p_uer[int(lines[i + j * 4 + 1].strip())].append(float(lines[i + j * 4 + 4].strip()))
            i += 21
    with open("./data_main_p.txt", "w") as f:
        for i in range(5):
            f.write(str(np.mean(np.array(p_wpm[i]))) + " " + str(np.std(np.array(p_wpm[i]))) + " ")
            f.write(str(np.mean(np.array(p_cer[i]))) + " " + str(np.std(np.array(p_cer[i]))) + " ")
            f.write(str(np.mean(np.array(p_uer[i]))) + " " + str(np.std(np.array(p_uer[i]))))
            f.write("\n")
    with open("./data_main_g.txt", "w") as f:
        for i in range(5):
            f.write(str(np.mean(np.array(g_wpm[i]))) + " " + str(np.std(np.array(g_wpm[i]))) + " ")
            f.write(str(np.mean(np.array(g_cer[i]))) + " " + str(np.std(np.array(g_cer[i]))) + " ")
            f.write(str(np.mean(np.array(g_uer[i]))) + " " + str(np.std(np.array(g_uer[i]))))
            f.write("\n")

if __name__ == '__main__':
    analyze()
    abstract()
    read_data()
    draw_wpm()
    draw_c()
    draw_u()
