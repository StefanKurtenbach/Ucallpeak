Ucallpeak - NGS peak caller taking replicates into account to detect smaller changes.

Use sorted bedgraph files as input. Threshold of peak detection and allowance for gaps can be set in the skript.

Example:
python Ucallpeak.py -t treatment1.bed treatment2.bed -c control1.bdg control2.bdg control3.bdg -o output.txt


Required:

-o    Output file name

-t    Treatment files

-c    Control files

Optional:
-chr    only do analysis for this chromosome - can be used to parallelize the script
-e_bed  exclude all regions in this bed file
