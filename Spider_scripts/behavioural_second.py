# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 18:07:43 2020
 _          _                 _                       _ 
| |        | |               (_)                     | |
| |__   ___| |__   __ ___   ___  ___  _   _ _ __ __ _| |
| '_ \ / _ \ '_ \ / _` \ \ / / |/ _ \| | | | '__/ _` | |
| |_) |  __/ | | | (_| |\ V /| | (_) | |_| | | | (_| | |
|_.__/ \___|_| |_|\__,_| \_/ |_|\___/ \__,_|_|  \__,_|_|
                                                        
                                                        
                              _                         
                             | |                        
 ___  ___  ___ ___  _ __   __| |                        
/ __|/ _ \/ __/ _ \| '_ \ / _` |                        
\__ \  __/ (_| (_) | | | | (_| |                        
|___/\___|\___\___/|_| |_|\__,_|                        
                                                        
                                                        
       _   _                       _                    
      | | | |                     | |                   
  __ _| |_| |_ ___ _ __ ___  _ __ | |_                  
 / _` | __| __/ _ \ '_ ` _ \| '_ \| __|                 
| (_| | |_| ||  __/ | | | | | |_) | |_                  
 \__,_|\__|\__\___|_| |_| |_| .__/ \__|                 
                            | |                         
                            |_|                         

@author: Paweł Jakuszyk
"""
import pandas as pd
import numpy as np
import os as os



   ####################
   ## Initialization ##
   ####################

# Main Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\behavioral\\'
print("----> Complete! The filepath is: " + filepath)

# Directory for ready data
directory_to_write= filepath +"ready_to_stat\\"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)
#Create empty masterlists for wide a long format to concat later
    
master_long =[]
master_wide = []


# Enter the list of subjects you want to analyse
participants = [1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

for participant in participants:
    
    ##Import the preprocessed participant data
    data = pd.read_csv(filepath +'P'+ str(participant)+'.csv')
    data = data[['participant','sounds','blocks','corrAns','key_resp_trial.keys','number','key_resp_trial.corr','key_resp_trial.rt']]
    data = data.rename(columns={"key_resp_trial.corr": "key_resp_corr", "key_resp_trial.rt": "key_resp_rt",'key_resp_trial.keys':'key_resp_key'})
    data = data.replace(
        
        
   ['sounds/buzz.wav', 'sounds/neutral.wav', 'sounds/silence.wav',
    'conditions_CPT_60_neutral.xlsx','conditions_CPT_60_buzz.xlsx',
    'conditions_CPT_60_nodis.xlsx'],
                                  
   ['buzz','neutral', 'silence','neutral_block','buzz_block','nodis_block']
   
   
   )
   
    #Set participant id variable
    participantId = ("P" + str(participant)) 
    
    
    #####################
    #Calculate variables#
    #####################
    
    
  
    ####Calculate mean corret rt time per block####
    
    
    # Adding variable
    df_corr = data.loc[(data.corrAns == 'space') & (data.key_resp_corr == 1), ['key_resp_rt']]
    #adding a new clumn with desired variable
    data['corr_rt'] = df_corr
    #pick the desired columns
    data_mean_rt = data[['blocks','corr_rt']]
    #groupby/calculate mean for correct rt per block
    data_mean_rt = data_mean_rt.groupby('blocks').mean()
    #drop column from index
    data_mean_rt = data_mean_rt.reset_index()
    #add a participant column with the current participant number(fucked up way I know)
    data_mean_rt['participant']= pd.Series(participantId)
    data_mean_rt=data_mean_rt.fillna({'participant': participantId})
    #now we have data in a long format it would be nice to append it to a master list
    master_long.append(data_mean_rt)
    
    # reshape from long to wide in pandas python
    data_mean_rt_wide =data_mean_rt.pivot(index = 'participant',columns='blocks', values='corr_rt')
    data_mean_rt_wide = data_mean_rt_wide.reset_index()
    data_mean_rt_wide = data_mean_rt_wide.rename(columns=
                        {"neutral_block": "neutral_block_mean_rt", 
                         "buzz_block": "buzz_block_mean_rt",
                         'nodis_block':'nodis_block_mean_rt'})
    
    
    ####Calculate omission error per block####
    
    #omission error create a variable
    data.loc[(data.number == 3) & (data.key_resp_corr == 0),'om_err'] = 1
    #pick the desired columns
    data_omission = data[['blocks','om_err']]
    #Fill in Nan values in omission error (0)
    data_omission=data_omission.fillna({'om_err':0})
    #groupby/calculate mean for omissioin error per block
    data_omission = data_omission.groupby('blocks').mean()
    #drop column from index
    data_omission = data_omission.reset_index()
    #add a participant column with the current participant number(fucked up way I know)
    data_omission['participant']= pd.Series(participantId)
    data_omission=data_omission.fillna({'participant': participantId})
    #now we have data in a long format it would be nice to append it to a master list
    master_long.append(data_omission)
    
    # reshape from long to wide in pandas python
    data_omission_wide =data_omission.pivot(index = 'participant',columns='blocks', values='om_err')
    data_omission_wide = data_omission_wide.reset_index()
    data_omission_wide = data_omission_wide.rename(columns=
                        {"neutral_block": "neutral_block_omission", 
                         "buzz_block": "buzz_block_mean_omission",
                         'nodis_block':'nodis_block_mean_omission'})

    
    ####Calculate false alarms per block####
    
    #false alarm create a variable
    data.loc[(data.number != 3) & (data.key_resp_key == 'space'),'false_alarm'] = 1
    #pick the desired columns
    data_alarm = data[['blocks','false_alarm']]
    #Fill in Nan values in false alarm (0)
    data_alarm=data_alarm.fillna({'false_alarm':0})
    #groupby/calculate mean for omissioin error per block
    data_alarm = data_alarm.groupby('blocks').mean()
    #drop column from index
    data_alarm = data_alarm.reset_index()
    #add a participant column with the current participant number(fucked up way I know)
    data_alarm['participant']= pd.Series(participantId)
    data_alarm=data_alarm.fillna({'participant': participantId})
    #now we have data in a long format it would be nice to append it to a master list
    master_long.append(data_alarm)
    
    # reshape from long to wide in pandas python
    data_alarm_wide =data_alarm.pivot(index = 'participant',columns='blocks', values='false_alarm')
    data_alarm_wide = data_alarm_wide.reset_index()
    data_alarm_wide = data_alarm_wide.rename(columns=
                        {"neutral_block": "neutral_block_falsAlarm", 
                         "buzz_block": "buzz_block_mean_falsAlarm",
                         'nodis_block':'nodis_block_mean_falsAlarm'})
    
  
    #Concat the result of 3 variables into 1 dataframe with shared column with participant ID
    result = pd.concat([data_mean_rt_wide.set_index('participant'),data_omission_wide.set_index('participant'),
                   data_alarm_wide.set_index('participant')], axis=1, join='inner').reset_index()
    
    #wide format appending to second master list
    master_wide.append(result)
    
#Concat the master_lists
data_behavioural_long = pd.concat(master_long,ignore_index=True)
data_behavioural_wide = pd.concat(master_wide,ignore_index=True)
#Save dataframes to csv files

data_behavioural_long.to_csv(directory_to_write+'data_behavioural_long.csv')
data_behavioural_wide.to_csv(directory_to_write+'data_behavioural_wide.csv',header=True)

   
    