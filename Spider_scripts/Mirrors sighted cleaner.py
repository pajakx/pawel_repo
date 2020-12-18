# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:31:04 2020
___  ____                      _____ _       _     _           _ 
|  \/  (_)                    /  ___(_)     | |   | |         | |
| .  . |_ _ __ _ __ ___  ___  \ `--. _  __ _| |__ | |_ ___  __| |
| |\/| | | '__| '__/ _ \/ __|  `--. \ |/ _` | '_ \| __/ _ \/ _` |
| |  | | | |  | | | (_) \__ \ /\__/ / | (_| | | | | ||  __/ (_| |
\_|  |_/_|_|  |_|  \___/|___/ \____/|_|\__, |_| |_|\__\___|\__,_|
                                        __/ |                    
                                       |___/                     
  _____ _                                                        
 /  __ \ |                                                       
 | /  \/ | ___  __ _ _ __   ___ _ __                             
 | |   | |/ _ \/ _` | '_ \ / _ \ '__|                            
 | \__/\ |  __/ (_| | | | |  __/ |                               
  \____/_|\___|\__,_|_| |_|\___|_|         
@author: Paweł Jakuszyk
"""
import os
#import numpy as np
import pandas as pd
from pathlib import Path

# Directory 
filepath = r'C:\Users\Pawel\Desktop\Braille_Project\BRAJL_LOGI\surowe\mirror'
print("The path is: " + filepath)
# Directory for preprocessed data
directory_to_write= filepath +"\\cleaned"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the lists of subjects codes and runs you want to analyse
pNUM = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
#pNUM = list(range(1, 1000))
timepoint = ['', '_2', '_3', '_4', '_42', '_22']

run = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6' ]

code = ['LCM', 'LCF', 'ACM', 'ACF', 'CCM', 'CCF']

version = ['image', 'letters']

print('Commence cleaning!')
#loop all the possible combinations
for p in pNUM:
    for t in timepoint:
        for r in run:
            for c in code:
                for v in version:
                    # check if this file exists
                    my_file = Path(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) +'.log')
                       
                    if my_file.is_file():
                         # read log file separated by tabulators
                        log = pd.read_csv(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) +'.log' , sep='\t',skiprows=(0,1,2),header=(0))
                        print('Current log is ' + filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) +'.log')
                        
                        #check if the log is complete (ends with code : koniec)
                        if sum(log["Code"].astype("str").str.contains("koniec")) > 0:
                            # fix the columns names
    
                            log.columns = log.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
                            
                            # get rid of the second dataframe below
                            log = log[log.stim_type != 'next'] 
                            log = log[log.stim_type != 'ReqDur']
                            
                            # get rid of unncescessary columns
                            log.drop('ttime', inplace=True, axis=1)
                            log.drop('uncertainty.1', inplace=True, axis=1)
                            log.drop('reqtime', inplace=True, axis=1)
                            log.drop('reqdur', inplace=True, axis=1)
                            log.drop('stim_type', inplace=True, axis=1)
                            log.drop('pair_index', inplace=True, axis=1)
                            log.drop('uncertainty', inplace=True, axis=1)
                            log.drop('duration', inplace=True, axis=1)
                            log.drop('trial', inplace=True, axis=1)
                            
                            
                            # create column with time in seconds
                            #convert time column into floats    
                            log['time'] = pd.to_numeric(log['time'])
                                
                            #create first time valuse based on the first pulse from the scanner
                            for_time = log[log['code'] == '3' ].iloc[0]
                            for_time = for_time.reset_index()
                            first_pulse = for_time.iloc[3]
                            first_pulse.iloc[1]
                                
                            #calculate the column    
                            log['Time_sec'] = (log['time'] - first_pulse.iloc[1])/10000
                                
                                
                            #clean the data some more
                            log = log[log.code != '3']
                            log = log[log.code != 'przerwa']
                            
                            #reset index
                            log = log.reset_index()
                            
                            #drop old index
                            log.drop('index', inplace=True, axis=1)
                            
                            #save dataframe to excel 
                            log.to_excel(directory_to_write + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) + '.xlsx', index = None, header=True)
                            
                            
                        else:
                            pass
print('Data cleaning complete!')