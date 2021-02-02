# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 16:21:12 2021

___  ____                          ______ _ _           _ 
|  \/  (_)                         | ___ \ (_)         | |
| .  . |_ _ __ _ __ ___  _ __ ___  | |_/ / |_ _ __   __| |
| |\/| | | '__| '__/ _ \| '__/ __| | ___ \ | | '_ \ / _` |
| |  | | | |  | | | (_) | |  \__ \ | |_/ / | | | | | (_| |
\_|  |_/_|_|  |_|  \___/|_|  |___/ \____/|_|_|_| |_|\__,_|
                                                          
                                                          
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
directory_to_write= filepath +"\\cleaned_blind"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the lists of subjects codes and runs you want to analyse
pNUM1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
pNUM2 = list(range(1, 1000))

pNUM = pNUM1 + pNUM2

timepoint = ['', '_2', '_3', '_4', '_42', '_22']

run = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6' ]

code = ['LBM', 'LBF', 'ABM', 'ABF', 'CBM', 'CBF']

version = ['', '_letters']

print('Commence cleaning!')
#loop all the possible combinations
for p in pNUM:
    for t in timepoint:
        for r in run:
            for c in code:
                for v in version:
                    # check if this file exists
                    my_file = Path(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) +'.log')
                       
                    if my_file.is_file():
                         # read log file separated by tabulators
                        log = pd.read_csv(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) +'.log' , sep='\t',skiprows=(0,1,2),header=(0))
                        print('Current log is ' + filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) +'.log')
                        
                        if 'Trial' in log.columns:

                            # fix the columns names
                            log.columns = log.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
                            
                            # get rid of the second dataframe below
                            log = log[log.subject != 'Picture'] 
                            log = log[log.subject != 'Event Type']
                        
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
                            
                            #some more cleaning
                            log = log[log.code != '6']
                            log = log[log.code != 'przerwa']
                            log = log[log.code != 'blank2']
                            log = log[log.code != 'blank1']
                            log = log[log.event_type != 'Port Input']
                      
                            # create column with time in seconds
                            #convert time column into floats    
                            log['time'] = pd.to_numeric(log['time'])
                            
                            #create first time valuse based on the first pulse from the scanner
                            for_time = log[log['code'] == '111' ].iloc[0]
                            for_time = for_time.reset_index()
                            first_pulse = for_time.iloc[3]
                            first_pulse.iloc[1]
                            
                            #calculate the column    
                            log['Time_sec'] = (log['time'] - first_pulse.iloc[1])/10000
                            
                            
                            #even more cleaning
                            log = log[log.code != '111']
                            
                            #reset index
                            log = log.reset_index()
                            
                            #drop old index
                            log.drop('index', inplace=True, axis=1)
                            
                            #save dataframe to excel 
                            log.to_excel(directory_to_write + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) + '.xlsx', index = None, header=True)
                        else:
                            pass
                    else:
                            pass
print('Data cleaning complete!')