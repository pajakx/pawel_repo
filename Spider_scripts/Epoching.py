# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 13:50:28 2020

@author: PJ

 _______   ________  ________  ___  ___  ___  ________   ________     
|\  ___ \ |\   __  \|\   ____\|\  \|\  \|\  \|\   ___  \|\   ____\    
\ \   __/|\ \  \|\  \ \  \___|\ \  \\\  \ \  \ \  \\ \  \ \  \___|    
 \ \  \_|/_\ \   ____\ \  \    \ \   __  \ \  \ \  \\ \  \ \  \  ___  
  \ \  \_|\ \ \  \___|\ \  \____\ \  \ \  \ \  \ \  \\ \  \ \  \|\  \ 
   \ \_______\ \__\    \ \_______\ \__\ \__\ \__\ \__\\ \__\ \_______\
    \|_______|\|__|     \|_______|\|__|\|__|\|__|\|__| \|__|\|_______| for ERP
                                                                      
                                                                      
                                                                      
"""
!pip install -U autoreject
import os, mne, pandas, matplotlib
from autoreject import AutoReject
from autoreject import get_rejection_threshold

    ####################
    ## Initialization ##
    ####################

# Main Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\Preprocessed_ERP\\'
print("----> Complete! The filepath is: " + filepath)
# Directory for epoched data
directory_to_write= filepath +"/epoched_ERP"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the list of subjects you want to analyse
participants = [1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

for participant in participants:
    
    ##Import the preprocessed participant data
    data_ep = mne.io.read_raw_fif(filepath +'P'+ str(participant) +'_Filtered_0.1Hz' +'.fif', preload=True)
    
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
   #'start_baseline_eyes_open_begin': 49,  'start_baseline_eyes_open_stop': 71 'start_baseline_eyes_closed_begin': 72,
    # # Visualizing events
    # fig = mne.viz.plot_events(events, sfreq=raw.info['sfreq'],
    #                           first_samp=raw.first_samp, event_id = event_dict)
    # fig.subplots_adjust(right=0.7)
    
    # Transform to pandas dataframe for easier data extraction
    events_df = pandas.DataFrame(data = events) 
    events_df.columns = ['time','drop', 'event']
    events_df.drop('drop', axis=1, inplace=True)
    events_df['time'] /= data_ep.info['sfreq'] # convert sample to timepoint in seconds
    
    
    ###Create epochs 
    epochs = mne.Epochs(data_ep, events, event_id=event_dict, tmin=-0.2, tmax=0.8,
                        baseline=(None, 0), preload=True, reject = dict(eeg=150e-6)) # V (EEG channels))
    #epochs.plot_drop_log()
 
    ###AUTOREJECT
    
    #ar = AutoReject()
    #epochs_clean = ar.fit_transform(epochs)
    
    #reject = get_rejection_threshold(epochs)  
    
    
    
    #############
    ###TARGETS###
    #############
    
    #target number epochs
    trig_number_nodis = epochs_clean['nodis_target_number'].average(picks=['POz'])
    trig_number_buzz = epochs_clean['buzz_target_number'].average(picks=['POz'])
    trig_number_neutral = epochs_clean['neutral_target_number'].average(picks=['POz'])
    
    #Combine epochs for plotting
    all_evokeds_targets = [trig_number_nodis, trig_number_buzz, trig_number_neutral]
    
    #Plot the different conditions target numbers parietal
    ylength = dict(eeg=[-12, 12])
    mne.viz.plot_compare_evokeds(dict(neutral=trig_number_neutral, buzz=trig_number_buzz, nodis=trig_number_nodis), legend=True, title='target numbers parietal')
   
    ##############
    ####SOUNDS####
    ##############
    
    
    #trig_buzz_parietal = epochs[52].average(picks=['POz'])
    #trig_neutral_parietal = epochs[53].average(picks=['POz'])
    
    #all_evokeds_sounds = [trig_buzz_parietal, trig_neutral_parietal]
    
    #Plot the different conditions sounds parietal
    #ylength = dict(eeg=[-12, 12])
    #mne.viz.plot_compare_evokeds(dict(neutral=trig_neutral_parietal, buzz=trig_buzz_parietal), legend=True, title='sounds parietal')