# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 11:46:00 2020

___  ____                       _____ _       _     _           _ 
|  \/  (_)                     /  ___(_)     | |   | |         | |
| .  . |_ _ __ _ __ ___  _ __  \ `--. _  __ _| |__ | |_ ___  __| |
| |\/| | | '__| '__/ _ \| '__|  `--. \ |/ _` | '_ \| __/ _ \/ _` |
| |  | | | |  | | | (_) | |    /\__/ / | (_| | | | | ||  __/ (_| |
\_|  |_/_|_|  |_|  \___/|_|    \____/|_|\__, |_| |_|\__\___|\__,_|
                                         __/ |                    
                                        |___/                     


@author: Paweł Jakuszyk
"""

import numpy as np
import pandas as pd


# read log file separated by tabulators
log = pd.read_csv(r'C:\Users\Pawel\Desktop\Braille_Project\BRAJL_LOGI\surowe\mirror\ACF02-mirror_image_run1.log', sep='\t',skiprows=(0,1,2),header=(0))

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
    
#create a column with reaction times [RT]
log['RT'] = log['Time_sec'].rolling(min_periods=2, window=2).apply(lambda x: x.iloc[1] - x.iloc[0])
log['RT'] = log[log['event_type']=='Response']['RT']

#create columns that show the stimuli orders/type


log['code_stimuli2'] = log['code'].shift(1)

log['code_stimuli1'] = log['code'].shift(2)


#szajs functions
"""
def correct(self):
    if [(log['event_type'] == 'Response') & (log['code'] == 2) & (log['code_stimuli2'] == 'c3') & (log['code_stimuli1'] == 'c4')]:
        return 1
    else:
        return 0

def test(self):
    if log.loc[log['code'] == '2']: #and log['code_stimuli2'] == 'c3']:
        return 1
    else:
        return 0

log.loc[(log['code'] == '2') & (log['code_stimuli1' == 'c2']), 'corr'] = 1


log['corr'] = log.apply(lambda x: 1 if log['code']  == '2' else 0, axis = 1)
"""
#create a column from conditions based on which to calculate correct answers

#extra column with characters only from the right
log['code_right1'] = log['code_stimuli1'].str[-1:]
log['code_right2'] = log['code_stimuli2'].str[-1:]


log['corr'] = np.where((log['code'] == '1') & (log['code_right2'] == log['code_right1']) | (log['code'] == '2') & (log['code_right2'] != log['code_right1']),1,0)

#create a column with SN/SM/DN/DM info

#extra column with characters only from the left
log['code_left1'] = log['code_stimuli1'].str[:1]
log['code_left2'] = log['code_stimuli2'].str[:1]

#create columns with RT values from various conditions
log['SN'] = np.where((log['event_type'] == 'Response') & (log['code_left1'] == log['code_left2']) & (log['code_right2'] == log['code_right1']),log['RT'],np.nan)
log['SM'] = np.where((log['event_type'] == 'Response') &(log['code_left1'] != log['code_left2']) & (log['code_right2'] == log['code_right1']),log['RT'],np.nan)
log['DN'] = np.where((log['event_type'] == 'Response') &(log['code_left1'] == log['code_left2']) & (log['code_right2'] != log['code_right1']),log['RT'],np.nan)
log['DM'] = np.where((log['event_type'] == 'Response') &(log['code_left1'] != log['code_left2']) & (log['code_right2'] != log['code_right1']),log['RT'],np.nan)

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
