# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:16:17 2021
____________  _____                            _             
| ___ \ ___ \/  ___|                          (_)            
| |_/ / |_/ /\ `--.   _ __ ___   ___ _ __ __ _ _ _ __   __ _ 
|  __/|  __/  `--. \ | '_ ` _ \ / _ \ '__/ _` | | '_ \ / _` |
| |   | |    /\__/ / | | | | | |  __/ | | (_| | | | | | (_| |
\_|   \_|    \____/  |_| |_| |_|\___|_|  \__, |_|_| |_|\__, |
                                          __/ |         __/ |
                                         |___/         |___/ 
@author: Paweł Jakuszyk
"""

import numpy as np
import pandas as pd
import os as os


#Specify the folder where you store the files
mypath = r'C:\Users\Pawel\Desktop\PPS_pilot_data'

#Specify the path where you want the result to be saved
directory_to_write = r'C:\Users\Pawel\Desktop\PPS_pilot_data\PPS_exp\results'
if not os.path.exists(directory_to_write):
    os.makedirs(directory_to_write)
    
#Specify the files to be merged

psychopy = pd.read_excel(mypath + '\\PPS_exp\\results\\PPS_results_all.xlsx')

qualtrics =  pd.read_excel(mypath + '\\PPS_qualtrics\\PPS_qual.xlsx')

#drop second header
qualtrics = qualtrics.drop([0, ])

#drop unnecessary columns
qualtrics = qualtrics.drop(columns=['StartDate', 'EndDate', 'Status', 'IPAddress', 'RecordedDate','ResponseId',
                                    'RecipientLastName', 'RecipientFirstName', 'RecipientEmail', 'ExternalReference',
                                    'LocationLatitude', 'LocationLongitude', 'DistributionChannel', 'UserLanguage'])

#change column name from id to participant
qualtrics = qualtrics.rename(columns={"id": "participant"})

#change common column to the same type
qualtrics['participant'] = qualtrics['participant'].astype(int)
psychopy['participant'] = psychopy['participant'].astype(int)

#join on participant column

#results_PPS_merged = pd.concat([qualtrics.set_index('participant'),psychopy.set_index('participant')], axis=1, join = 'inner').reset_index()


results_PPS_merged = pd.merge(qualtrics, psychopy, on='participant')

#Save the data to an excel file
results_PPS_merged.to_excel(directory_to_write + '\\' + 'PPS_results_all_merged.xlsx', index = None, header=True)
