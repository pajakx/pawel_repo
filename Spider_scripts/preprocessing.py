# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:57:25 2020

############################
 _______  _______  _______ 
(  ____ \(  ____ \(  ____ \
| (    \/| (    \/| (    \/
| (__    | (__    | |      
|  __)   |  __)   | | ____ 
| (      | (      | | \_  )
| (____/\| (____/\| (___) |
(_______/(_______/(_______)
                           
#############################

@author: PJ
"""
# Import packages
import os
import os.path as op
import numpy as np
import mne
from mne.datasets import sample
#from mne.preprocessing import create_eog_epochs
#from mne_sandbox.preprocessing import eog_regression

#progress bars are cool
print("----> Packages loaded")

# Set a filepath
filepath = 'C:/Users/user/Desktop/FOCUS/'
print("----> Complete! The filepath is: " + filepath)
#subjects with 8 external electrodes
#subjects_pre = [1,2,3,4] #1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,40,41,42,43,44,45,46
## Read the raw data of one participant
subject = ("2") #1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,40,41,42,43,44,45,46
## Read the raw data of one participant


participant = ('P'+subject)
Data_rawEEG = mne.io.read_raw_edf(filepath + participant +'.bdf', preload=True)
    
## Rename and drop channles
Data_rawEEG.drop_channels(['C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
                               'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31',
                               'C32', 'GSR1', 'GSR2', 'Erg1', 'Erg2', 'Resp', 'Plet', 'Temp',
                               'EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6','EXG7', 'EXG8'])
    
Data_rawEEG.rename_channels(mapping={'A1':'Fp1', 'A2':'AF7', 'A3':'AF3', 'A4':'F1', 'A5':'F3', 'A6':'F5', 'A7':'F7',
                                         'A8':'FT7', 'A9':'FC5', 'A10':'FC3', 'A11':'FC1', 'A12':'C1', 'A13':'C3', 'A14':'C5',
                                         'A15':'T7', 'A16':'TP7', 'A17':'CP5', 'A18':'CP3', 'A19':'CP1', 'A20':'P1', 'A21':'P3',                                     
                                         'A22':'P5', 'A23':'P7', 'A24':'P9', 'A25':'PO7', 'A26':'PO3', 'A27':'O1', 'A28':'Iz',
                                         'A29':'Oz', 'A30':'POz', 'A31':'Pz', 'A32':'CPz', 'B1':'Fpz', 'B2':'Fp2', 'B3':'AF8',                                  
                                         'B4':'AF4', 'B5':'AFz', 'B6':'Fz', 'B7':'F2', 'B8':'F4', 'B9':'F6', 'B10':'F8', 
                                         'B11':'FT8', 'B12':'FC6', 'B13':'FC4', 'B14':'FC2', 'B15':'FCz', 'B16':'Cz', 'B17':'C2',                                 
                                         'B18':'C4', 'B19':'C6', 'B20':'T8', 'B21':'TP8', 'B22':'CP6', 'B23':'CP4', 'B24':'CP2',  
                                         'B25':'P2', 'B26':'P4', 'B27':'P6', 'B28':'P8', 'B29':'P10', 'B30':'PO8', 'B31':'PO4',
                                         'B32':'O2','C1':'mastoidleft', 'C2':'mastoidright', 'C3':'HEOGleft','C4':'HEOGright',
                                         'C5':'VEOGup', 'C6':'VEOGdown','Status':'triggers'})

#VEOG< HEOG setup
Data_rawEEG = mne.set_bipolar_reference(Data_rawEEG,anode='VEOGup',cathode='VEOGdown',ch_name='VEOG')
Data_rawEEG = mne.set_bipolar_reference(Data_rawEEG,anode='HEOGleft',cathode='HEOGright',ch_name='HEOG')
    
Data_rawEEG.set_channel_types({'VEOG':'eog','HEOG':'eog'})

# Setting channel montage
montage = mne.channels.read_montage('biosemi64')
Data_rawEEG.set_montage(montage)

## Setting EEG reference
Data_rawEEG.set_eeg_reference(['mastoidleft','mastoidright'])

Data_rawEEG.drop_channels(['mastoidleft','mastoidright'])

print(Data_rawEEG.info['bads'])

##Make o copy of the raw data

Data_raw_copy= Data_rawEEG


## Filter on data
low_f = 1#Low edge of the high-pass filter
high_f = 30 #High edge of the low-pass filter
picks_eeg_eog = mne.pick_types(Data_rawEEG.info, meg=False, eeg=True, eog=True) #select the eeg and the eog channels for filtering
Data_Filtered = Data_rawEEG.filter(low_f, high_f, method='iir', l_trans_bandwidth='auto', filter_length='auto', phase='zero', picks=picks_eeg_eog)

"""
    #############
    ###TARGETS###
    #############
    
#target number epochs
trig_number_nodis = epochs['nodis_target_number'].average(picks=['POz'])
trig_number_buzz = epochs['buzz_target_number'].average(picks=['POz'])
trig_number_neutral = epochs['neutral_target_number'].average(picks=['POz'])
    
#Combine epochs for plotting
all_evokeds_targets = [trig_number_nodis, trig_number_buzz, trig_number_neutral]
    
#Plot the different conditions target numbers parietal
ylength = dict(eeg=[-12, 12])
mne.viz.plot_compare_evokeds(dict(neutral=trig_number_neutral, buzz=trig_number_buzz, nodis=trig_number_nodis), legend=True, title='target numbers parietal',noise_cov=noise_cov)



##########################
### ICA decomposition ###
#########################

from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,
                               corrmap)

ica = ICA(n_components=15, random_state=97)
ica.fit(Data_Filtered)

ica.plot_sources(Data_raw_copy)

# blinks
ica.plot_overlay(Data_raw_copy, exclude=['VEOG'], picks='eeg')
# horizontal eye movement
ica.plot_overlay(Data_raw_copy, exclude=['HEOG'], picks='eeg')

### EXCLUDING BASED ON EOG CHANNEL ###


ica.exclude = []
# find which ICs match the EOG pattern
eog_indices, eog_scores = ica.find_bads_eog(Data_raw_copy)
ica.exclude = eog_indices

# barplot of ICA component "EOG match" scores
ica.plot_scores(eog_scores)

# plot diagnostics
ica.plot_properties(Data_raw_copy, picks=eog_indices)

# plot ICs applied to raw data, with EOG matches highlighted
ica.plot_sources(Data_raw_copy)

# plot ICs applied to the averaged EOG epochs, with EOG matches highlighted
ica.plot_sources(eog_evoked)

print(ica.exclude)
ica.apply(Data_raw_copy)
Data_raw_copy.plot()
#eog_epochs = mne.preprocessing.create_eog_epochs(Data_Filtered)
#eog_epochs.plot_image(combine='mean')
#eog_epochs.average().plot_joint()

events = mne.find_events(Data_Filtered)

"""

#check for unusal frequencies
Data_Filtered.plot_psd(fmax=60); # Frequency domain --> check for line noise or unusual frequencies

#manually marking noisy channels
Data_Filtered.info['bads'].extend(['T8','T7','FC5'])

## noisy channels interpolation: 
   
Data_Filtered.info['bads']
Data_Filtered.interpolate_bads(reset_bads=True)
  
Data_Filtered.plot_psd(fmax=60); # Frequency domain --> check for line noise or unusual frequencies
## save the data for ERP
Data_Filtered.save(r'C:\Users\user\Desktop\FOCUS\Preprocessed_ERP/' + participant + '_Filtered_0.1Hz.fif')

## save the data for TFD
Data_Filtered.save(r'C:\Users\user\Desktop\FOCUS\Preprocessed_TimeFreqDom/' + participant + '_Filtered_1Hz.fif')