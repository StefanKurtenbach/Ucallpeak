# Ucallpeak
##### NGS peak caller taking replicates into account to detect smaller changes. Especially suited for ATAC-seq, as the peak caller does not require an input file. For other NGS datatypes use normalized bedgraphs.

![Image description](https://raw.githubusercontent.com/StefanKurtenbach/Ucallpeak/master/Example%20peak%20calling.png)

Image shows Ucallpeak peakcalls in first row, and MACS2 bdgdiff calls with different stringency settings. 


##### Howto:

Use sorted bedgraph files as input. Threshold of peak detection and allowance for gaps can be set in the skript.

Example:
python Ucallpeak.py -t treatment1.bed treatment2.bed -c control1.bdg control2.bdg control3.bdg -o output.txt


Required:

-o		Output file name

-t    Treatment files

-c		Control files

Optional:

-chr    only do analysis for this chromosome - can be used to parallelize the script

-e_bed  exclude all regions in this bed file
