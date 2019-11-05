
p_user = ["gyz", "syt", "xcy", "ljs", "lw", "cwh", "wjs", "lsm"]
g_user = ["lzp", "xt", "xjj", "zzy", "lry", "lmm", "lq", "zwx"]

select_time = {}
p_result = {}
g_result = {}

def calc_time(fs):
    lines = fs.readlines()
    for line in lines:
        line = line.strip().split()
        speed = select_time[line[1]]
        time = 0.0
        for i in range(2, 7):
            time += (float(line[i].split("%")[0]) / 100.0) * (speed[i - 2]) + 3.0
        time += (float(line[7].split("%")[0]) / 100.0) * 4.5
        if line[1] in p_user:
            if line[1] not in p_result.keys():
                p_result[line[1]] = 0.0
            p_result[line[1]] += time
        else:
            if line[1] not in g_result.keys():
                g_result[line[1]] = 0.0
            g_result[line[1]] += time
    g_ans = 0.0
    p_ans = 0.0
    for i in g_result.keys():
        g_ans += g_result[i]
    for i in p_result.keys():
        p_ans += p_result[i]
    return g_ans, p_ans
        
def calc_c(fs):
    lines = fs.readlines()
    p_c = [0.0, 0.0, 0.0, 0.0, 0.0]
    g_c = [0.0, 0.0, 0.0, 0.0, 0.0]
    for line in lines:
        line = line.strip().split()
        day = int(line[0])
        if line[1] in g_user:
            g_c[day] += (float(line[-1].split("%")[0]) / 100.0)
        else:
            p_c[day] += (float(line[-1].split("%")[0]) / 100.0)
    print((g_c) )
    print((p_c) )
        

if __name__ == "__main__":
    with open("./select_time.txt", "r") as f:
        lines = f.readlines()
        i = 1
        while i < len(lines):
            if lines[i - 1].strip().split()[0] == "wjs":
                i += 2
                continue
            temp = []
            line = lines[i].strip().split()
            for j in range(5):
                temp.append(float(line[j]))
            select_time[lines[i - 1].strip().split()[0]] = temp
            i += 2
    
    old = open("./data-analyze/predict_result.txt", "r")
    # old_g, old_p = calc_time(old)
    calc_c(old)
    p_result = {}
    g_result = {}
    new = open("./predict_result.txt", "r")
    # new_g, new_p = calc_time(new)
    calc_c(new)

    print((old_g, old_p) )
    print((new_g, new_p) )
    print((old_g / new_g, old_p / new_p) )
