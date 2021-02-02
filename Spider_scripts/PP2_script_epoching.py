# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 10:20:07 2020

@author: Paweł Jakuszyk
"""



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import mne
import glob
import pickle
from tqdm import tqdm
from scipy import stats
from scipy import signal 
from matplotlib import cm


Data_rawEEG = mne.io.read_raw_bdf(r'C:\Users\user\Desktop\FOCUS\P1.bdf', preload=True)

print(Data_rawEEG.info)

## Rename channels: only 73 relevant ones
Data_rawEEG.drop_channels(['C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
                               'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31',
                               'C32', 'EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7', 'EXG8', 'GSR1', 'GSR2', 'Erg1', 'Erg2', 'Resp', 'Plet', 'Temp'])
    
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
Data_rawEEG.plot()

#VEOG< HEOG setup
Data_rawEEG = mne.set_bipolar_reference(Data_rawEEG,anode='VEOGup',cathode='VEOGdown',ch_name='VEOG')
Data_rawEEG = mne.set_bipolar_reference(Data_rawEEG,anode='HEOGleft',cathode='HEOGright',ch_name='HEOG')
    
Data_rawEEG.set_channel_types({'VEOG':'eog','HEOG':'eog'})

## Setting EEG reference
Data_rawEEG.set_eeg_reference(['mastoidleft','mastoidright'])

Data_rawEEG.drop_channels(['mastoidleft','mastoidright'])

## Filter on data
low_f = 0.1 #Low edge of the high-pass filter
high_f = 30 #High edge of the low-pass filter
picks_eeg_eog = mne.pick_types(Data_rawEEG.info, meg=False, eeg=True, eog=True) #select the eeg and the eog channels for filtering

Data_Filtered = Data_rawEEG.filter(low_f, high_f, method='iir', l_trans_bandwidth='auto', filter_length='auto', phase='zero', picks=picks_eeg_eog)
Data_Filtered.plot()

## Read and set Biosemi64 montage
montage = mne.channels.make_standard_montage('biosemi64')
Data_rawEEG.set_montage(montage, raise_if_subset=False)
montage.plot(show_names=True)
    #print(Data_rawEEG.info['chs'][0]['loc'])
Data_rawEEG.plot_sensors('3d')


#manually marking noisy channels
Data_Filtered.info['bads'].extend(['P7','O2','PO4','PO8','FC1','C3','POz','Fz','F1','FC1','CPz'])

## noisy channels interpolation: 
   
Data_Filtered.info['bads']
Data_Filtered.interpolate_bads(reset_bads=True)
    
Data_Filtered.plot_psd(fmax=60); # Frequency domain --> check for line noise or unusual frequencies

raw = Data_Filtered

#Epoching and averaging (ERP/ERF)
import os.path as op

events = mne.find_events(Data_Filtered)

#start_block_nodis =  mne.pick_events(events, include=65)
plot = mne.viz.plot_events(events, sfreq=Data_Filtered.info['sfreq'])
#raw.plot(events=start_block_Nodis)



plot.subplots_adjust(right=0.7)  # make room for the legend

#choose electrode
pick_parietal = ['POz','Pz'] 
pick_frontal = ['Fpz']
#reject = {'eeg': 40e-6}
#events_Target_number = {'target_number': 51} #the way to indicate events of interest
epochs_parietal = mne.Epochs(Data_Filtered, events=events, tmin=-0.2, tmax=0.8, picks=pick_parietal , preload=True,baseline = (None, 0.0))# ,reject=True)
#epochs_parietal.plot()

epochs_frontal = mne.Epochs(Data_Filtered,  events=events, tmin=-0.2, tmax=0.8, picks=pick_frontal , preload=True,baseline = (None, 0.0))#,reject=reject)
#epochs_frontal.plot()

# create epochs based on 
    #sounds
trig_buzz_frontal = epochs_frontal[53].average()
trig_neutral_frontal = epochs_frontal[52].average()


trig_buzz_parietal = epochs_parietal[52].average()
trig_neutral_parietal = epochs_parietal[53].average()
    #target number
trig_number_nodis = epochs_parietal[51].average()
trig_number_buzz = epochs_parietal[57].average()
trig_number_neutral = epochs_parietal[56].average()

#Combine epochs for plotting
all_evokeds_frontal = [trig_buzz_frontal, trig_neutral_frontal]
all_evokeds_parietal = [trig_buzz_parietal, trig_neutral_parietal]
all_evokeds_targets = [trig_number_nodis, trig_number_buzz, trig_number_neutral]

#Plot the different conditions sounds frontal
ylength = dict(eeg=[-12, 12])
pick = all_evokeds_frontal[1].ch_names.index('Fpz') # just to choose an electrode, index doesn't matter
mne.viz.plot_compare_evokeds(dict(neutral=trig_neutral_frontal, buzz=trig_buzz_frontal), legend=True, title='sounds frontal')

#Plot the different conditions sounds parietal
ylength = dict(eeg=[-12, 12])
pick = all_evokeds_parietal[1].ch_names.index('Pz') # just to choose an electrode, index doesn't matter
mne.viz.plot_compare_evokeds(dict(neutral=trig_neutral_parietal, buzz=trig_buzz_parietal), legend=True, title='sounds parietal')

#Plot the different conditions target numbers parietal
ylength = dict(eeg=[-12, 12])
pick = all_evokeds_targets[2].ch_names.index('Pz') # just to choose an electrode, index doesn't matter
mne.viz.plot_compare_evokeds(dict(neutral=trig_number_neutral, buzz=trig_number_buzz, nodis=trig_number_nodis), legend=True, title='target numbers parietal')

#Plot the different conditions 
ylength = dict(eeg=[-12, 12])
pick = trig_number_buzz.ch_names.index('Pz') # just to choose an electrode, index doesn't matter
mne.viz.plot_compare_evokeds(dict(buzz=trig_number_buzz), legend=True, title=None)

#Plot the different conditions
ylength = dict(eeg=[-12, 12])
pick = trig_number_buzz.ch_names.index('Pz') # just to choose an electrode, index doesn't matter
mne.viz.plot_compare_evokeds(dict(buzz=trig_number_buzz), legend=True, title=None)