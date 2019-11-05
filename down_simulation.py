import log
import os
import event
import panel
import entry

if __name__ == "__main__":
    root = "./data-main/"
    files = os.listdir(root)
    '''
    files = []
    with open("D:/ring input/mark.txt", "r") as f:
        ls = f.readlines()
        for l in ls:
            if ".txt" in l:
                l = l.strip()
                files.append(l)
    '''
    for fs in files:
        print((fs) )
        output = open("D:/ring input/data-corrected/" + fs, "w")
        with open(root + fs, "r") as f:
            lines = f.readlines()
            last_entry = -1
            for i in range(len(lines)):
                line = lines[i]
                line = line.strip().split()
                if len(line) ==  13:
                    continue
                else:
                    if line[1] == "ENTRY_A_LETTER":
                        up_timestamp = int(line[0])
                        eve = event.Event()
                        down_line = -1
                        down_time = -1
                        for j in range(last_entry - 100, i):
                            if len(lines[j].strip().split()) == 13:
                                data = [float(k) for k in lines[j].strip().split()]
                                curr_event = eve.get_event(data)
                                if curr_event == eve.TOUCH_DOWN:
                                    down_line = j
                                    down_time = int(data[0])
                        if down_line == -1:
                            down_line = i - 1
                        for j in range(last_entry + 1, down_line + 1):
                            output.write(lines[j])
                        data = [float(k) for k in lines[down_line].strip().split()]
                        output.write(str(int(data[0])) + " ENTRY_A_LETTER " + str(data[-3]) + " " + str(data[-2]) + "\n")
                        for j in range(down_line + 1, i):
                            output.write(lines[j])
                        last_entry = i
                    else:
                        for j in range(last_entry + 1, i + 1):
                            output.write(lines[j])
                        last_entry = i
                
            for i in range(last_entry + 1, len(lines)):
                output.write(lines[i])
        exit()          
