# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 10:31:04 2020


___  ____                           _____ _       _     _           _  
|  \/  (_)                         /  ___(_)     | |   | |         | | 
| .  . |_ _ __ _ __ ___  _ __ ___  \ `--. _  __ _| |__ | |_ ___  __| | 
| |\/| | | '__| '__/ _ \| '__/ __|  `--. \ |/ _` | '_ \| __/ _ \/ _` | 
| |  | | | |  | | | (_) | |  \__ \ /\__/ / | (_| | | | | ||  __/ (_| | 
\_|  |_/_|_|  |_|  \___/|_|  |___/ \____/|_|\__, |_| |_|\__\___|\__,_| 
                                             __/ |                     
                                            |___/                      
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
filepath = r'C:\Users\Pawel\Desktop\Braille_Project\BRAJL_LOGI\surowe\mirror\manually_checked'
print("The path is: " + filepath)
# Directory for preprocessed data
directory_to_write= filepath +"\\results"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the lists of subjects codes and runs you want to analyse
pNUM1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
pNUM2 = list(range(1, 1000))

pNUM = pNUM1 + pNUM2

timepoint = ['', '_2', '_3', '_4', '_42', '_22']

run = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6' ]

code = ['LCM', 'LCF', 'ACM', 'ACF', 'CCM', 'CCF']

version = ['image', 'letters']

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
                    my_file = Path(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) +'.xlsx')
                       
                    if my_file.is_file():
                         # read log file separated by tabulators
                        log = pd.read_excel(filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) +'.xlsx',header=(0))
                        print('Current log is ' + filepath + '\\' + str(c) + str(p) + str(t) + '-mirror_' + str(v) + '_' + str(r) +'.xlsx')
                        
                        #check if the log is complete (ends with code : koniec)
                        if sum(log["code"].astype("str").str.contains("koniec")) > 0:
                            # fix the columns names
    
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
                            
                            output['participant'] = str(c) +str(p)
                            output['p_code'] = str(c)
                            output['run'] = str(r)
                            output['version'] = str(v)
                            output['timepoint'] = str(t)
                            output['group'] = 'sighted'
                            
                            output['age'] = np.where(((output['p_code'] == 'ACM') | (output['p_code'] == 'ACF')),'adult','child')
                            
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
'''
# melt from wide to long

data_master_long1 =  pd.melt(data_master, id_vars=['participant'], value_vars=['RTmeanSN','RTmeanSM','RTmeanDN','RTmeanDM'],

        var_name='conditions', value_name='meanRT')

data_master_long2 =  pd.melt(data_master, id_vars=['participant','age_group','version','run','timepoint'], value_vars=['RTmeanSN','RTmeanSM','RTmeanDN','RTmeanDM'],

        var_name='conditions', value_name='meanRT')

data_master_long3 =  pd.melt(data_master, id_vars=['participant'], value_vars=['RTmeanSN','RTmeanSM','RTmeanDN','RTmeanDM'],

        var_name='conditions', value_name='meanRT')


data_master_long = data_master_long.replace(             
   ['Target_Block_Neutral_maxAmp_Pz', 
    'Target_Block_Buzz_maxAmp_Pz', 
    'Target_Block_Nodis_maxAmp_Pz'],
                                  
   ['neutral_block',
    'buzz_block',
    'nodis_block']
   )

'''
#drop timepoints
data_master = data_master[data_master.timepoint != '_2']
data_master.drop('timepoint', inplace=True, axis=1)

#calculate mean for all runs
data_master_runMEAN = data_master.groupby(['participant','group','age','version'], as_index=False).mean()

#Save the master data to an excel file
data_master.to_excel(directory_to_write + '\\' + 'behavioral_results_sighted.xlsx', index = None, header=True)
data_master_runMEAN.to_excel(directory_to_write + '\\' + 'behavioral_results_sighted_runMEAN.xlsx', index = None, header=True)

#Save the master data to an csv file
data_master.to_csv(directory_to_write + '\\' + 'behavioral_results_sighted.csv', index = None, header=True)
data_master_runMEAN.to_csv(directory_to_write + '\\' + 'behavioral_results_sighted_runMEAN.csv', index = None, header=True)


print('Data processing complete!')