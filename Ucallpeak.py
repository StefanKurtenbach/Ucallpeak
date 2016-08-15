# calls peaks and provides an output.txt and begraph file

# needs sorted bedgraph files with additional fold-change column
# files should be normalized to RPM


import os

cut_off_RPM = 1       # threshold in RPM
cut_off_foldchange = 0.5  # threshold fold change
gap = 5                 # gaps allowed
min_peak_len = 10


def callpeak (file, outputfilename):
    temp = []
    with open(file) as f:
        output = []
        for line in f:
            line_split_temp = line.split("\t")
            line_split = []
            for x in line_split_temp:   # to be flexible in case this should work with normal bedgraphs too
                line_split.append(x.replace("\n", ""))
            try:
                if float(line_split[3]) > cut_off_RPM or float(line_split[3]) < -1*cut_off_RPM:   # if RMP cutoff fulfilled
                    if float(line_split[4]) > cut_off_foldchange or float(line_split[4]) < 1/cut_off_foldchange:
                        if temp == []:
                            temp = list(line_split)
                        else:
                            if temp[0] == line_split[0]:    #if same chromosome
                                if int(temp[2]) > int(line_split[1]) -1 -gap:    #if same peak
                                    x = int(temp[2]) - int(temp[1])
                                    y = int(line_split[2]) - int(line_split[1])
                                    temp[2] = line_split[2]
                                    temp[3] = (x*float(temp[3]) + y*float(line_split[3]))/(x+y) #average read in peak
                                    temp[4] = (x * float(temp[4]) + y * float(line_split[4])) / (
                                    x + y)  # average fold change in peak

                                else:               #if not same peak
                                    output.append(temp)
                                    temp = list(line_split)
                            else:
                                output.append(temp)
                                temp = list(line_split)
            except:
                pass


    with open(outputfilename + ".txt", "w") as f:
        f.write("Chromosome" + '\t' + "start" + '\t' + "stop" + '\t' + "RPMdiff" + '\t' + "foldchange" + '\n')
        for row in output:
            if int(row[2]) - int(row[1]) > min_peak_len:
                f.write('\t'.join([str(n) for n in row]) + '\n')

    with open(outputfilename + ".bedgraph", "w") as f:
        for row in output:
            if int(row[2]) - int(row[1]) > min_peak_len:
                row.pop(-1) #removes fold change
                f.write('\t'.join([str(n) for n in row]) + '\n')

#############################################

callpeak("substracted.txt", "final")