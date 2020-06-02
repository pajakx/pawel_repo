# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 14:45:24 2020
 _________________                                
|_   _|  ___|  _  \                               
  | | | |_  | | | |                               
  | | |  _| | | | |                               
  | | | |   | |/ /                                
  \_/ \_|   |___/                                 
                                                  
                                                  
 _                                                
| |                                               
| |_ ___                                          
| __/ _ \                                         
| || (_) |                                        
 \__\___/                                         
                                                  
                                                  
______      _       ______                        
|  _  \    | |      |  ___|                       
| | | |__ _| |_ __ _| |_ _ __ __ _ _ __ ___   ___ 
| | | / _` | __/ _` |  _| '__/ _` | '_ ` _ \ / _ \
| |/ / (_| | || (_| | | | | | (_| | | | | | |  __/
|___/ \__,_|\__\__,_\_| |_|  \__,_|_| |_| |_|\___|
                                                  
parietal alpha
                                                  
https://raphaelvallat.com/bandpower.html

@author: Paweł Jakuszyk
"""

# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker
import datetime
import seaborn as sns
import numpy as np
import matplotlib as mpl
import seaborn as sns
import glob
import pickle
import os
from tqdm import tqdm
from scipy import stats
from scipy import signal 
from scipy.integrate import simps
from matplotlib import cm
import mne
from mne.preprocessing import create_eog_epochs
from mne.datasets import somato
from mne.time_frequency import tfr_morlet, psd_multitaper, psd_welch
from scipy.integrate import simps
import csv
##############################
## Create lists for epochs  ##
##############################

baseline_freq = []
nodis_freq = []
buzz_freq = []
neutral_freq = []

#Set parameters for FFT
Fs = 100.                       # set the sampling rate (in Hz)
sliding_window = 2 * Fs         # select the sliding window: at least two cycles of the lowest freq of interest (2/1Hz=2). Here in datapoints (200 x 10 ms).
overlap = 0.50                  # decide on overlap percentage of 50%
n_overlap = int(sliding_window * overlap)

                
# upper and lower border of freq bands
# sampling rate is 100hz dus max freq is 50Hz (nyquist theorem)
Gamma_low, Gamma_high = 30, 50 
Beta_low, Beta_high = 12, 30
Alpha_low, Alpha_high = 8, 12
Theta_low, Theta_high = 4, 8
Delta_low, Delta_high = 1,4

freqs = np.arange(0, 50.5 , 0.5)  #shape (551,)
# Find intersecting values in frequency vector
idx_Gamma = np.logical_and(freqs >= Gamma_low, freqs <= Gamma_high)
idx_Beta = np.logical_and(freqs >= Beta_low, freqs <= Beta_high)
idx_Alpha = np.logical_and(freqs >= Alpha_low, freqs <= Alpha_high)
idx_Theta = np.logical_and(freqs >= Theta_low, freqs <= Theta_high)
idx_Delta = np.logical_and(freqs >= Delta_low, freqs <= Delta_high)
  

# Specify the electrodes that cover the ares of interest
parietal = ['P1','P2','Pz','POz']
frontal = ['F1','F2','Fz','AFz']

#Define a master list for dataframes of all the frequency values
master = []


    ####################
    ## Initialization ##
    ####################

# Main Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\epoched_TFA'
print("----> Complete! The filepath is: " + filepath)
# Directory for epoched data
directory_to_write= filepath + "\\analysis\\"
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)

# Enter the list of subjects you want to analyse
participants = [1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

for participant in participants:
  
########################
## Frequency Analysis ##
########################
  
    #Create list for one participant all electrodes data
    padawan = []
  
    #Set participant ID var
    participantId = ["P" + str(participant)] 

    # Importing Epoched Data
    baseline_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_baseline-epo.fif', preload=True)
    nodis_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_nodis-epo.fif', preload=True)
    buzz_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_buzz-epo.fif', preload=True)
    neutral_epoch = mne.read_epochs(filepath + '\\P'+str(participant)+'_neutral-epo.fif', preload=True)
    
    '''
    #Let’s first check out all channel types by averaging across epochs.
    baseline_epoch.plot_psd(fmin=2., fmax=30., average=True, spatial_colors=True)
    nodis_epoch.plot_psd(fmin=2., fmax=30., average=True, spatial_colors=True)
    buzz_epoch.plot_psd(fmin=2., fmax=30., average=True, spatial_colors=True)
    neutral_epoch.plot_psd(fmin=2., fmax=30., average=True, spatial_colors=True)
    
    #Now let’s take a look at the spatial distributions of the PSD.
    baseline_epoch.plot_psd_topomap(ch_type='eeg', normalize=True)
    
    baseline = baseline_epoch.to_data_frame()
    baseline_pickel = pickle.load(baseline)
    
    baseline_fft =  mne.time_frequency.psd_welch(baseline_epoch, fmin =alpha_low, fmax = alpha_high,picks = parietal)
    
    # define frequencies of interest (log-spaced)
    freqs = np.logspace(*np.log10([4, 30]), num=8)
    n_cycles = freqs / 2.  # different number of cycle per frequency
    power, itc = tfr_morlet(baseline_epoch, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1,picks =parietal )
    power.plot(baseline=(-0.5, 0), mode='logratio', title='power')
    '''
    #Choose epoch to convert to dataframe
    baseline = baseline_epoch.to_data_frame().reset_index(drop=True)
    baseline_open = baseline.loc[ 0 : 12000 , :  ]
    baseline_closed = baseline.loc[ 12001 : 24001 , :  ]
    
    nodis = nodis_epoch.to_data_frame().reset_index(drop=True)
    buzz = buzz_epoch.to_data_frame().reset_index(drop=True)
    neutral = neutral_epoch.to_data_frame().reset_index(drop=True)




    for electrode in parietal:
      #Choose electrodes to investigate
      data_baseline_open=baseline_open[electrode]
      data_baseline_closed=baseline_closed[electrode]
      data_nodis=nodis[electrode]
      data_buzz=buzz[electrode]
      data_neutral=neutral[electrode]

      
      #Compute Welch transform
      freqs_baseline_open, psd_baseline_open = signal.welch(data_baseline_open, Fs, nperseg=sliding_window,noverlap=n_overlap)
      freqs_baseline_closed, psd_baseline_closed = signal.welch(data_baseline_closed, Fs, nperseg=sliding_window,noverlap=n_overlap)
      freqs_nodis, psd_nodis = signal.welch(data_nodis, Fs, nperseg=sliding_window,noverlap=n_overlap)
      freqs_buzz, psd_buzz = signal.welch(data_buzz, Fs, nperseg=sliding_window,noverlap=n_overlap)
      freqs_neutral, psd_neutral = signal.welch(data_neutral, Fs, nperseg=sliding_window,noverlap=n_overlap)

      
      
      '''
      # Plot the power spectrum
      sns.set(font_scale=1.2, style='white')
      plt.figure(figsize=(8, 4))
      plt.plot(freqs, psd, color='k', lw=2)
      plt.xlabel('Frequency (Hz)')
      plt.ylabel('Power spectral density (V^2 / Hz)')
      plt.ylim([0, psd.max() * 1.1])
      plt.title("Welch's periodogram")
      plt.xlim([0, freqs.max()])
      sns.despine()
      '''
      
      '''
      # Plot the power spectral density and fill the alpha area
      plt.figure(figsize=(7, 4))
      plt.plot(freqs_baseline_open, psd_baseline_open, lw=2, color='k')
      plt.fill_between(freqs_baseline_open, psd_baseline_open, where=idx_Alpha, color='skyblue')
      plt.xlabel('Frequency (Hz)')
      plt.ylabel('Power spectral density (uV^2 / Hz)')
      plt.xlim([0, 20])
      plt.ylim([0, psd_baseline_open.max() * 1.1])
      plt.title("Welch's periodogram")
      sns.despine()
      '''
      
      '''
      # Absolute bandpower just by taking mean of psd
      Base_AlphaAbsPower = np.mean(psd_baseline_open[idx_Alpha])
      Nodis_AlphaAbsPower = np.mean(psd_nodis[idx_Alpha])
      Buzz_AlphaAbsPower = np.mean(psd_buzz[idx_Alpha])
      Neutral_AlphaAbsPower = np.mean(psd_neutral[idx_Alpha])
      
      # compute absolute bandpower with baseline correction (Decibel Conversion dB = 10*log10(signal/baseline))
      Nodis_AlphaAbsPowerRelChaBL = ((Nodis_AlphaAbsPower-Base_AlphaAbsPower)/Base_AlphaAbsPower)
      Buzz_AlphaAbsPowerRelChaBL = ((Buzz_AlphaAbsPower-Base_AlphaAbsPower)/Base_AlphaAbsPower)
      Neutral_AlphaAbsPowerRelChaBL = ((Neutral_AlphaAbsPower-Base_AlphaAbsPower)/Base_AlphaAbsPower)
      '''
      
      #Compute average absolute band power
     
  
      # Compute the average absolute power by approximating the area under the curve (simpson)
      # Frequency resolution
      freq_res = freqs[1] - freqs[0]  # = 1 / 2 = 0.5
      
      base_open_alpha_power = simps(psd_baseline_open[idx_Alpha], dx=freq_res)
      nodis_alpha_power = simps(psd_nodis[idx_Alpha], dx=freq_res)
      buzz_alpha_power = simps(psd_buzz[idx_Alpha], dx=freq_res)
      neutral_alpha_power = simps(psd_neutral[idx_Alpha], dx=freq_res)
      #print('Absolute alpha power: %.3f uV^2' % alpha_power)
      

      # Relative power (expressed as a percentage of total power)(simpson)
      base_open_total_power = simps(psd_baseline_open, dx=freq_res)
      base_open_alpha_rel_power = base_open_alpha_power / base_open_total_power
      
      nodis_total_power = simps(psd_nodis, dx=freq_res)
      nodis_alpha_rel_power = nodis_alpha_power / nodis_total_power
      
      buzz_total_power = simps(psd_buzz, dx=freq_res)
      buzz_alpha_rel_power = buzz_alpha_power / buzz_total_power
      
      neutral_total_power = simps(psd_neutral, dx=freq_res)
      neutral_alpha_rel_power = neutral_alpha_power / neutral_total_power
    
      #print('Relative alpha power: %.3f' % alpha_rel_power)
      
      
      #Compute average absolute power (simpson) with baseline correction (Decibel Conversion dB = 10*log10(signal/baseline))
      nodis_AlphaPowerDecLog= 10*(np.log10(nodis_alpha_power / base_open_alpha_power))
      buzz_AlphaPowerDecLog= 10*(np.log10(buzz_alpha_power / base_open_alpha_power))
      neutral_AlphaPowerDecLog= 10*(np.log10(neutral_alpha_power / base_open_alpha_power))
      
      
      #Compute abs power just by taking mean of psd
      baseline_mean_psd_alpha_power = np.mean(psd_baseline_open[idx_Alpha])
      nodis_mean_psd_alpha_power = np.mean(psd_nodis[idx_Alpha])
      neutral_mean_psd_alpha_power = np.mean(psd_neutral[idx_Alpha])
      buzz_mean_psd_alpha_power = np.mean(psd_buzz[idx_Alpha])
  
      #Compute abs power just by taking mean of psd + LOG
      baseline_log_psd_alpha_power = np.mean(10*(np.log10(psd_baseline_open))[idx_Alpha])
      nodis_log_psd_alpha_power = np.mean(10*(np.log10(psd_nodis))[idx_Alpha])
      neutral_log_psd_alpha_power = np.mean(10*(np.log10(psd_neutral))[idx_Alpha])
      buzz_log_psd_alpha_power = np.mean(10*(np.log10(psd_buzz))[idx_Alpha])
      
      #Compute abs power by taking a mean of psd with decibel baseline correction
      nodis_declog_psd_alpha_power = 10*(np.log10(nodis_mean_psd_alpha_power / baseline_mean_psd_alpha_power))
      neutral_declog_psd_alpha_power = 10*(np.log10(neutral_mean_psd_alpha_power / baseline_mean_psd_alpha_power))
      buzz_declog_psd_alpha_power = 10*(np.log10(buzz_mean_psd_alpha_power / baseline_mean_psd_alpha_power))
      
      
      
      #Create a dataframe with desired columns
      data = {'participant':  [],
        'nodis_AlphaPowerDecLog'+electrode: [],
        'buzz_AlphaPowerDecLog'+electrode:[],
        'neutral_AlphaPowerDecLog'+electrode:[],
        'nodis_alpha_rel_power'+electrode:[],
        'buzz_alpha_rel_power'+electrode:[],
        'neutral_alpha_rel_power'+electrode:[],
        'baseline_alpha_rel_power'+electrode:[],
        'baseline_abs_alpha_power'+electrode:[],
        'nodis_abs_alpha_power'+electrode:[],
        'buzz_abs_alpha_power'+electrode:[],
        'neutral_abs_alpha_power'+electrode:[],
        'baseline_mean_psd_alpha_power'+electrode:[],
        'nodis_mean_psd_alpha_power'+electrode:[],
        'neutral_mean_psd_alpha_power'+electrode:[],
        'buzz_mean_psd_alpha_power'+electrode:[],
        'baseline_log_psd_alpha_power'+electrode:[],
        'nodis_log_psd_alpha_power'+electrode:[],
        'neutral_log_psd_alpha_power'+electrode:[],
        'buzz_log_psd_alpha_power'+electrode:[],
        'nodis_declog_psd_alpha_power'+electrode:[],
        'neutral_declog_psd_alpha_power'+electrode:[],
        'buzz_declog_psd_alpha_power'+electrode:[],


        

        
        }
      
      data = pd.DataFrame(data)
      
      data['participant'] = participantId
      
      #for baseline
      data['baseline_alpha_rel_power'+electrode]=base_open_alpha_rel_power
      data['baseline_abs_alpha_power'+electrode]=base_open_alpha_power
      data['baseline_mean_psd_alpha_power'+electrode]=baseline_mean_psd_alpha_power
      data['baseline_log_psd_alpha_power'+electrode]=baseline_log_psd_alpha_power      

      ##for block nodis
      data['nodis_AlphaPowerDecLog'+electrode]=nodis_AlphaPowerDecLog
      data['nodis_alpha_rel_power'+electrode]=nodis_alpha_rel_power 
      data['nodis_abs_alpha_power'+electrode]=nodis_alpha_power 
      data['nodis_mean_psd_alpha_power'+electrode]=nodis_mean_psd_alpha_power 
      data['nodis_log_psd_alpha_power'+electrode]=nodis_log_psd_alpha_power 
      data['nodis_declog_psd_alpha_power'+electrode]=nodis_declog_psd_alpha_power 
      

      ##for block buzz
      data['buzz_AlphaPowerDecLog'+electrode]=buzz_AlphaPowerDecLog
      data['buzz_alpha_rel_power'+electrode]=buzz_alpha_rel_power    
      data['buzz_abs_alpha_power'+electrode]=buzz_alpha_power
      data['buzz_mean_psd_alpha_power'+electrode]=buzz_mean_psd_alpha_power 
      data['buzz_log_psd_alpha_power'+electrode]=buzz_log_psd_alpha_power 
      data['buzz_declog_psd_alpha_power'+electrode]=buzz_declog_psd_alpha_power 

      ##for block neutral
      data['neutral_AlphaPowerDecLog'+electrode]=neutral_AlphaPowerDecLog
      data['neutral_alpha_rel_power'+electrode]=neutral_alpha_rel_power    
      data['neutral_abs_alpha_power'+electrode]=neutral_alpha_power
      data['neutral_mean_psd_alpha_power'+electrode]=neutral_mean_psd_alpha_power 
      data['neutral_log_psd_alpha_power'+electrode]=neutral_log_psd_alpha_power 
      data['neutral_declog_psd_alpha_power'+electrode]=neutral_declog_psd_alpha_power 
      
      
      
      #Append the result with a master dataframe list
      padawan.append(data)
      

    #Concat the master_list 
    data_participant = pd.concat(padawan, axis=1, join='outer')#.set_index('participant')
    data_participant = data_participant.loc[:, ~data_participant.columns.duplicated()]
    
    #Append the result with a master dataframe list
    master.append(data_participant)

#Concat the master_list 
data_frequency = pd.concat(master,ignore_index=True)

##Compute averges across electrodes
#for average absolute alpha power with baseline correction (SIMPSON)
data_frequency['parietal_buzz_AlphaPowerDecLog'] = data_frequency[[
    'buzz_AlphaPowerDecLogP1', 'buzz_AlphaPowerDecLogP2',
    'buzz_AlphaPowerDecLogPz', 'buzz_AlphaPowerDecLogPOz'
    ]].mean(axis=1)

data_frequency['parietal_nodis_AlphaPowerDecLog'] = data_frequency[[
    'nodis_AlphaPowerDecLogP1', 'nodis_AlphaPowerDecLogP2',
    'nodis_AlphaPowerDecLogPz', 'nodis_AlphaPowerDecLogPOz'
    ]].mean(axis=1)

data_frequency['parietal_neutral_AlphaPowerDecLog'] = data_frequency[[
    'neutral_AlphaPowerDecLogP1', 'neutral_AlphaPowerDecLogP2',
    'neutral_AlphaPowerDecLogPz', 'neutral_AlphaPowerDecLogPOz'
    ]].mean(axis=1)

#for relative alpha power (SIMPSON)
data_frequency['parietal_nodis_alpha_rel_power'] = data_frequency[[
    'nodis_alpha_rel_powerP1', 'nodis_alpha_rel_powerP2',
    'nodis_alpha_rel_powerPz', 'nodis_alpha_rel_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_buzz_alpha_rel_power'] = data_frequency[[
    'buzz_alpha_rel_powerP1', 'buzz_alpha_rel_powerP2',
    'buzz_alpha_rel_powerPz', 'buzz_alpha_rel_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_neutral_alpha_rel_power'] = data_frequency[[
    'neutral_alpha_rel_powerP1', 'neutral_alpha_rel_powerP2',
    'neutral_alpha_rel_powerPz', 'neutral_alpha_rel_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_baseline_alpha_rel_power'] = data_frequency[[
    'baseline_alpha_rel_powerP1', 'baseline_alpha_rel_powerP2',
    'baseline_alpha_rel_powerPz', 'baseline_alpha_rel_powerPOz'
    ]].mean(axis=1)



#for absolute alpha power (SIMPSON)

data_frequency['parietal_neutral_alpha_abs_power'] = data_frequency[[
    'neutral_abs_alpha_powerP1', 'neutral_abs_alpha_powerP2',
    'neutral_abs_alpha_powerPz', 'neutral_abs_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_nodis_alpha_abs_power'] = data_frequency[[
    'nodis_abs_alpha_powerP1', 'nodis_abs_alpha_powerP2',
    'nodis_abs_alpha_powerPz', 'nodis_abs_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_buzz_alpha_abs_power'] = data_frequency[[
    'buzz_abs_alpha_powerP1', 'buzz_abs_alpha_powerP2',
    'buzz_abs_alpha_powerPz', 'buzz_abs_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_baseline_alpha_abs_power'] = data_frequency[[
    'baseline_abs_alpha_powerP1', 'baseline_abs_alpha_powerP2',
    'baseline_abs_alpha_powerPz', 'baseline_abs_alpha_powerPOz'
    ]].mean(axis=1)


#for absolute alpha power (mean psd)
data_frequency['parietal_neutral_mean_psd_alpha_power'] = data_frequency[[
    'neutral_mean_psd_alpha_powerP1', 'neutral_mean_psd_alpha_powerP2',
    'neutral_mean_psd_alpha_powerPz', 'neutral_mean_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_nodis_mean_psd_alpha_power'] = data_frequency[[
    'nodis_mean_psd_alpha_powerP1', 'nodis_mean_psd_alpha_powerP2',
    'nodis_mean_psd_alpha_powerPz', 'nodis_mean_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_buzz_mean_psd_alpha_power'] = data_frequency[[
    'buzz_mean_psd_alpha_powerP1', 'buzz_mean_psd_alpha_powerP2',
    'buzz_mean_psd_alpha_powerPz', 'buzz_mean_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_baseline_mean_psd_alpha_power'] = data_frequency[[
    'baseline_mean_psd_alpha_powerP1', 'baseline_mean_psd_alpha_powerP2',
    'baseline_mean_psd_alpha_powerPz', 'baseline_mean_psd_alpha_powerPOz'
    ]].mean(axis=1)

#for absolute alpha power LOG (mean psd)
data_frequency['parietal_neutral_log_psd_alpha_power'] = data_frequency[[
    'neutral_log_psd_alpha_powerP1', 'neutral_log_psd_alpha_powerP2',
    'neutral_log_psd_alpha_powerPz', 'neutral_log_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_nodis_log_psd_alpha_power'] = data_frequency[[
    'nodis_log_psd_alpha_powerP1', 'nodis_log_psd_alpha_powerP2',
    'nodis_log_psd_alpha_powerPz', 'nodis_log_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_buzz_log_psd_alpha_power'] = data_frequency[[
    'buzz_log_psd_alpha_powerP1', 'buzz_log_psd_alpha_powerP2',
    'buzz_log_psd_alpha_powerPz', 'buzz_log_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_baseline_log_psd_alpha_power'] = data_frequency[[
    'baseline_log_psd_alpha_powerP1', 'baseline_log_psd_alpha_powerP2',
    'baseline_log_psd_alpha_powerPz', 'baseline_log_psd_alpha_powerPOz'
    ]].mean(axis=1)

#for absolute alpha power DECLOG (mean psd)
data_frequency['parietal_neutral_declog_psd_alpha_power'] = data_frequency[[
    'neutral_declog_psd_alpha_powerP1', 'neutral_declog_psd_alpha_powerP2',
    'neutral_declog_psd_alpha_powerPz', 'neutral_declog_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_nodis_declog_psd_alpha_power'] = data_frequency[[
    'nodis_declog_psd_alpha_powerP1', 'nodis_declog_psd_alpha_powerP2',
    'nodis_declog_psd_alpha_powerPz', 'nodis_declog_psd_alpha_powerPOz'
    ]].mean(axis=1)

data_frequency['parietal_buzz_declog_psd_alpha_power'] = data_frequency[[
    'buzz_declog_psd_alpha_powerP1', 'buzz_declog_psd_alpha_powerP2',
    'buzz_declog_psd_alpha_powerPz', 'buzz_declog_psd_alpha_powerPOz'
    ]].mean(axis=1)


#Save dataframe to csv file

data_frequency.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_alpha.csv', index = None, header=True)    
    
info=data_frequency.describe()      

      
      
      
     
    



