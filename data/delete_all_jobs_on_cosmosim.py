#!/usr/bin/env python

"""
delete all queries on cosmosim
"""

from __future__ import print_function, division
import numpy as np 
import os, sys, subprocess
import time
from astropy.io import ascii
from uws import UWS

def main():
    
    login_fname = 'login_info.txt'

    #read login information
    with open(login_fname) as f:
        info = f.readlines()
    info = [x.strip() for x in info]
    username = info[0]
    password=info[1]

    url = 'https://www.cosmosim.org/uws/query/'
    c = UWS.client.Client(url, username, password)

    jobs = c.get_job_list({})
    ids = [x.id for x in jobs.job_reference]
    
    if len(ids)>0:
        for id in ids:
    	      print('deleting job: ', id)
    	      result = c.delete_job(id)
    else:
    	print('no jobs found')


if __name__ == "__main__":
    main()
