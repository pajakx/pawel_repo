# -*- coding: utf-8 -*-
"""
  _____  _____   _____                                 
 |  __ \|  __ \ / ____|                                
 | |__) | |__) | (___                                  
 |  ___/|  ___/ \___ \      _                      _   
 | |    | |     ____) |    (_)                    | |  
 |_|____|_|__ _|_____/ _ __ _ _ __ ___   ___ _ __ | |_ 
  / _ \ \/ / '_ \ / _ \ '__| | '_ ` _ \ / _ \ '_ \| __|
 |  __/>  <| |_) |  __/ |  | | | | | | |  __/ | | | |_ 
  \___/_/\_\ .__/ \___|_|  |_|_| |_| |_|\___|_| |_|\__|
           | |                                         
           |_|                                         
"""
# import packages 
import numpy as np
import pandas as pd
import os
from os import listdir
from os.path import isfile, join


#Specify the path where you store the log files
mypath = r'C:\Users\Ada\Desktop\PPS_exp'

#Specify the path where you want the result to be saved
directory_to_write = r'C:\Users\Ada\Desktop\PPS_exp\results'
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)
    
#make a list of all the log file names from this directory
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

LogList =  [ x for x in onlyfiles if "gz" not in x ]


#Define a master list for dataframes of all the participants values
master_list = []

for p in LogList:

    # read log file

    log = pd.read_csv(mypath + '\\' + str(p))
    
    #show which log is being processed, useful for debugging
    
    print('Current log is ' + mypath + '\\' + str(p))
    
    # check your data
    #print(log)
    
    # Now we have to make the data look better. 
    #- remove colums we don't need for the analysis
    #- remove rows we don't need
    #- rename colums if needed
        
    # get rid of unncescessary columns 
    # column names that I want: participant, corrAns, date, key_trial.keys, key_trial.corr, trials.thisTrialN (order), key_trial.rt, video
    
    log = log[['participant', 'corrAns', 'key_trial.keys', 'key_trial.corr', 'trials.thisTrialN' , 'key_trial.rt', 'video']]
    
    #exclude practice
    log = log[log['video'].notna()]
    
    
    #create columns telling us the sum and percentage of missing responses
    log['missing_responsesSUM'] = log['key_trial.keys'].isna().sum()
    
    log['missing_responsesPERCENT'] = log['key_trial.keys'].isna().sum()/40*100
    
    #False percept measures sum
    
    log['FALSEpercept_SUM'] =  np.where((log['key_trial.keys'] == 'p') & (log['corrAns'] == 'q'),1,np.nan)
    
    log['FALSEpercept_AUDIO'] =  np.where((log['FALSEpercept_SUM'] == 1) & ((log['video'] == 'noise-1.mp4') | (log['video'] == 'noise-2.mp4')),1,np.nan)
    
    log['FALSEpercept_VIDEO'] =  np.where((log['FALSEpercept_SUM'] == 1) & ((log['video'] == 'messenger-video-muted.mp4') | (log['video'] == 'whatsapp-video-muted.mp4')),1,np.nan)
    
    #Check if someone reacted faster than 500ms
    
    log['ReactionUnder500ms'] =  np.where((log['key_trial.rt'] < 0.5 ),1,np.nan)
    
    #mean RT from all trials
    log['meanRT'] = log['key_trial.rt'].mean()
    
    #sum of all correct answers if the stimuli was audible
    
    log['correct_audible'] =  np.where((log['key_trial.corr'] == 1) & (log['video'] == 'messenger-video.mp4') | (log['video'] == 'whatsapp-video.mp4')
                                       | (log['video'] == 'whatsapp-audio.mp4') | (log['video'] == 'messenger-audio.mp4'),1,np.nan)
    
    
    log["SUM_correct_audible"] = log['correct_audible'].sum()
    
    #create output dataframe containing all the relevant information
    
    output = pd.DataFrame(index = (0,))
    
    output['participant'] = log.iloc[0]['participant']
    
    output['FALSEpercept_SUM'] = log['FALSEpercept_SUM'].sum()
    
    output['FALSEpercept_AUDIO'] = log['FALSEpercept_AUDIO'].sum()
    
    output['FALSEpercept_VIDEO'] = log['FALSEpercept_VIDEO'].sum()
    
    output['ReactionsUnder500ms'] = log['ReactionUnder500ms'].sum()
    
    output['meanRT'] = log.iloc[0]['meanRT']
    
    output['correct_audible_SUM'] = log['correct_audible'].sum()
    
    output['missing_responsesSUM'] = log.iloc[0]['missing_responsesSUM']
    
    output['missing_responsesPERCENT'] = log.iloc[0]['missing_responsesPERCENT']
    
    #Append the result with a master dataframe list
    master_list.append(output)
                            
    #save dataframe to excel 
    log.to_excel(directory_to_write + '\\' + str(p)  + 'calculated' + '.xlsx', index = None, header=True)

else:
    pass

#Concat the master_list 
data_master = pd.concat(master_list,ignore_index=True)

#Save the master data to an excel file
data_master.to_excel(directory_to_write + '\\' + 'PPS_results_all.xlsx', index = None, header=True)


#Save the master data to an csv file
data_master.to_csv(directory_to_write + '\\' + 'PPS_results_all.csv', index = None, header=True)


print('Data processing complete!')





