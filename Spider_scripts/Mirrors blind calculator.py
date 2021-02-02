# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:23:18 2021
___  ____                          ______ _ _           _ 
|  \/  (_)                         | ___ \ (_)         | |
| .  . |_ _ __ _ __ ___  _ __ ___  | |_/ / |_ _ __   __| |
| |\/| | | '__| '__/ _ \| '__/ __| | ___ \ | | '_ \ / _` |
| |  | | | |  | | | (_) | |  \__ \ | |_/ / | | | | | (_| |
\_|  |_/_|_|  |_|  \___/|_|  |___/ \____/|_|_|_| |_|\__,_|
                                                          
                                                          
 _____       _            _       _                       
/  __ \     | |          | |     | |                      
| /  \/ __ _| | ___ _   _| | __ _| |_ ___  _ __           
| |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|          
| \__/\ (_| | | (__| |_| | | (_| | || (_) | |             
 \____/\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|             
                                                          
                                                          
@author: Paweł Jakuszyk
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path

# Directory 
filepath = r'C:\Users\Pawel\Desktop\Braille_Project\BRAJL_LOGI\surowe\mirror\manually_checked_blind'
print("The path is: " + filepath)
# Directory for preprocessed data
directory_to_write= filepath +"\\results_blind"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the lists of subjects codes and runs you want to analyse
pNUM1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
pNUM2 = list(range(1, 1000))

pNUM = pNUM1 + pNUM2

timepoint = ['', '_2', '_3', '_4', '_42', '_22']

run = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6' ]

runs_to_correct = ['run2','run3', 'run5', 'run6']

code = ['LBM', 'LBF', 'ABM', 'ABF', 'CBM', 'CBF']

version = ['', '_letters']

#codes_to_correct = ['SN1', 'SN2']

#Define a master list for dataframes of all the participants values
master_list = []

print('Commence calculating!')

#loop all the possible combinations
for p in pNUM:
    for t in timepoint:
        for r in run:
            for c in code:
                for v in version:
                    # check if this file exists
                    my_file = Path(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) +'.xlsx')
                       
                    if my_file.is_file():
                         # read log file separated by tabulators
                        log = pd.read_excel(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) +'.xlsx',header=(0))
                        print('Current log is ' + filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) +'.xlsx')
                        ###correct for wrong encoding 
                        if (str(r) in runs_to_correct) & (str(v)==''):
                            print('Checking log ' + filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_blind' + str(v) + '_' + str(r) +'.xlsx')
                            SN1 =log['code'].iloc[27:28].tolist()
                            SN2 =log['code'].iloc[28:29].tolist()
                            bad_codes = SN1 + SN2
                            #print(log['code'].loc[27:28])
                            if  (log['code'].loc[0,] == 'DN1') & (log['code'].loc[1,] == 'DN2') & (log['code'].loc[3,] == 'DN1') & (log['code'].loc[4,] == 'DN2'):
                                pass
                            else:
                                if any('SN1' in s for s in bad_codes) & any('SN2' in s for s in bad_codes):
                                
                                    print('Correcting log')
                                    print(log['code'].loc[27,])
                                    print(log['code'].loc[28,])
                                    print('into')
                                    log['code'].loc[27,] = 'DN1'
                                    log['code'].loc[28,] = 'DN2'
                                    print(log['code'].loc[27,])
                                    print(log['code'].loc[28,])
                                else:
                                    pass                            
                        else:
                            pass
                        
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
                        

                        
                        output['participant'] = str(c) +str(p)
                        output['p_code'] = str(c)
                        output['run'] = str(r)
                        output['version'] = str(v)
                        output['timepoint'] = str(t)
                        output['group'] = 'blind'
                        
                        output['age'] = np.where(((output['p_code'] == 'ABM') | (output['p_code'] == 'ABF')),'adult','child')
                        
                        output.drop('p_code', inplace=True, axis=1)
                        
                        output = output[['participant','group','age','version','run','timepoint','RTmeanSN','RTmeanSM','RTmeanDN','RTmeanDM','sumSN','sumSM','sumDN','sumDM']]
                            
                        output = output.drop(1)
                            
                        #Append the result with a master dataframe list
                        master_list.append(output)

                            
                        #save dataframe to excel 
                        log.to_excel(directory_to_write + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) + 'calculated ' + '.xlsx', index = None, header=True)
                                                       
                                                        
                    else:
                        pass

#Concat the master_list 
data_master = pd.concat(master_list,ignore_index=True)

#fix the version values
data_master['version'] = data_master['version'].map({'': 'image', '_letters': 'letters'})

#drop timepoints
data_master = data_master[data_master.timepoint != '_2'] 
data_master = data_master[data_master.timepoint != '_3']
data_master = data_master[data_master.timepoint != '_4']
data_master = data_master[data_master.timepoint != '_42']
data_master = data_master[data_master.timepoint != '_22']
                           
data_master.drop('timepoint', inplace=True, axis=1)

#calculate mean for all runs
data_master_runMEAN = data_master.groupby(['participant','group','age','version'], as_index=False).mean()

#Save the master data to an excel file
data_master.to_excel(directory_to_write + '\\' + 'behavioral_results_blind.xlsx', index = None, header=True)
data_master_runMEAN.to_excel(directory_to_write + '\\' + 'behavioral_results_blind_runMEAN.xlsx', index = None, header=True)

#Save the master data to an csv file
data_master.to_csv(directory_to_write + '\\' + 'behavioral_results_blind.csv', index = None, header=True)
data_master_runMEAN.to_csv(directory_to_write + '\\' + 'behavioral_results_blind_runMEAN.csv', index = None, header=True)


print('Data processing complete!')