#!/usr/bin/env python

from __future__ import print_function, division
import numpy as np 
import os, sys, fnmatch
from astropy.io import ascii

def main():

    savepath = '/Volumes/G-RAID/simulations/unprocessed/MDR1/particles/snapshot_85/'

    fnames = []
    for file in os.listdir(savepath):
        if fnmatch.fnmatch(file, 'subvol_*.csv'):
            if 'N' not in file:
                fnames.append(file)
    
    #read in queries
    queries_fname = 'particles_queries_list.txt'
    queries = ascii.read(queries_fname)

    mask = np.in1d(queries['filename'],fnames)
    
    ascii.write(queries[mask==False], './remaining_particles_queries.txt', overwrite=True)  

    fnames = []
    for file in os.listdir(savepath):
        if fnmatch.fnmatch(file, '*_N_*.csv'):
            fnames.append(file)
    
    #read in queries
    queries_fname = 'count_queries_list.txt'
    queries = ascii.read(queries_fname)

    mask = np.in1d(queries['filename'],fnames)
    
    ascii.write(queries[mask==False], './remaining_count_queries.txt', overwrite=True)  



if __name__ == "__main__":
    main()

