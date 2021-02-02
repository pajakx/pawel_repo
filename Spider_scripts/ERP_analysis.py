# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:31:50 2020
 _________________                     _           _     
|  ___| ___ \ ___ \                   | |         (_)    
| |__ | |_/ / |_/ /   __ _ _ __   __ _| |_   _ ___ _ ___ 
|  __||    /|  __/   / _` | '_ \ / _` | | | | / __| / __|
| |___| |\ \| |     | (_| | | | | (_| | | |_| \__ \ \__ \
\____/\_| \_\_|      \__,_|_| |_|\__,_|_|\__, |___/_|___/
                                          __/ |          
                                         |___/           

@author: Paweł Jakuszyk
"""
import os, mne
import numpy as np
import matplotlib.pyplot as plt
from mne.time_frequency import tfr_morlet, psd_multitaper

##############################
## ERP to targets per block ##
##############################

target_nodis = []
target_buzz = []
target_neutral = []
sound_neutral =[]
sound_buzz =[]



    ####################
    ## Initialization ##
    ####################

# Main Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\Preprocessed_ERP\\epoched_ERP\\'
print("----> Complete! The filepath is: " + filepath)
# Directory for epoched data
directory_to_write= filepath +"epoched_TFA"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the list of subjects you want to analyse
participants = [1,]#2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

for participant in participants:
    
    ##Import the epochs
    epochs = mne.read_epochs(filepath + '\\P'+str(participant)+'_ERP-epo_ERP.fif',preload=True)
    
    ## Selecting relevant epochs  
    nodis = epochs['target_number_block_Nodis']
    buzz= epochs['target_number_block_Buzz']
    neutral = epochs['target_number_block_Neutral']
    s_neutral = epochs['target_sound_neutral']
    s_buzz = epochs['target_sound_buzz']
    
    ## And appending them to list
    target_nodis.append(nodis.average())
    target_buzz.append(buzz.average())
    target_neutral.append(neutral.average())
    sound_neutral.append(s_neutral.average())
    sound_buzz.append(s_buzz.average())

## Create grand average
target_nodis_grand = mne.grand_average(target_nodis)
target_buzz_grand = mne.grand_average(target_buzz)
target_neutral_grand = mne.grand_average(target_neutral)
sound_neutral_grand = mne.grand_average(sound_neutral)
sound_buzz_grand = mne.grand_average(sound_buzz)

# # Visualize grand averages
target_nodis_grand.plot_joint(title='Grand Average Nodis')
target_buzz_grand.plot_joint(title='Grand Average Buzz')
target_neutral_grand.plot_joint(title='Grand Average Neutral')
sound_neutral_grand.plot_joint(title='Grand Average Sound Neutral')
sound_buzz_grand.plot_joint(title='Grand Average Sound Buzz')


##PLots to compare conditions and different electrodes

##For blocks P3b
mne.viz.plot_compare_evokeds(dict(buzz=target_buzz_grand, nodis=target_nodis_grand,
                                  neutral=target_neutral_grand),
                              legend='upper left', show_sensors='upper right',
                              picks = ['Pz'], title="Grand Average Targets Pz")
  
mne.viz.plot_compare_evokeds(dict(buzz=target_buzz_grand, nodis=target_nodis_grand,
                                  neutral=target_neutral_grand),
                              legend='upper left', show_sensors='upper right',
                              picks = ['Cz'], title="Grand Average Targets Cz")  
  
mne.viz.plot_compare_evokeds(dict(buzz=target_buzz_grand, nodis=target_nodis_grand,
                                  neutral=target_neutral_grand),
                              legend='upper left', show_sensors='upper right',
                              picks = ['POz'], title="Grand Average Targets POz")  
  
  
  
##For sounds P3a
mne.viz.plot_compare_evokeds(dict(buzz=sound_buzz_grand,  neutral=sound_neutral_grand),
                              legend='upper left', show_sensors='upper right',
                              picks = ['Pz'], title="Grand Average Sounds Pz")

mne.viz.plot_compare_evokeds(dict(buzz=sound_buzz_grand,  neutral=sound_neutral_grand),
                              legend='upper left', show_sensors='upper right',
                              picks = ['POz'], title="Grand Average Sounds POz")

mne.viz.plot_compare_evokeds(dict(buzz=sound_buzz_grand,  neutral=sound_neutral_grand),
                              legend='upper left', show_sensors='upper right',
                              picks = ['Cz'], title="Grand Average Sounds Cz")

##For sounds frontal P3a

mne.viz.plot_compare_evokeds(dict(buzz=sound_buzz_grand,  neutral=sound_neutral_grand),
                              legend='upper left', show_sensors='upper right',
                              picks = ['Fz'], title="Grand Average Sounds Fz")
