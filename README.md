# Ucallpeak
##### Comprehensive NGS peak caller taking replicates into account to detect smaller changes.


<img src="https://raw.githubusercontent.com/StefanKurtenbach/Ucallpeak/master/Example%20peak%20calling.png" width="300">

Image shows Ucallpeak peakcalls in first row, and MACS2 bdgdiff calls with different stringency settings. 


#### Usage:

Use sorted normalized bedgraph files as input.



Example:
python Ucallpeak.py -t treatment1.bed treatment2.bed -c control1.bdg control2.bdg control3.bdg -o output.txt


Required:

-o		Output file name

-t    Treatment files

-c		Control files

Optional:

-chr    only do analysis for this chromosome - can be used to parallelize the script

-e_bed  exclude all regions in this bed file


Known issues:
- This script is not very efficient and will run for a significant time. It is reccomended to split up chromosomes (-chr command) to paralellize and speed up the analysis.
