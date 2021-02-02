# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:37:27 2020
__                                    
| |_(_)_ __ ___   ___                     
| __| | '_ ` _ \ / _ \                    
| |_| | | | | | |  __/                    
 \__|_|_| |_| |_|\___|                    
                                          
  __                                      
 / _|_ __ ___  __ _  ___ _ __   ___ _   _ 
| |_| '__/ _ \/ _` |/ _ \ '_ \ / __| | | |
|  _| | |  __/ (_| |  __/ | | | (__| |_| |
|_| |_|  \___|\__, |\___|_| |_|\___|\__, |
                 |_|                |___/ 
     _                       _            
  __| | ___  _ __ ___   __ _(_)_ __       
 / _` |/ _ \| '_ ` _ \ / _` | | '_ \      
| (_| | (_) | | | | | | (_| | | | | |     
 \__,_|\___/|_| |_| |_|\__,_|_|_| |_|     
                                          


@author: Paweł Jakuszyk
"""
import os, mne, numpy
from mne.time_frequency import tfr_morlet, psd_multitaper
##############################
## Create lists for epochs  ##
##############################

baseline_freq = []
nodis_freq = []
buzz_freq = []
neutral_freq = []



    ####################
    ## Initialization ##
    ####################

# Main Directory 
filepath = r'C:\Users\user\Desktop\FOCUS\epoched_TFA'
print("----> Complete! The filepath is: " + filepath)
# Directory for epoched data
directory_to_write= filepath + "\analysis\"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the list of subjects you want to analyse
participants = [1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

for participant in participants:
  
########################
## Frequency Analysis ##
########################

    # Importing Epoched Data
    baseline_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_baseline-epo.fif', preload=True)
    nodis_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_nodis-epo.fif', preload=True)
    buzz_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_buzz-epo.fif', preload=True)
    neutral_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_neutral-epo.fif', preload=True)
   
    baseline_freq.append(baseline_epoch)
    nodis_freq.append(nodis_epoch)
    buzz_freq.append(buzz_epoch)
    neutral_freq.append(neutral_epoch)

###Combine a list of epochs into one epochs object
baseline_combined = mne.concatenate_epochs(baseline_freq)
nodis_combined = mne.concatenate_epochs(nodis_freq)
buzz_combined = mne.concatenate_epochs(buzz_freq)
neutral_combined = mne.concatenate_epochs(neutral_freq)


###Plot frequencies

baseline_combined.plot_psd_topomap()
nodis_combined.plot_psd_topomap()
buzz_combined.plot_psd_topomap()
neutral_combined.plot_psd_topomap()

baseline_combined.plot_psd(fmin=2., fmax=30.)
nodis_combined.plot_psd(fmin=2., fmax=30.)
buzz_combined.plot_psd(fmin=2., fmax=30.)
neutral_combined.plot_psd(fmin=2., fmax=30.)

print(baseline_freq)



parietal = ['Pz', 'POz', 'CPz', 
            'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10',
            'CP1', 'CP2', 'CP3', 'CP4', 'CP5', 'CP6',
            'PO3', 'PO4', 'PO7', 'PO8']
parietal_min = ['Pz', 'POz', 'CPz', 'P1', 'P2'] 
baseline_combined.plot_psd(picks = parietal_min, fmax = 15, fmin = 5, average = True, bandwidth = 1)
nodis_combined.plot_psd(picks = parietal_min, fmax = 15, fmin = 5, average = True, bandwidth = 1)
buzz_combined.plot_psd(picks = parietal_min, fmax = 15, fmin = 5, average = True, bandwidth = 1)
neutral_combined.plot_psd(picks = parietal_min, fmax = 15, fmin = 5, average = True, bandwidth = 1)


##define frequencies of interest (log-spaced)
freqs = numpy.logspace(*numpy.log10([6, 35]), num=8)
n_cycles = freqs / 2.  # different number of cycle per frequency
power, itc = tfr_morlet(baseline_combined, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1)



power.plot(['POz'], baseline=(-0.5, 0), mode='logratio', title=power.ch_names['POz'])

#Save concat epochs data
baseline_combined.save(filepath +'_concat_baseline.fif', overwrite=True)
nodis_combined.save(filepath +'_concat_nodis.fif', overwrite=True)
buzz_combined.save(filepath +'_concat_buzz.fif', overwrite=True)
neutral_combined.save(filepath +'_concat_neutral.fif', overwrite=True)
