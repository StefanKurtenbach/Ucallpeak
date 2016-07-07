# needs sorted bedgraph files
# files should be normalized to RPM
# outputs bedgraph files
# makes peak bedgraph file for all files in folder

import os
import csv

cut_off = 0.1   # threshold in RPM
gap = 5         # gaps allowed


for file in os.listdir():
    output = []
    if file.endswith(".bedgraph"):
        temp = []
        with open(file) as f:
            for line in f:
                line_split = line.split("\t")       #check if there is a more efficient way to import
                line_split[3] = line_split[3].replace("\n", "")

                if float(line_split[3]) > cut_off or float(line_split[3]) < -cut_off:  # if no line in temp fill
                    if temp == []:
                        temp = list(line_split)
                    else:
                        if temp[0] == line_split[0]:    #if same chromosome
                            if int(temp[2]) > int(line_split[1]) -1 -gap:    #if same peak
                                x = int(temp[2]) - int(temp[1])
                                y = int(line_split[2]) - int(line_split[1])
                                temp[2] = line_split[2]
                                temp[3] = (x*float(temp[3]) + y*float(line_split[3]))/(x+y) #average read in peak
                            else:               #if not same peak
                                output.append(temp)
                                temp = list(line_split)
                        else:
                            output.append(temp)
                            temp = list(line_split)
        with open(file.replace(".bedgraph", "_peaks.bedgraph"), "w") as f:
            for row in output:
                f.write('\t'.join([str(n) for n in row])+'\n')