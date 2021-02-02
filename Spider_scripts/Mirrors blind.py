# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 14:19:48 2021

___  ____                          ______ _ _           _ 
|  \/  (_)                         | ___ \ (_)         | |
| .  . |_ _ __ _ __ ___  _ __ ___  | |_/ / |_ _ __   __| |
| |\/| | | '__| '__/ _ \| '__/ __| | ___ \ | | '_ \ / _` |
| |  | | | |  | | | (_) | |  \__ \ | |_/ / | | | | | (_| |
\_|  |_/_|_|  |_|  \___/|_|  |___/ \____/|_|_|_| |_|\__,_|
                                                          
                                                          


@author: Paweł Jakuszyk
"""


import numpy as np
import pandas as pd


# read log file separated by tabulators
log = pd.read_csv(r'C:\Users\Pawel\Desktop\Braille_Project\BRAJL_LOGI\surowe\mirror\ABM01-mirror_blind_run1.log', sep='\t',skiprows=(0,1,2),header=(0))

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

#create a column with reaction times [RT]
log['RT'] = log['Time_sec'].rolling(min_periods=2, window=2).apply(lambda x: x.iloc[1] - x.iloc[0])
log['RT'] = log[log['event_type']=='Response']['RT']

#create columns that show the stimuli orders/type

log['code_stimuli2'] = log['code'].shift(1)

log['code_stimuli1'] = log['code'].shift(2)

#create a column from conditions based on which to calculate correct answers

#extra column with characters only from the right
log['code_right1'] = log['code_stimuli1'].str[-1:]
log['code_right2'] = log['code_stimuli2'].str[-1:]

#extra column with characters only from the left
log['code_left1'] = log['code_stimuli1'].str[:1]
log['code_left2'] = log['code_stimuli2'].str[:1]

log['code_stimuli1'].str[:2]

log['corr'] = np.where((log['code'] == '1') & (log['code_left2'] == 'S') & (log['code_left1'] == 'S') | (log['code'] == '2') & (log['code_left2'] == 'D') & (log['code_left1'] == 'D'),1,0)

#create columns with RT values from various conditions
log['SN'] = np.where((log['event_type'] == 'Response') & (log['code_stimuli1'].str[:2] == 'SN') & (log['code_stimuli2'].str[:2] == 'SN'),log['RT'],np.nan)
log['SM'] = np.where((log['event_type'] == 'Response') & (log['code_stimuli1'].str[:2] == 'SM') & (log['code_stimuli2'].str[:2] == 'SM'),log['RT'],np.nan)
log['DN'] = np.where((log['event_type'] == 'Response') & (log['code_stimuli1'].str[:2] == 'DN') & (log['code_stimuli2'].str[:2] == 'DN'),log['RT'],np.nan)
log['DM'] = np.where((log['event_type'] == 'Response') & (log['code_stimuli1'].str[:2] == 'DM') & (log['code_stimuli2'].str[:2] == 'DM'),log['RT'],np.nan)

#Variables where we store meanRT for various conditions 
RTmeanSN = log['SN'].mean(skipna = True)

RTmeanSM = log['SM'].mean(skipna = True)

RTmeanDN = log['DN'].mean(skipna = True)

RTmeanDM = log['DM'].mean(skipna = True)


#Variables where we store sum of corrresct responses in for various conditions
sumSN = log['SN'].count()

sumSM = log['SM'].count()

sumDN = log['DN'].count()

sumDM = log['DM'].count()


#create a dataframe with all relevant info from this run 
output = pd.DataFrame({'sumSN': sumSN, 
                       'sumSM':sumSM, 
                       'sumDN':sumDN, 
                       'sumDM': sumDM, 
                       'RTmeanSN': RTmeanSN, 
                       'RTmeanSM' : RTmeanSM, 
                       'RTmeanDN':RTmeanDN, 
                       'RTmeanDM':RTmeanDM}, 
                      index = (0,1))

output['participant'] = log['subject']
output = output.drop(1)