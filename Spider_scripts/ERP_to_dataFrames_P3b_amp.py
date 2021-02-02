# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:02:41 2020

 _________________                                     
|  ___| ___ \ ___ \                                    
| |__ | |_/ / |_/ /                                    
|  __||    /|  __/                                     
| |___| |\ \| |                                        
\____/\_| \_\_|                                        
                                                       
                                                       
 _                                                     
| |                                                    
| |_ ___                                               
| __/ _ \                                              
| || (_) |                                             
 \__\___/                                              
                                                       
                                                       
______      _       ______                             
|  _  \    | |      |  ___|                            
| | | |__ _| |_ __ _| |_ _ __ __ _ _ __ ___   ___  ___ 
| | | / _` | __/ _` |  _| '__/ _` | '_ ` _ \ / _ \/ __|
| |/ / (_| | || (_| | | | | | (_| | | | | | |  __/\__ \
|___/ \__,_|\__\__,_\_| |_|  \__,_|_| |_| |_|\___||___/
                                                       
P3b amplitude

@author: Paweł Jakuszyk
"""
import os
import seaborn as sns
import mne
import pandas


    ####################
    ## Initialization ##
    ####################

# Main Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\raw_data\\preprocessed_auto\\'
print("----> Complete! The filepath is: " + filepath)

# Directory for epoched data
directory_to_write= filepath +"epoched_ERP"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)
directory_plots= filepath +"ERP_plots"
if not os.path.exists(directory_plots):
    os.makedirs(directory_plots)
    
# Enter the list of subjects you want to analyse
participants = [1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

#Define a master list for dataframes of all the amplitude values
master_list = []

for participant in participants:
    
    ##Import the preprocessed participant data
    data_ep = mne.io.read_raw_fif(filepath +'P'+ str(participant) +'Filtered_0.1' +'.fif', preload=True)
    participantId = ["P" + str(participant)] 
    # Edit event anomalies
    #if participant == 7: # Subject 8: insert event at first sample-point
        #events[0] = [0,0,11]

    ##Read in the events
    events = mne.find_events(data_ep, shortest_event=1)
    

    
    ## Specify event codes of interest with descriptive labels.
    event_dict = {
              'target_number_block_Nodis' : 51, 
              'target_number_block_Neutral' : 56, 
              'target_number_block_Buzz' : 57, 
              'target_sound_neutral' : 52,
              'target_sound_buzz' : 53, 
              'start_block_Nodis' : 65,
              'end_block_Nodis' : 66, 
              'start_block_Buzz' : 67, 
              'end_block_Buzz' : 68, 
              'start_block_Neutral' : 69,
              'end_block_Neutral' : 70, 
              'end_baseline_eyes_open_begin' : 54, 
              'end_baseline_eyes_open_stop' : 73, 
              'end_baseline_eyes_closed_begin' : 74,
              'end_baseline_eyes_closed_stop' : 55 
              }

    ###Create epochs 
    epochs_ERP = mne.Epochs(data_ep, events, event_id=event_dict, tmin=-0.2, tmax=0.8,
                        baseline=(None, 0), preload=True, reject = dict(eeg=150e-6))
    
    
    ###Converting epochs to a datafame
    df = epochs_ERP.to_data_frame()
    df.iloc[:5, :10]
    
    
    #############
    ###TARGETS###
    #############
    
    #target number epochs avareged
    trig_number_nodis = epochs_ERP['target_number_block_Nodis'].average()
    trig_number_buzz = epochs_ERP['target_number_block_Buzz'].average()
    trig_number_neutral = epochs_ERP['target_number_block_Neutral'].average()
    
    #load the averaged epochs into dataframes
    df_target_nodis = trig_number_nodis.to_data_frame()
    df_target_buzz = trig_number_buzz.to_data_frame()
    df_target_neutral = trig_number_neutral.to_data_frame()
    
    #select time window for max amplitude from 300ms to 600ms
    data_nodis = df_target_nodis[['Pz']].loc[ 300 : 600 , : ]
    data_buzz = df_target_buzz[['Pz']].loc[ 300 : 600 , : ]
    data_neutral = df_target_neutral[['Pz']].loc[ 300 : 600 , : ]
    
    #pick the max amplitude in given time window
    data_ready_nodis = data_nodis.max()
    data_ready_buzz = data_buzz.max()
    data_ready_neutral = data_neutral.max()
    
    #Convert series to dataframe, rename the amplitude column, 
    ##add a column with participant info,reindex to 0
    
    ##for block nodis
    df_nodis = pandas.DataFrame(data_ready_nodis)
    df_nodis = df_nodis.rename(columns={0: "Target_Block_Nodis_maxAmp_Pz"})
    df_nodis['participant'] = participantId 
    df_nodis = df_nodis.rename(index={'Pz':0})
    ##for block buzz
    df_buzz = pandas.DataFrame(data_ready_buzz)
    df_buzz = df_buzz.rename(columns={0: "Target_Block_Buzz_maxAmp_Pz"})
    df_buzz['participant'] = participantId 
    df_buzz = df_buzz.rename(index={'Pz':0})
    #for block neutral
    df_neutral = pandas.DataFrame(data_ready_neutral)
    df_neutral = df_neutral.rename(columns={0: "Target_Block_Neutral_maxAmp_Pz"})
    df_neutral['participant'] = participantId 
    df_neutral = df_neutral.rename(index={'Pz':0})
    
    
    #Concat the result of 3 blocks into 1 dataframe with shared column with participant ID
    result = pandas.concat([df_nodis.set_index('participant'),df_buzz.set_index('participant'),
                   df_neutral.set_index('participant')], axis=1, join='inner').reset_index()
    
    #Append the result with a master dataframe list
    master_list.append(result)


#Concat the master_list 
data_max_amplitudes_targets = pandas.concat(master_list,ignore_index=True)

#Save dataframe to csv file

data_max_amplitudes_targets.to_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\max_amp_targets.csv', index = None, header=True)

# Note also that, by default, channel measurement values are scaled so that EEG
# data are converted to μV, magnetometer data are converted to fT, and
# gradiometer data are converted to fT/cm.
# By default, time values are converted from seconds to milliseconds and
# then rounded to the nearest integer;
        