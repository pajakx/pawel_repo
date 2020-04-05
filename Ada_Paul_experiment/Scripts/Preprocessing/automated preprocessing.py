# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:41:45 2020

                                                 (_)            
 _ __  _ __ ___ _ __  _ __ ___   ___ ___  ___ ___ _ _ __   __ _ 
| '_ \| '__/ _ \ '_ \| '__/ _ \ / __/ _ \/ __/ __| | '_ \ / _` |
| |_) | | |  __/ |_) | | | (_) | (_|  __/\__ \__ \ | | | | (_| |
| .__/|_|  \___| .__/|_|  \___/ \___\___||___/___/_|_| |_|\__, |
| |            | |                                         __/ |
|_|            |_|                                        |___/ 
             _                        _           _             
            | |                      | |         | |            
  __ _ _   _| |_ ___  _ __ ___   __ _| |_ ___  __| |            
 / _` | | | | __/ _ \| '_ ` _ \ / _` | __/ _ \/ _` |            
| (_| | |_| | || (_) | | | | | | (_| | ||  __/ (_| |            
 \__,_|\__,_|\__\___/|_| |_| |_|\__,_|\__\___|\__,_|            
                                                          


@author: Paweł Jakuszyk based on TOON
"""
import os, mne

# Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\raw_data\\'

# Directory for preprocessed data
directory_to_write= filepath +"preprocessed_auto\\"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter bad channels per subject
badchannels = [[], #1
               ['C3', 'FC1', 'F1', 'POz', 'CPz', 'PO8', 'PO4', 'O2', 'P7','Fz','F1','FC1','PO4','P2'], #2
               ['Iz','PO3'], #3
               ['P10','POz','Iz','PO8'], #4
               ['P2'], #5
               [],#no participant 6
               ['P2'], #7
               ['P2'], #8
               [], #9
               [], #10
               ['P2'], #11
               [], #12
               [], #13
               [], #14
               ['P2'], #15
               [], #16
               [], #17
               ['P2', 'PO4'], #18
               [], #19
               ['FC4'], #20
               ['FC2'], #21
               [], #22
               ['Iz'], #23
               [], #24
               ['P2'], #25
               ['P2'], #26
               [], #27
               [], #28
               [], #29
               ['P2'], #30
               []] #31



# Enter the list of subjects you want to analyse
participants = [1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

for participant in participants:
  
  raw = mne.io.read_raw_fif(filepath + '\\P'+str(participant)+ '.fif', preload=True)
  
  ## Rename and drop channles
  
  raw.rename_channels(mapping={'A1':'Fp1', 'A2':'AF7', 'A3':'AF3', 'A4':'F1', 'A5':'F3', 'A6':'F5', 'A7':'F7',
                                         'A8':'FT7', 'A9':'FC5', 'A10':'FC3', 'A11':'FC1', 'A12':'C1', 'A13':'C3', 'A14':'C5',
                                         'A15':'T7', 'A16':'TP7', 'A17':'CP5', 'A18':'CP3', 'A19':'CP1', 'A20':'P1', 'A21':'P3',                                     
                                         'A22':'P5', 'A23':'P7', 'A24':'P9', 'A25':'PO7', 'A26':'PO3', 'A27':'O1', 'A28':'Iz',
                                         'A29':'Oz', 'A30':'POz', 'A31':'Pz', 'A32':'CPz', 'B1':'Fpz', 'B2':'Fp2', 'B3':'AF8',                                  
                                         'B4':'AF4', 'B5':'AFz', 'B6':'Fz', 'B7':'F2', 'B8':'F4', 'B9':'F6', 'B10':'F8', 
                                         'B11':'FT8', 'B12':'FC6', 'B13':'FC4', 'B14':'FC2', 'B15':'FCz', 'B16':'Cz', 'B17':'C2',                                 
                                         'B18':'C4', 'B19':'C6', 'B20':'T8', 'B21':'TP8', 'B22':'CP6', 'B23':'CP4', 'B24':'CP2',  
                                         'B25':'P2', 'B26':'P4', 'B27':'P6', 'B28':'P8', 'B29':'P10', 'B30':'PO8', 'B31':'PO4',
                                         'B32':'O2','C1':'M1', 'C2':'M2', 'C3':'HEOGleft','C4':'HEOGright',
                                         'C5':'VEOGup', 'C6':'VEOGdown','Status':'triggers'})
  

   # Setting channel montage
  montage = mne.channels.read_montage('biosemi64')
  raw.set_montage(montage)
    
   # Creating EOG channels
  raw = mne.set_bipolar_reference(raw,anode='VEOGup',cathode='VEOGdown',ch_name='VEOG')
  raw = mne.set_bipolar_reference(raw,anode='HEOGleft',cathode='HEOGright',ch_name='HEOG')
  raw.set_channel_types({'VEOG':'eog','HEOG':'eog'})
    
    # Setting reference (mastoids, but given different name for better electrode location)
  raw.set_eeg_reference(['M1','M2'])
  raw.drop_channels(['M1','M2'])
    # raw.set_eeg_reference(ref_channels='average')
    
    # # Investigating raw data (Identify bad channels and add to list above)
    # raw.plot()
    # raw.plot_psd(fmax=70)
    
     ###############
    ## Filtering ##
    ###############
            
    # Low-pass filter
    #for ERP
  raw.filter(.05, 30., fir_design='firwin')
    
    #for TFA
  #raw.filter(1, 30., fir_design='firwin')
    
    # Resampling
  #raw.resample(100, npad="auto")

    
    # Interpolating bad channels
  raw.info['bads'] = badchannels[participant-1]
  raw.interpolate_bads(reset_bads = True) 
    
    # # Investigating resulting data
    # raw.plot()
  raw.plot_psd(fmax=30)

    
    # Save ERP
  raw.save(directory_to_write + 'P'+str(participant)+'Filtered_0.1.fif' , overwrite=True)
    
    # Save TFA
  #raw.save(directory_to_write + 'P'+str(participant)+'Filtered_1.fif' , overwrite=True)
