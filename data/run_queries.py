#!/usr/bin/env python

"""
Submit and run queries to cosmosim to download particle data for MDR1
"""

from __future__ import print_function, division
import numpy as np 
import os, sys, subprocess
import time
from astropy.io import ascii

def main():
    
    login_fname = 'login_info.txt'
    savepath = '/Volumes/G-RAID/simulations/unprocessed/MDR1/particles/snapshot_85/'
    
    #set the maximum time to spend on a given query
    max_time = 1000.0 #seconds
    
    #1st positional argument gives starting position in query list
    if len(sys.argv)>1:
        istart = int(sys.argv[1])
    else: 
        istart = 0
    
    #2nd positional argument gives the query list
    if len(sys.argv)>2:
        queries_fname = sys.argv[2]
    else:
        queries_fname = 'particles_queries_list.txt'

    #read in queries
    queries = ascii.read(queries_fname)
    N_queries = len(queries)

    #3rd positional argument gives the ending position in query list
    if len(sys.argv)>3:
        iend = int(sys.argv[3])
    else: 
        iend = N_queries
    
    #print out table of queries to be run
    print("running queries: ", istart, iend)
    print(queries[istart:iend])
    
    #read login information
    with open(login_fname) as f:
        info = f.readlines()
    info = [x.strip() for x in info]
    username = info[0]
    password=info[1]
    
    #create uws call to connect to cosmosim
    com = 'uws --host https://www.cosmosim.org/uws/query --user ' + username + ' --password ' + password +  ' job '
    
    #open file to store failed jobs list
    failed_jobs_file = open('failed_jobs.txt','w')

    # run queries
    for i in range(istart, iend):
        
        #get the time the job was submitted
        start = time.time()
        
        query = queries['query'][i]
        index = queries['index'][i]
        savename = queries['filename'][i]
        
        #submit job to server
        #q = com + 'new queue="long" query="' + query +'"' + ' table="subvol_' + str(index) + '"  --run'
        q = com + 'new queue="long" query="' + query +'"  --run' #dont name the table on the server
        result = os.popen(q)
        
        #get information about the job
        job_sub_dict = read_job(result)
        
        if job_sub_dict['Phase'] == 'ERROR':
            print("There was an unexpected error running: ", i, savename)
            print(job_sub_dict)
            time.sleep(1*60)
            continue

        #print out status
        print("running job: ", job_sub_dict['Job id'], job_sub_dict['Run id'], savename)
        
        #keep checking on the job until its done
        not_complete=True
        while not_complete:
            
            #wait before checking on job
            time.sleep(1*30)
            
            #calculate time elapsed since the job was submitted
            time_elapsed = time.time() - start
            
            #get current status of the job
            mid_result = os.popen(com + 'show '+ job_sub_dict['Job id'])
            job_sub_dict = read_job(mid_result)
            
            #given status, do some things
            if job_sub_dict['Phase'] == 'COMPLETED':
                print("    job completed in {} seconds".format(time.time()-start))
                not_complete=False
            elif time_elapsed>max_time:
                print("    job timed out after {} seconds".format(time.time()-start))
                time.sleep(1)
                break
            elif job_sub_dict['Phase'] == 'ERROR':
                print("    error!")
                print(job_sub_dict)
                time.sleep(1*60)
                break
            elif job_sub_dict['Phase'] == 'ABORTED':
                print("    job aborted after {} seconds".format(time.time()-start))
                time.sleep(1)
                break
            elif job_sub_dict['Phase'] == 'PENDING':
                print("    pending...")
            elif job_sub_dict['Phase'] == 'QUEUED':
                print("    queued...")
            elif job_sub_dict['Phase'] == 'EXECUTING':
                print("    executing...")
            else:
                print("    unexpected error: ", job_sub_dict['Phase'])
                break
        
        #if the job completed, download the file
        if not_complete==False:
            fname = savepath + savename
            e = 'http --auth '+username+':'+password+' --download GET https://www.cosmosim.org/query/download/stream/table/'+job_sub_dict['Run id']+'/format/csv --output '+ fname
            result = subprocess.call(e, shell=True) #this call is blocking
        else:
            print("     The job did not complete. The file could not be downloaded!")
            failed_jobs_file.write(str(index)+'.    '+q+'\n')

        #delete job
        if 'Job id' in job_sub_dict:
            print("    deleting job: ", job_sub_dict['Job id'])
            e = 'uws --host https://www.cosmosim.org/uws/query --user '+username+' --password '+password+' job delete ' + job_sub_dict['Job id']
            result = subprocess.call(e, shell=True) #this call is blocking
        
        
        
        
import csv
def read_job(file):
    """
    process output of the UWS job
    """
    
    #read in lines
    lines=[]
    for line in csv.reader(file, dialect="excel-tab"):
        try: 
            lines.append(line[0])
        except IndexError:
            break
    
    #create dictionary of results
    d = {}
    for i in range(2,15):
        try:
            line = lines[i].rstrip()
            key, value = line.rsplit('  ',1)
            value = value.lstrip()
            key = key.rstrip()
            d[key] = value
        except IndexError:
            d['Phase'] = 'ERROR'
            d['result'] = lines
            return d
    return  d

    
if __name__ == "__main__":
    main()


