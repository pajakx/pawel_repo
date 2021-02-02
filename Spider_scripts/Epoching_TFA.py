# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 20:03:42 2020

@author: PJ

 _______   ________  ________  ___  ___  ___  ________   ________     
|\  ___ \ |\   __  \|\   ____\|\  \|\  \|\  \|\   ___  \|\   ____\    
\ \   __/|\ \  \|\  \ \  \___|\ \  \\\  \ \  \ \  \\ \  \ \  \___|    
 \ \  \_|/_\ \   ____\ \  \    \ \   __  \ \  \ \  \\ \  \ \  \  ___  
  \ \  \_|\ \ \  \___|\ \  \____\ \  \ \  \ \  \ \  \\ \  \ \  \|\  \ 
   \ \_______\ \__\    \ \_______\ \__\ \__\ \__\ \__\\ \__\ \_______\
    \|_______|\|__|     \|_______|\|__|\|__|\|__|\|__| \|__|\|_______| for TFA
                                                                      
                                                                      
                                                                      
"""
import os, mne, pandas, matplotlib


    ####################
    ## Initialization ##
    ####################

# Main Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\'
print("----> Complete! The filepath is: " + filepath)
# Directory for epoched data
directory_to_write= filepath +"epoched_TFA\\"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the list of subjects you want to analyse
participants = [1]#,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

for participant in participants:
    
    ##Import the preprocessed participant data
    data_ep = mne.io.read_raw_fif(filepath+'preprocessed_auto' +'P'+ str(participant) +'Filtered_1' +'.fif', preload=True)
    
    # Edit event anomalies
    #if participant == 7

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
   
    ##################
    ## Block Epochs ##
    ##################
    
    # Block epochs
    baseline = mne.Epochs(data_ep, events, event_id = event_dict["end_baseline_eyes_open_begin"], 
                          tmin=0, tmax=240, preload=True, baseline= None, reject = None)
    nodis = mne.Epochs(data_ep, events, event_id = event_dict["start_block_Nodis"], 
                      tmin=0, tmax=500, preload=True, baseline= None, reject = None)
    buzz = mne.Epochs(data_ep, events, event_id = event_dict["start_block_Buzz"], 
                      tmin=0, tmax=500, preload=True, baseline= None, reject = None)
    neutral = mne.Epochs(data_ep, events, event_id = event_dict["start_block_Neutral"], 
                      tmin=0, tmax=500, preload=True, baseline= None, reject = None)


    # # Visualize block epochs
    # baseline.plot_image()
    # manual.plot_image()
    # low.plot_image()
    # medium.plot_image()
    # high.plot_image()
    
    # Save block epochs
    
    ## save the data for TFA analysis
    baseline.save(directory_to_write + '\\P'+str(participant)+'_baseline-epo.fif', overwrite=True)
    nodis.save(directory_to_write + '\\P'+str(participant)+'_nodis-epo.fif', overwrite=True)
    buzz.save(directory_to_write + '\\P'+str(participant)+'_buzz-epo.fif', overwrite=True)
    neutral.save(directory_to_write + '\\P'+str(participant)+'_neutral-epo.fif', overwrite=True)

   
   

