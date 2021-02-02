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
                                                  
frontal theta
                                                  
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
theta_low, theta_high = 4, 8


freqs = np.arange(0, 50.5 , 0.5)  #shape (551,)
# Find intersecting values in frequency vector
idx_theta = np.logical_and(freqs >= theta_low, freqs <= theta_high)


# Specify the electrodes that cover the ares of interest
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
    
    baseline_fft =  mne.time_frequency.psd_welch(baseline_epoch, fmin =theta_low, fmax = theta_high,picks = frontal)
    
    # define frequencies of interest (log-spaced)
    freqs = np.logspace(*np.log10([4, 30]), num=8)
    n_cycles = freqs / 2.  # different number of cycle per frequency
    power, itc = tfr_morlet(baseline_epoch, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                        return_itc=True, decim=3, n_jobs=1,picks =frontal )
    power.plot(baseline=(-0.5, 0), mode='logratio', title='power')
    '''
    #Choose epoch to convert to dataframe
    baseline = baseline_epoch.to_data_frame().reset_index(drop=True)
    baseline_open = baseline.loc[ 0 : 12000 , :  ]
    baseline_closed = baseline.loc[ 12001 : 24001 , :  ]
    
    nodis = nodis_epoch.to_data_frame().reset_index(drop=True)
    buzz = buzz_epoch.to_data_frame().reset_index(drop=True)
    neutral = neutral_epoch.to_data_frame().reset_index(drop=True)




    for electrode in frontal:
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
      # Plot the power spectral density and fill the theta area
      plt.figure(figsize=(7, 4))
      plt.plot(freqs_baseline_open, psd_baseline_open, lw=2, color='k')
      plt.fill_between(freqs_baseline_open, psd_baseline_open, where=idx_theta, color='skyblue')
      plt.xlabel('Frequency (Hz)')
      plt.ylabel('Power spectral density (uV^2 / Hz)')
      plt.xlim([0, 20])
      plt.ylim([0, psd_baseline_open.max() * 1.1])
      plt.title("Welch's periodogram")
      sns.despine()
      '''
      
      '''
      # Absolute bandpower just by taking mean of psd
      Base_thetaAbsPower = np.mean(psd_baseline_open[idx_theta])
      Nodis_thetaAbsPower = np.mean(psd_nodis[idx_theta])
      Buzz_thetaAbsPower = np.mean(psd_buzz[idx_theta])
      Neutral_thetaAbsPower = np.mean(psd_neutral[idx_theta])
      
      # compute absolute bandpower with baseline correction (Decibel Conversion dB = 10*log10(signal/baseline))
      Nodis_thetaAbsPowerRelChaBL = ((Nodis_thetaAbsPower-Base_thetaAbsPower)/Base_thetaAbsPower)
      Buzz_thetaAbsPowerRelChaBL = ((Buzz_thetaAbsPower-Base_thetaAbsPower)/Base_thetaAbsPower)
      Neutral_thetaAbsPowerRelChaBL = ((Neutral_thetaAbsPower-Base_thetaAbsPower)/Base_thetaAbsPower)
      '''
      
      #Compute average absolute band power
     
  
      # Compute the average absolute power by approximating the area under the curve (simpson)
      # Frequency resolution
      freq_res = freqs[1] - freqs[0]  # = 1 / 2 = 0.5
      
      base_open_theta_power = simps(psd_baseline_open[idx_theta], dx=freq_res)
      nodis_theta_power = simps(psd_nodis[idx_theta], dx=freq_res)
      buzz_theta_power = simps(psd_buzz[idx_theta], dx=freq_res)
      neutral_theta_power = simps(psd_neutral[idx_theta], dx=freq_res)
      #print('Absolute theta power: %.3f uV^2' % theta_power)
      

      # Relative power (expressed as a percentage of total power)(simpson)
      base_open_total_power = simps(psd_baseline_open, dx=freq_res)
      base_open_theta_rel_power = base_open_theta_power / base_open_total_power
      
      nodis_total_power = simps(psd_nodis, dx=freq_res)
      nodis_theta_rel_power = nodis_theta_power / nodis_total_power
      
      buzz_total_power = simps(psd_buzz, dx=freq_res)
      buzz_theta_rel_power = buzz_theta_power / buzz_total_power
      
      neutral_total_power = simps(psd_neutral, dx=freq_res)
      neutral_theta_rel_power = neutral_theta_power / neutral_total_power
    
      #print('Relative theta power: %.3f' % theta_rel_power)
      
      
      #Compute average absolute power (simpson) with baseline correction (Decibel Conversion dB = 10*log10(signal/baseline))
      nodis_thetaPowerDecLog= 10*(np.log10(nodis_theta_power / base_open_theta_power))
      buzz_thetaPowerDecLog= 10*(np.log10(buzz_theta_power / base_open_theta_power))
      neutral_thetaPowerDecLog= 10*(np.log10(neutral_theta_power / base_open_theta_power))
      
      
      #Compute abs power just by taking mean of psd
      baseline_mean_psd_theta_power = np.mean(psd_baseline_open[idx_theta])
      nodis_mean_psd_theta_power = np.mean(psd_nodis[idx_theta])
      neutral_mean_psd_theta_power = np.mean(psd_neutral[idx_theta])
      buzz_mean_psd_theta_power = np.mean(psd_buzz[idx_theta])
  
      #Compute abs power just by taking mean of psd + LOG
      baseline_log_psd_theta_power = np.mean(10*(np.log10(psd_baseline_open))[idx_theta])
      nodis_log_psd_theta_power = np.mean(10*(np.log10(psd_nodis))[idx_theta])
      neutral_log_psd_theta_power = np.mean(10*(np.log10(psd_neutral))[idx_theta])
      buzz_log_psd_theta_power = np.mean(10*(np.log10(psd_buzz))[idx_theta])
      
      #Compute abs power by taking a mean of psd with decibel baseline correction
      nodis_declog_psd_theta_power = 10*(np.log10(nodis_mean_psd_theta_power / baseline_mean_psd_theta_power))
      neutral_declog_psd_theta_power = 10*(np.log10(neutral_mean_psd_theta_power / baseline_mean_psd_theta_power))
      buzz_declog_psd_theta_power = 10*(np.log10(buzz_mean_psd_theta_power / baseline_mean_psd_theta_power))
      
      
      
      #Create a dataframe with desired columns
      data = {'participant':  [],
        'nodis_thetaPowerDecLog'+electrode: [],
        'buzz_thetaPowerDecLog'+electrode:[],
        'neutral_thetaPowerDecLog'+electrode:[],
        'nodis_theta_rel_power'+electrode:[],
        'buzz_theta_rel_power'+electrode:[],
        'neutral_theta_rel_power'+electrode:[],
        'baseline_theta_rel_power'+electrode:[],
        'baseline_abs_theta_power'+electrode:[],
        'nodis_abs_theta_power'+electrode:[],
        'buzz_abs_theta_power'+electrode:[],
        'neutral_abs_theta_power'+electrode:[],
        'baseline_mean_psd_theta_power'+electrode:[],
        'nodis_mean_psd_theta_power'+electrode:[],
        'neutral_mean_psd_theta_power'+electrode:[],
        'buzz_mean_psd_theta_power'+electrode:[],
        'baseline_log_psd_theta_power'+electrode:[],
        'nodis_log_psd_theta_power'+electrode:[],
        'neutral_log_psd_theta_power'+electrode:[],
        'buzz_log_psd_theta_power'+electrode:[],
        'nodis_declog_psd_theta_power'+electrode:[],
        'neutral_declog_psd_theta_power'+electrode:[],
        'buzz_declog_psd_theta_power'+electrode:[],


        

        
        }
      
      data = pd.DataFrame(data)
      
      data['participant'] = participantId
      
      #for baseline
      data['baseline_theta_rel_power'+electrode]=base_open_theta_rel_power
      data['baseline_abs_theta_power'+electrode]=base_open_theta_power
      data['baseline_mean_psd_theta_power'+electrode]=baseline_mean_psd_theta_power
      data['baseline_log_psd_theta_power'+electrode]=baseline_log_psd_theta_power      

      ##for block nodis
      data['nodis_thetaPowerDecLog'+electrode]=nodis_thetaPowerDecLog
      data['nodis_theta_rel_power'+electrode]=nodis_theta_rel_power 
      data['nodis_abs_theta_power'+electrode]=nodis_theta_power 
      data['nodis_mean_psd_theta_power'+electrode]=nodis_mean_psd_theta_power 
      data['nodis_log_psd_theta_power'+electrode]=nodis_log_psd_theta_power 
      data['nodis_declog_psd_theta_power'+electrode]=nodis_declog_psd_theta_power 
      

      ##for block buzz
      data['buzz_thetaPowerDecLog'+electrode]=buzz_thetaPowerDecLog
      data['buzz_theta_rel_power'+electrode]=buzz_theta_rel_power    
      data['buzz_abs_theta_power'+electrode]=buzz_theta_power
      data['buzz_mean_psd_theta_power'+electrode]=buzz_mean_psd_theta_power 
      data['buzz_log_psd_theta_power'+electrode]=buzz_log_psd_theta_power 
      data['buzz_declog_psd_theta_power'+electrode]=buzz_declog_psd_theta_power 

      ##for block neutral
      data['neutral_thetaPowerDecLog'+electrode]=neutral_thetaPowerDecLog
      data['neutral_theta_rel_power'+electrode]=neutral_theta_rel_power    
      data['neutral_abs_theta_power'+electrode]=neutral_theta_power
      data['neutral_mean_psd_theta_power'+electrode]=neutral_mean_psd_theta_power 
      data['neutral_log_psd_theta_power'+electrode]=neutral_log_psd_theta_power 
      data['neutral_declog_psd_theta_power'+electrode]=neutral_declog_psd_theta_power 
      
      
      
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
#for average absolute theta power with baseline correction (SIMPSON)
data_frequency['frontal_buzz_thetaPowerDecLog'] = data_frequency[[
    'buzz_thetaPowerDecLogF1', 'buzz_thetaPowerDecLogF2',
    'buzz_thetaPowerDecLogFz', 'buzz_thetaPowerDecLogAFz'
    ]].mean(axis=1)

data_frequency['frontal_nodis_thetaPowerDecLog'] = data_frequency[[
    'nodis_thetaPowerDecLogF1', 'nodis_thetaPowerDecLogF2',
    'nodis_thetaPowerDecLogFz', 'nodis_thetaPowerDecLogAFz'
    ]].mean(axis=1)

data_frequency['frontal_neutral_thetaPowerDecLog'] = data_frequency[[
    'neutral_thetaPowerDecLogF1', 'neutral_thetaPowerDecLogF2',
    'neutral_thetaPowerDecLogFz', 'neutral_thetaPowerDecLogAFz'
    ]].mean(axis=1)

#for relative theta power (SIMPSON)
data_frequency['frontal_nodis_theta_rel_power'] = data_frequency[[
    'nodis_theta_rel_powerF1', 'nodis_theta_rel_powerF2',
    'nodis_theta_rel_powerFz', 'nodis_theta_rel_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_buzz_theta_rel_power'] = data_frequency[[
    'buzz_theta_rel_powerF1', 'buzz_theta_rel_powerF2',
    'buzz_theta_rel_powerFz', 'buzz_theta_rel_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_neutral_theta_rel_power'] = data_frequency[[
    'neutral_theta_rel_powerF1', 'neutral_theta_rel_powerF2',
    'neutral_theta_rel_powerFz', 'neutral_theta_rel_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_baseline_theta_rel_power'] = data_frequency[[
    'baseline_theta_rel_powerF1', 'baseline_theta_rel_powerF2',
    'baseline_theta_rel_powerFz', 'baseline_theta_rel_powerAFz'
    ]].mean(axis=1)



#for absolute theta power (SIMPSON)

data_frequency['frontal_neutral_theta_abs_power'] = data_frequency[[
    'neutral_abs_theta_powerF1', 'neutral_abs_theta_powerF2',
    'neutral_abs_theta_powerFz', 'neutral_abs_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_nodis_theta_abs_power'] = data_frequency[[
    'nodis_abs_theta_powerF1', 'nodis_abs_theta_powerF2',
    'nodis_abs_theta_powerFz', 'nodis_abs_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_buzz_theta_abs_power'] = data_frequency[[
    'buzz_abs_theta_powerF1', 'buzz_abs_theta_powerF2',
    'buzz_abs_theta_powerFz', 'buzz_abs_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_baseline_theta_abs_power'] = data_frequency[[
    'baseline_abs_theta_powerF1', 'baseline_abs_theta_powerF2',
    'baseline_abs_theta_powerFz', 'baseline_abs_theta_powerAFz'
    ]].mean(axis=1)


#for absolute theta power (mean psd)
data_frequency['frontal_neutral_mean_psd_theta_power'] = data_frequency[[
    'neutral_mean_psd_theta_powerF1', 'neutral_mean_psd_theta_powerF2',
    'neutral_mean_psd_theta_powerFz', 'neutral_mean_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_nodis_mean_psd_theta_power'] = data_frequency[[
    'nodis_mean_psd_theta_powerF1', 'nodis_mean_psd_theta_powerF2',
    'nodis_mean_psd_theta_powerFz', 'nodis_mean_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_buzz_mean_psd_theta_power'] = data_frequency[[
    'buzz_mean_psd_theta_powerF1', 'buzz_mean_psd_theta_powerF2',
    'buzz_mean_psd_theta_powerFz', 'buzz_mean_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_baseline_mean_psd_theta_power'] = data_frequency[[
    'baseline_mean_psd_theta_powerF1', 'baseline_mean_psd_theta_powerF2',
    'baseline_mean_psd_theta_powerFz', 'baseline_mean_psd_theta_powerAFz'
    ]].mean(axis=1)

#for absolute theta power LOG (mean psd)
data_frequency['frontal_neutral_log_psd_theta_power'] = data_frequency[[
    'neutral_log_psd_theta_powerF1', 'neutral_log_psd_theta_powerF2',
    'neutral_log_psd_theta_powerFz', 'neutral_log_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_nodis_log_psd_theta_power'] = data_frequency[[
    'nodis_log_psd_theta_powerF1', 'nodis_log_psd_theta_powerF2',
    'nodis_log_psd_theta_powerFz', 'nodis_log_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_buzz_log_psd_theta_power'] = data_frequency[[
    'buzz_log_psd_theta_powerF1', 'buzz_log_psd_theta_powerF2',
    'buzz_log_psd_theta_powerFz', 'buzz_log_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_baseline_log_psd_theta_power'] = data_frequency[[
    'baseline_log_psd_theta_powerF1', 'baseline_log_psd_theta_powerF2',
    'baseline_log_psd_theta_powerFz', 'baseline_log_psd_theta_powerAFz'
    ]].mean(axis=1)

#for absolute theta power DECLOG (mean psd)
data_frequency['frontal_neutral_declog_psd_theta_power'] = data_frequency[[
    'neutral_declog_psd_theta_powerF1', 'neutral_declog_psd_theta_powerF2',
    'neutral_declog_psd_theta_powerFz', 'neutral_declog_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_nodis_declog_psd_theta_power'] = data_frequency[[
    'nodis_declog_psd_theta_powerF1', 'nodis_declog_psd_theta_powerF2',
    'nodis_declog_psd_theta_powerFz', 'nodis_declog_psd_theta_powerAFz'
    ]].mean(axis=1)

data_frequency['frontal_buzz_declog_psd_theta_power'] = data_frequency[[
    'buzz_declog_psd_theta_powerF1', 'buzz_declog_psd_theta_powerF2',
    'buzz_declog_psd_theta_powerFz', 'buzz_declog_psd_theta_powerAFz'
    ]].mean(axis=1)


#Save dataframe to csv file

data_frequency.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_theta.csv', index = None, header=True)    
    
info=data_frequency.describe()      

      
      
      
     
    



