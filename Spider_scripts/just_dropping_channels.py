# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 17:24:16 2020

@author: Paweł Jakuszyk
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
# Directory 
filepath = r'C:\\Users\\user\\Desktop\\FOCUS\\'

#subjects with 8 external electrodes
#subjects_pre = [1,2,3,4] #1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,40,41,42,43,44,45,46
## Read the raw data of one participant
#subject = ("1") #1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,40,41,42,43,44,45,46
## Read the raw data of one participant

# Enter the list of subjects you want to analyse
participants = [5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
#[1,2,3,4]#
for participant in participants:
  
  Data_rawEEG = mne.io.read_raw_edf(filepath + '\\P'+str(participant)+ '.bdf', preload=True)


## Rename and drop channles
  Data_rawEEG.drop_channels(['C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19',
                               'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31',
                               'C32', 'GSR1', 'GSR2', 'Erg1', 'Erg2', 'Resp', 'Plet', 'Temp'])
  
  #                             'EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6','EXG7', 'EXG8'])


  Data_rawEEG.save(filepath + 'P' + str(participant) + ".fif",overwrite= True )