# Data

directory to store scripts to download data products needed for the analysis

the scripts are:
1.) create_queries.py
2.) run_queries.py
3.) remaining_count_queries.py

(1) cretaes text files whioch contain the list of queries that need to be made on Cosmosim, one list to download the particle data and another to query how may particles are in each subvolume.  

(2) This is the script which submits queries.  
To download all the particle data simply type:
    $user run_queries.py 0 particles_queries_list.txt
To download files which contain the total number of particles in each subvolume, type:
    $user run_queries.py 0 count_queries_list.txt

(3) checks the directory to see if any count queries failed to download and creates a new queires list which can be passed to (2) in order to download the remaining files.  This step can be repeated N times untill all the files are downloaded.

A file called login_info.txt should be edited to contain your cosmosim login information.  If you do not have a cosmosim account, go to cosmosim.org to create one.

