# hcbb_provider_matching

In order to run the code save the initial data (provider_data.txt) and the python file (provider_solution.py) to a folder.  

Important adjustable parameters within the python script that will alter the outcome of the results include, but are not limited to: thres_count, counts, fuzz_thres, and sample_n.

Thresh_count:  This parameter accounts for columns with missing values and can be adjusted to drop columns accordingly.
counts:  This parameter takes into account the repeated values of Service Provider Names. 
Fuzzy_thres:  This parameter adjusts the acceptable threshold of the matching sequences.
Sample_n:  This parameter takes a random sample of the data set.  (to run this process on the full file is computationally                                                                        expensive)
