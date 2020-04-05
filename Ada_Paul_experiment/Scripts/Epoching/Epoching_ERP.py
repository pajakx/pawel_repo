# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 13:50:28 2020

@author: PJ


 _______   ________  ________  ________  ___  ___  ___  ________   ________     
|\  ___ \ |\   __  \|\   __  \|\   ____\|\  \|\  \|\  \|\   ___  \|\   ____\    
\ \   __/|\ \  \|\  \ \  \|\  \ \  \___|\ \  \\\  \ \  \ \  \\ \  \ \  \___|    
 \ \  \_|/_\ \   ____\ \  \\\  \ \  \    \ \   __  \ \  \ \  \\ \  \ \  \  ___  
  \ \  \_|\ \ \  \___|\ \  \\\  \ \  \____\ \  \ \  \ \  \ \  \\ \  \ \  \|\  \ 
   \ \_______\ \__\    \ \_______\ \_______\ \__\ \__\ \__\ \__\\ \__\ \_______\
    \|_______|\|__|     \|_______|\|_______|\|__|\|__|\|__|\|__| \|__|\|_______|
    for ERP
                                                                      
                                                                      
                                                                      
"""
#!pip install -U autoreject
import os, mne, pandas, matplotlib
from autoreject import AutoReject
from autoreject import get_rejection_threshold

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

for participant in participants:
    
    ##Import the preprocessed participant data
    data_ep = mne.io.read_raw_fif(filepath +'P'+ str(participant) +'Filtered_0.1' +'.fif', preload=True)
    
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
    '''
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
    '''
    
    ###Create epochs 
    epochs_ERP = mne.Epochs(data_ep, events, event_id=event_dict, tmin=-0.2, tmax=0.8,
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
    trig_number_nodis = epochs_ERP['target_number_block_Nodis'].average()
    trig_number_buzz = epochs_ERP['target_number_block_Buzz'].average()
    trig_number_neutral = epochs_ERP['target_number_block_Neutral'].average()
    
    
    #Combine epochs for plotting
    all_evokeds_targets = [trig_number_nodis, trig_number_buzz, trig_number_neutral]
    
 
    #Plot the different conditions target numbers parietal
    ylength = dict(eeg=[-12, 12])
    plot_targets = mne.viz.plot_compare_evokeds(
            dict(neutral=trig_number_neutral, buzz=trig_number_buzz, nodis=trig_number_nodis),
            legend=True, title='target numbers parietal P_'+ str(participant),picks=['Pz'])
     #Save plots to a designated diretory
    #plot_targets.save(directory_plots+'P'+ str(participant) + 'ERP_plot.png', overwrite=True)
                                                            
  
    ##############
    ####SOUNDS####
    ##############
    
    
    trig_sound_buzz = epochs_ERP['target_sound_buzz'].average()
    trig_sound_neutral = epochs_ERP['target_sound_neutral'].average()
    
    all_evokeds_sounds = [trig_sound_buzz, trig_sound_neutral]
    
    #Plot the different conditions sounds parietal
    ylength = dict(eeg=[-12, 12])
    mne.viz.plot_compare_evokeds(dict(neutral=trig_sound_neutral, buzz=trig_sound_buzz),
    legend=True, title='P_'+ str(participant) +'_sounds central', picks=['Cz'])
    
    '''
    
    ### Save the data for ERP analysis
    epochs_ERP.save(directory_to_write + '\\P'+str(participant)+'_ERP-epo_ERP.fif')
    
    #trig_number_nodis.save(directory_to_write + '\\P'+str(participant)+'_nodis-epo_ERP.fif')
    #trig_number_buzz.save(directory_to_write + '\\P'+str(participant)+'_buzz-epo_ERP.fif')
    #trig_number_neutral.save(directory_to_write + '\\P'+str(participant)+'_neutral-epo_ERP.fif')
    '''