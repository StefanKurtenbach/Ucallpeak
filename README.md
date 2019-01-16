# Ucallpeak
Calls peaks from normalized bedgraph files

Use sorted bedgraph files as input. Threshold of peak detection and allowance for gaps can be set in the skript. The skript will take all bedgraph files in the same folder and perform peak calling on them. It's reccomended to use normalized bedgraph files.

Required:
-o    Output file name
-t    Treatment files
-c    Control files

Optional:
-chr    only do analysis for this chromosome - can be used to parallelize the script
-e_bed  exclude all regions in this bed file
