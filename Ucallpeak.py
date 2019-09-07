# Ucallpeak 3.5

import argparse
import copy
import numpy
import os
from array import *

# criteria
req_FC = 1.25               # required fold change
req_FC_bckgr = 5            # required fold change above background
req_delta_background = 5    # required difference (delta) in backgrounds
# a delta oft stdv1 + stdv2 is required too (inserted below)

gap = 1 #gap allowed between significant areas to be merged 1 = no gap Values below threshold (gaps) will not be included in averages

#get arguments from command line
parser = argparse.ArgumentParser(description='Uaveragebedgraphs_args')
parser.add_argument('-o','--output', help='name of output file', required=True, type=str)
parser.add_argument('-t','--list_of_tfiles', help='treatment files', required=True, nargs='+', type=str)
parser.add_argument('-c','--list_of_cfiles', help='control files', required=True, nargs='+', type=str)
parser.add_argument('-chr','--only_chr', help='only do analysis for this chromosome - can be used to parallelize the script', required=False, type=str, default="all")
parser.add_argument('-e_bed','--exclude_bed_file', help='exclude all regions in this bed file', required=False, type=str, default=None)

args = vars(parser.parse_args())
treatment_files = args['list_of_tfiles']
control_files = args['list_of_cfiles']
only_chr = args['only_chr']

if only_chr != "all":
    output_file = args['output'] + "_" + only_chr + ".txt"
else:
    output_file = args['output'] + ".txt"

e_bedfile = args['exclude_bed_file']

number_of_files = len(control_files) + len(treatment_files)
complete_list_of_files = control_files + treatment_files

def makematrix (treatment_files, control_files, newfile, only_chr):
    print("Starting analysis:")
    if only_chr != "all": print("Analysis only performed for chr: " + only_chr + ", as requested")
    if e_bedfile is None: print("No BED file to subtract detected")
    elif e_bedfile is not None: print("Regions from " + e_bedfile + " will be excluded from the analysis")

    try: os.remove(output_file)
    except: pass

    if len(control_files) < 2 or len(treatment_files) < 2:
        print("Error: Two files for each condition are needed.")
        sys.exit()

# Write headings
    with open(newfile, "a") as f:  # Write headings
        f.write("chr" + "\t" + "start" + "\t" + "stop" + "\t")
        for x, sample in enumerate(control_files):
            f.write("Ctrl" + str(x) + "\t")
        for x, sample in enumerate(treatment_files):
            f.write("Treatment" + str(x) + "\t")
        f.write("average Ctrl" + "\t" + "average Treatment" + "\t" + "Delta_treat-ctrl" + "\t" + "FC" + "\t" + "STD_ctrl" + "\t" + "STD_treat" + "\t" + "Score" + "\t" + "Coords" + "\t" + "length" + "\n")

# make list of chromosomes
    chromosomes = []
    for file in complete_list_of_files:
        with open(file) as f:
            for line in f:
                line_split = line.split("\t")
                if line_split[0][0:3] == "chr": # account for different formats with and without "chr"
                    line_split[0] = line_split[0][3:]
                if line_split[0] not in chromosomes:
                    if only_chr == "all": #check if analysis was limited to one chromosome
                        chromosomes.append(line_split[0])
                    elif only_chr == line_split[0]:
                        chromosomes.append(line_split[0])

# MAIN CODE STARTS HERE
    while len(chromosomes) > 0:
        print("Working on chromosome " + str(chromosomes[0]))
        current_chromosome = chromosomes.pop(0)

    # get length of current chromosome
        stop = 0
        output = []
        for file in complete_list_of_files: # go through all files
            with open(file) as f:
                for line in f:
                    line_split = line.split("\t")
                    if line_split[0][0:3] == "chr":  # account for different formats with and without "chr"
                        line_split[0] = line_split[0][3:]
                    if line_split[0] == current_chromosome:
                        if int(line_split[2]) > stop:
                            stop = int(line_split[2])

# continue only if values in chromosome
    # make the empty array for all the data
        if stop > 0:
            for i in range(number_of_files):
                output.append(array('f', [0] * stop))

    # fill output with data
            temp_matrix = []
            for x, file in enumerate(complete_list_of_files):
                with open(file) as file:
                    for line in file:
                        line_split = line.split("\t")
                        line_split[3] = line_split[3].replace("\n", "")
                        if line_split[0][0:3] == "chr":  # account for different formats with and without "chr"
                            line_split[0] = line_split[0][3:]
                        if line_split[0] == current_chromosome:
                            if float(line_split[3]) > 0:
                                for position in range(int(line_split[2]) - int(line_split[1])):
                                    coord = position + int(line_split[1])
                                    output[x][coord] = float(line_split[3])

    # if BED for excluding regions was provided -> exclude regions
            if e_bedfile is not None:
                with open(e_bedfile) as BED:
                    for line in (BED):
                        line_split = line.split("\t")
                        line_split[2] = line_split[2].replace("\n", "")
                        if line_split[0][0:3] == "chr":  # account for different formats with and without "chr"
                            line_split[0] = line_split[0][3:]
                        if line_split[0] == current_chromosome:
                            for position in range(int(line_split[2]) - int(line_split[1])):
                                coord = position + int(line_split[1])
                                for x, dataset in enumerate(output):
                                    if coord < len(output[0]):  #as BED file might be longer than output
                                        output[x][coord] = 0

    # get background
            output_row = []
            background = numpy.mean(output)
    # gather values from temp_matrix
            for n, value in enumerate(output[0]):
                output_row_temp = []
                for i in range(len(complete_list_of_files)):
                  output_row_temp.append(output[i][n])
    #Write averages
                average_ctrl = 0
                ctrl_values = []
                for x, sample in enumerate(control_files):
                    average_ctrl = average_ctrl + (output[x][n] / len(control_files))
                    ctrl_values.append(output[x][n])
                output_row_temp.append(average_ctrl)
                average_treat = 0
                treat_values = []
                for x, sample in enumerate(treatment_files):
                    average_treat = average_treat + (output[x+len(ctrl_values)][n] / len(treatment_files))
                    treat_values.append(output[x+len(ctrl_values)][n])
                output_row_temp.append(average_treat)

    #Write delta
                output_row_temp.append(average_treat - average_ctrl)
    # Write FC
                output_row_temp.append((average_treat+background)/(average_ctrl + background))
    # Write STD
                c_std = numpy.std(ctrl_values)
                output_row_temp.append(c_std)
                t_std = numpy.std(treat_values)
                output_row_temp.append(t_std)


    # check criteria, add chromosome location and concatenate rows with the same values --> inefficient, but keep code in case you want to plot FC ect on bp resolution
                if check_criteria(average_ctrl, background, average_treat, c_std, t_std, ctrl_values, treat_values) == True:
                    chr_start = n
                    chr_stop = n + 1
                    put_in_temp_matrix(current_chromosome, chr_start, chr_stop, output_row_temp, temp_matrix)

    # consolidate temp matrix into peaks and write to file
            temp = []
            for x, row in enumerate(temp_matrix):
                if x == 0:
                    temp.append(copy.deepcopy(row))
                elif int(row[2]) == int(temp[len(temp)-1][2])+gap:
                    temp.append(row)
                else:
                    consolidate(temp, newfile)
                    temp = []
                    temp.append(copy.deepcopy(row))
            if temp != []: # last row
                consolidate(temp, newfile)

def put_in_temp_matrix (current_chromosome, chr_start, chr_stop, data, temp_matrix): # stores the complete dataset before catting: Chr, Start, Stop, Data...
    temp = []
    temp.append(current_chromosome)
    temp.append(str(chr_start))
    temp.append(str(chr_stop))
    for i in data:
        temp.append(str(i))
    temp_matrix.append(temp)
def check_criteria (average_ctrl, background, average_treat, c_std, t_std, ctrl_values, treat_values):
    if ((average_ctrl+background)/(average_treat+background)) > req_FC or ((average_treat+background)/(average_ctrl+background)) > req_FC:  # Fold change check
        if average_ctrl > (req_FC_bckgr * background) or average_treat > (req_FC_bckgr * background):  # if Ctrl or Treat are above threshold
            if numpy.absolute(average_ctrl-average_treat) > (req_delta_background * background):  # if Ctrl or Treat are above threshold2
                if c_std + t_std < numpy.absolute(average_ctrl-average_treat):  # if delta is above the sum of std
                    return True
    return False
def consolidate(matrix, newfile):
    output_row_temp = []
    for i, n in enumerate(matrix[0]):  # go through each value
        if i == 0:
            output_row_temp.append(matrix[0][0])  # chromosome
        elif i == 1:
            output_row_temp.append(matrix[0][1])  # Start
        elif i == 2:
            output_row_temp.append(matrix[len(matrix) - 1][2])  # Stop
        else:  # all values
            average = []
            for entry in matrix:
                average.append(float(entry[i]))
            if i == 10: fc = numpy.average(average)
            output_row_temp.append(numpy.average(average))
    output_row_temp.append(numpy.sqrt(fc * (int(matrix[len(matrix) - 1][2])-(int(matrix[0][1]))))) # Score
    output_row_temp.append("chr" + str(matrix[0][0]) + ":" + str(matrix[0][1]) + "-" + str((matrix[len(matrix) - 1][2])))  # Coordinates for IGV or such
    output_row_temp.append(int(matrix[len(matrix) - 1][2])-int(matrix[0][1]))  # add peak length value
    write_to_file(output_row_temp, newfile)
def write_to_file (row, filename):
    with open(filename, "a") as f:
        for value in row:
            f.write(str(value))
            f.write("\t")
        f.write("\n")

############################################################################

makematrix(treatment_files, control_files, output_file, only_chr)
print("Success :) Enjoy your Data!")


# FC not sufficient, what if many reads but onlu 20% more
# background is calculated for each chromosome of all files combined _> overestimation which is good
# make sure all empty rows are removed from files
