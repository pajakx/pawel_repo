# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 10:12:08 2020
___  ___     _ _   
|  \/  |    | | |  
| .  . | ___| | |_ 
| |\/| |/ _ \ | __|
| |  | |  __/ | |_ 
\_|  |_/\___|_|\__|
                   
                   
@author: Paweł Jakuszyk
"""
import pandas as pd
import numpy as np
import os as os

#max_amp_targets

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\max_amp_targets.csv')


data2 =  pd.melt(data, id_vars=['participant'], value_vars=['Target_Block_Nodis_maxAmp_Pz',
        'Target_Block_Buzz_maxAmp_Pz','Target_Block_Neutral_maxAmp_Pz'],

        var_name='blocks', value_name='target_maxAmp_Pz')

data2 = data2.replace(             
   ['Target_Block_Neutral_maxAmp_Pz', 
    'Target_Block_Buzz_maxAmp_Pz', 
    'Target_Block_Nodis_maxAmp_Pz'],
                                  
   ['neutral_block',
    'buzz_block',
    'nodis_block']
   )

data2.to_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\max_amp_targets_long.csv', index = None, header=True)

#max_amp_sounds

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\max_amp_sounds.csv')


data2 =  pd.melt(data, id_vars=['participant'], value_vars=['Sound_Block_Neutral_maxAmp_Cz',
        'Sound_Block_Buzz_maxAmp_Cz'],

        var_name='blocks', value_name='sound_maxAmp_Cz')

data2 = data2.replace(             
   ['Sound_Block_Neutral_maxAmp_Cz', 
    'Sound_Block_Buzz_maxAmp_Cz', 
     ],
                                  
   ['neutral_block',
    'buzz_block',
    ]
   )

data2.to_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\max_amp_sounds_long.csv', index = None, header=True)

#latency_max_amp_targets

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\latency_max_amp_targets.csv')


data2 =  pd.melt(data, id_vars=['participant'], value_vars=['Target_Block_Nodis_latency_Pz',
        'Target_Block_Buzz_latency_Pz','Target_Block_Neutral_latency_Pz'],

        var_name='blocks', value_name='latency_target_maxAmp_Pz')

data2 = data2.replace(             
   ['Target_Block_Neutral_latency_Pz', 
    'Target_Block_Buzz_latency_Pz', 
    'Target_Block_Nodis_latency_Pz'],
                                  
   ['neutral_block',
    'buzz_block',
    'nodis_block']
   )

data2.to_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\latency_max_amp_targets_long.csv', index = None, header=True)


#latency_max_amp_sounds

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\latency_max_amp_sounds.csv')


data2 =  pd.melt(data, id_vars=['participant'], value_vars=['Sound_Block_Buzz_latency_Cz',
        'Sound_Block_Neutral_latency_Cz'],

        var_name='blocks', value_name='sounds_latency_Cz')

data2 = data2.replace(             
   ['Sound_Block_Neutral_latency_Cz', 
    'Sound_Block_Buzz_latency_Cz'],
                                  
   ['neutral_block',
    'buzz_block']
   )

data2.to_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\latency_max_amp_sounds_long.csv', index = None, header=True)


#Concat long format ERP data
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\Long_format\latency_max_amp_sounds_long.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\Long_format\latency_max_amp_targets_long.csv')
dat3 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\Long_format\max_amp_sounds_long.csv')
dat4 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\Long_format\max_amp_targets_long.csv')

dat=[dat1,dat2,dat3,dat4]

master_ERP=pd.concat([dat1,dat2,dat3,dat4],sort=False, ignore_index=True)

#Concat it with the behavioural data
dat5 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_behavioural_long.csv')
dat5=dat5.drop(columns=['Unnamed: 0'])
master_data=pd.concat([master_ERP,dat5],sort=False, ignore_index=True)

master_data.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long.csv', index = None, header=True)



#Merge wide format ERP data
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\latency_max_amp_sounds.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\latency_max_amp_targets.csv')
dat3 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\max_amp_sounds.csv')
dat4 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\data_amplitudes\max_amp_targets.csv')

dat=[dat1,dat2,dat3,dat4]


merg=dat1.merge(dat2)
merg2=merg.merge(dat3)
merg3=merg2.merge(dat4)

#Merge it with the behavioural data
dat5 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_behavioural_wide.csv')
dat5=dat5.drop(columns=['Unnamed: 0'])
master_data=merg3.merge(dat5)
master_data=master_data.drop(columns=['Unnamed: 0'])

master_data.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide.csv', index = None, header=True)

#Concat long format master data with  MobileDna data
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\MobileDNA\socialmedia_mean_allmerged_5days.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\MobileDNA\appevents_mean_allmerged_5days.csv')
dat3 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long.csv')

master_data=pd.concat([dat3,dat1,dat2],sort=False, ignore_index=True)

master_data.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv', index = None, header=True)





#Merge wide format master data with socialmedia MobileDna data
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\MobileDNA\socialmedia_mean_allmerged_5days.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide.csv')

merg=dat1.merge(dat2)

merg.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv', index = None, header=True)

#Merge wide format master data with screentime MobileDna data
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\MobileDNA\appevents_mean_allmerged_5days.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')

merg=dat1.merge(dat2)

merg.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv', index = None, header=True)


#power estimates to long format alpha

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_alpha.csv')


data1 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_AlphaPowerDecLogP1',
        
        'buzz_AlphaPowerDecLogP1','neutral_AlphaPowerDecLogP1'],

        var_name='blocks', value_name='AlphaPowerDecLogP1')

data2 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_AlphaPowerDecLogP2',
        
        'buzz_AlphaPowerDecLogP2','neutral_AlphaPowerDecLogP2'],

        var_name='blocks', value_name='AlphaPowerDecLogP2')

data3 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_AlphaPowerDecLogPz',
        
        'buzz_AlphaPowerDecLogPz','neutral_AlphaPowerDecLogPz'],

        var_name='blocks', value_name='AlphaPowerDecLogPz')

data4 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_AlphaPowerDecLogPOz',
        
        'buzz_AlphaPowerDecLogPOz','neutral_AlphaPowerDecLogPOz'],

        var_name='blocks', value_name='AlphaPowerDecLogPOz')

data5 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_alpha_rel_powerP1',
        
        'buzz_alpha_rel_powerP1','neutral_alpha_rel_powerP1'],

        var_name='blocks', value_name='alpha_rel_powerP1')

data6 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_alpha_rel_powerP2',
        
        'buzz_alpha_rel_powerP2','neutral_alpha_rel_powerP2'],

        var_name='blocks', value_name='alpha_rel_powerP2')

data7 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_alpha_rel_powerPz',
        
        'buzz_alpha_rel_powerPz','neutral_alpha_rel_powerPz'],

        var_name='blocks', value_name='alpha_rel_powerPz')

data8 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_alpha_rel_powerPOz',
        
        'buzz_alpha_rel_powerPOz','neutral_alpha_rel_powerPOz'],

        var_name='blocks', value_name='alpha_rel_powerPOz')

data9 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_alpha_powerP1',
        
        'buzz_abs_alpha_powerP1','neutral_abs_alpha_powerP1'],

        var_name='blocks', value_name='alpha_abs_powerP1')

data10 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_alpha_powerP2',
        
        'buzz_abs_alpha_powerP2','neutral_abs_alpha_powerP2'],

        var_name='blocks', value_name='alpha_abs_powerP2')

data11 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_alpha_powerPz',
        
        'buzz_abs_alpha_powerPz','neutral_abs_alpha_powerPz'],

        var_name='blocks', value_name='alpha_abs_powerPz')

data12 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_alpha_powerPOz',
        
        'buzz_abs_alpha_powerPOz','neutral_abs_alpha_powerPOz'],

        var_name='blocks', value_name='alpha_abs_powerPOz')


data13 =  pd.melt(data, id_vars=['participant'], value_vars=['parietal_nodis_AlphaPowerDecLog',
        
        'parietal_buzz_AlphaPowerDecLog','parietal_neutral_AlphaPowerDecLog'],

        var_name='blocks', value_name='parietal_AlphaPowerDecLog')

data14 =  pd.melt(data, id_vars=['participant'], value_vars=['parietal_nodis_alpha_rel_power',
        
        'parietal_buzz_alpha_rel_power','parietal_neutral_alpha_rel_power'],

        var_name='blocks', value_name='parietal_alpha_rel_power')

data15 =  pd.melt(data, id_vars=['participant'], value_vars=['parietal_nodis_alpha_abs_power',
        
        'parietal_buzz_alpha_abs_power','parietal_neutral_alpha_abs_power'],

        var_name='blocks', value_name='parietal_alpha_abs_power')

data16 =  pd.melt(data, id_vars=['participant'], value_vars=['parietal_neutral_log_psd_alpha_power',
        
        'parietal_nodis_log_psd_alpha_power','parietal_buzz_log_psd_alpha_power'],

        var_name='blocks', value_name='parietal_log_psd_alpha_power')

data17 =  pd.melt(data, id_vars=['participant'], value_vars=['parietal_neutral_declog_psd_alpha_power',
        
        'parietal_buzz_declog_psd_alpha_power','parietal_nodis_declog_psd_alpha_power'],

        var_name='blocks', value_name='parietal_declog_psd_alpha_power')

data18 =  pd.melt(data, id_vars=['participant'], value_vars=['neutral_declog_psd_alpha_powerPz',
        
        'buzz_declog_psd_alpha_powerPz','nodis_declog_psd_alpha_powerPz'],

        var_name='blocks', value_name='declog_psd_alpha_powerPz')

data19 =  pd.melt(data, id_vars=['participant'], value_vars=['neutral_log_psd_alpha_powerPz',
        
        'nodis_log_psd_alpha_powerPz','buzz_log_psd_alpha_powerPz'],

        var_name='blocks', value_name='log_psd_alpha_powerPz')






freq=pd.concat([data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15,data16,data17,data18,data19],sort=False, ignore_index=True)





freq = freq.replace(             
   ['nodis_AlphaPowerDecLogP1',
    'nodis_AlphaPowerDecLogP2',
    'nodis_AlphaPowerDecLogPz',
    'nodis_AlphaPowerDecLogPOz',
    'nodis_alpha_rel_powerP1',
    'nodis_alpha_rel_powerP2',
    'nodis_alpha_rel_powerPz',
    'nodis_alpha_rel_powerPOz',
    'nodis_abs_alpha_powerP1',
    'nodis_abs_alpha_powerP2',
    'nodis_abs_alpha_powerPz',
    'nodis_abs_alpha_powerPOz',
    'parietal_nodis_AlphaPowerDecLog',
    'parietal_nodis_alpha_rel_power',
    'parietal_nodis_alpha_abs_power',
    'parietal_nodis_log_psd_alpha_power',
    'parietal_nodis_declog_psd_alpha_power',
    'nodis_declog_psd_alpha_powerPz',
    'nodis_log_psd_alpha_powerPz',
    
    ],
                                  
    ['nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',])

freq = freq.replace(             
   ['buzz_AlphaPowerDecLogP1',
    'buzz_AlphaPowerDecLogP2',
    'buzz_AlphaPowerDecLogPz',
    'buzz_AlphaPowerDecLogPOz',
    'buzz_alpha_rel_powerP1',
    'buzz_alpha_rel_powerP2',
    'buzz_alpha_rel_powerPz',
    'buzz_alpha_rel_powerPOz',
    'buzz_abs_alpha_powerP1',
    'buzz_abs_alpha_powerP2',
    'buzz_abs_alpha_powerPz',
    'buzz_abs_alpha_powerPOz',
    'parietal_buzz_AlphaPowerDecLog',
    'parietal_buzz_alpha_rel_power',
    'parietal_buzz_alpha_abs_power',
    'parietal_buzz_log_psd_alpha_power',
    'parietal_buzz_declog_psd_alpha_power',
    'buzz_declog_psd_alpha_powerPz',
    'buzz_log_psd_alpha_powerPz',
    ],
                                  
    ['buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     ])

freq = freq.replace(             
   ['neutral_AlphaPowerDecLogP1',
    'neutral_AlphaPowerDecLogP2',
    'neutral_AlphaPowerDecLogPz',
    'neutral_AlphaPowerDecLogPOz',
    'neutral_alpha_rel_powerP1',
    'neutral_alpha_rel_powerP2',
    'neutral_alpha_rel_powerPz',
    'neutral_alpha_rel_powerPOz',
    'neutral_abs_alpha_powerP1',
    'neutral_abs_alpha_powerP2',
    'neutral_abs_alpha_powerPz',
    'neutral_abs_alpha_powerPOz',
    'parietal_neutral_AlphaPowerDecLog',
    'parietal_neutral_alpha_rel_power',
    'parietal_neutral_alpha_abs_power',
    'parietal_neutral_log_psd_alpha_power',
    'parietal_neutral_declog_psd_alpha_power',
    'neutral_declog_psd_alpha_powerPz',
    'neutral_log_psd_alpha_powerPz',
    ],
                                  
    ['neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     ])


#Concat long format master data with  power estimates
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv')
#dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\MobileDNA\appevents_mean_allmerged_5days.csv')

master_data=pd.concat([dat1,freq],sort=False, ignore_index=True)

master_data.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv', index = None, header=True)     

info = master_data.describe()    

#Create long format with baseline block for plot

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_alpha.csv')

data1 =  pd.melt(data, id_vars=['participant'], value_vars=['parietal_baseline_alpha_abs_power',
        
        'parietal_buzz_alpha_abs_power','parietal_neutral_alpha_abs_power','parietal_nodis_alpha_abs_power'],

        var_name='blocks', value_name='parietal_abs_alpha_power')

data2 =  pd.melt(data, id_vars=['participant'], value_vars=['baseline_abs_alpha_powerPz',
        
        'neutral_abs_alpha_powerPz','nodis_abs_alpha_powerPz','buzz_abs_alpha_powerPz'],

        var_name='blocks', value_name='abs_alpha_powerPz')

data3 =  pd.melt(data, id_vars=['participant'], value_vars=['parietal_buzz_log_psd_alpha_power',
        
        'parietal_nodis_log_psd_alpha_power','parietal_neutral_log_psd_alpha_power','parietal_baseline_log_psd_alpha_power'],

        var_name='blocks', value_name='parietal_log_psd_alpha_power')

data4 =  pd.melt(data, id_vars=['participant'], value_vars=['baseline_log_psd_alpha_powerPz',
        
        'neutral_log_psd_alpha_powerPz','nodis_log_psd_alpha_powerPz','buzz_log_psd_alpha_powerPz'],

        var_name='blocks', value_name='Pz_psd_log_alpha_power')



freqbase=pd.concat([data1,data2,data3,data4],sort=False, ignore_index=True)


freqbase = freqbase.replace(             
   ['parietal_baseline_alpha_abs_power',
    'baseline_abs_alpha_powerPz',
    'parietal_baseline_log_psd_alpha_power',
    'baseline_log_psd_alpha_powerPz',   
    
    'parietal_buzz_alpha_abs_power',
    'buzz_abs_alpha_powerPz',
    'parietal_buzz_log_psd_alpha_power',
    'buzz_log_psd_alpha_powerPz',
    
    'parietal_neutral_alpha_abs_power',
    'neutral_abs_alpha_powerPz',
    'parietal_neutral_log_psd_alpha_power',
    'neutral_log_psd_alpha_powerPz',    
    
    'parietal_nodis_alpha_abs_power',
    'nodis_abs_alpha_powerPz',
    'parietal_nodis_log_psd_alpha_power',
    'nodis_log_psd_alpha_powerPz',   
    
    
    ],
                                  
    ['baseline',
     'baseline',
     'baseline',
     'baseline',
     
     'buzz',
     'buzz',
     'buzz',
     'buzz',
     
     'neutral',
     'neutral',
     'neutral',
     'neutral',
     
     'nodis',
     'nodis',
     'nodis',
     'nodis',

     ])
freqbase.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\freq_long_with_baseline.csv', index = None, header=True)     


#Merge wide format master data with alpha 
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_alpha.csv')

merg=dat1.merge(dat2)

merg.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv', index = None, header=True)


#power estimates to long format frontal THETA

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_theta.csv')


data1 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_thetaPowerDecLogF1',
        
        'buzz_thetaPowerDecLogF1','neutral_thetaPowerDecLogF1'],

        var_name='blocks', value_name='thetaPowerDecLogF1')

data2 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_thetaPowerDecLogF2',
        
        'buzz_thetaPowerDecLogF2','neutral_thetaPowerDecLogF2'],

        var_name='blocks', value_name='thetaPowerDecLogF2')

data3 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_thetaPowerDecLogFz',
        
        'buzz_thetaPowerDecLogFz','neutral_thetaPowerDecLogFz'],

        var_name='blocks', value_name='thetaPowerDecLogFz')

data4 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_thetaPowerDecLogAFz',
        
        'buzz_thetaPowerDecLogAFz','neutral_thetaPowerDecLogAFz'],

        var_name='blocks', value_name='thetaPowerDecLogAFz')

data5 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_theta_rel_powerF1',
        
        'buzz_theta_rel_powerF1','neutral_theta_rel_powerF1'],

        var_name='blocks', value_name='theta_rel_powerF1')

data6 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_theta_rel_powerF2',
        
        'buzz_theta_rel_powerF2','neutral_theta_rel_powerF2'],

        var_name='blocks', value_name='theta_rel_powerF2')

data7 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_theta_rel_powerFz',
        
        'buzz_theta_rel_powerFz','neutral_theta_rel_powerFz'],

        var_name='blocks', value_name='theta_rel_powerFz')

data8 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_theta_rel_powerAFz',
        
        'buzz_theta_rel_powerAFz','neutral_theta_rel_powerAFz'],

        var_name='blocks', value_name='theta_rel_powerAFz')

data9 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_theta_powerF1',
        
        'buzz_abs_theta_powerF1','neutral_abs_theta_powerF1'],

        var_name='blocks', value_name='theta_abs_powerF1')

data10 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_theta_powerF2',
        
        'buzz_abs_theta_powerF2','neutral_abs_theta_powerF2'],

        var_name='blocks', value_name='theta_abs_powerF2')

data11 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_theta_powerFz',
        
        'buzz_abs_theta_powerFz','neutral_abs_theta_powerFz'],

        var_name='blocks', value_name='theta_abs_powerFz')

data12 =  pd.melt(data, id_vars=['participant'], value_vars=['nodis_abs_theta_powerAFz',
        
        'buzz_abs_theta_powerAFz','neutral_abs_theta_powerAFz'],

        var_name='blocks', value_name='theta_abs_powerAFz')


data13 =  pd.melt(data, id_vars=['participant'], value_vars=['frontal_nodis_thetaPowerDecLog',
        
        'frontal_buzz_thetaPowerDecLog','frontal_neutral_thetaPowerDecLog'],

        var_name='blocks', value_name='frontal_thetaPowerDecLog')

data14 =  pd.melt(data, id_vars=['participant'], value_vars=['frontal_nodis_theta_rel_power',
        
        'frontal_buzz_theta_rel_power','frontal_neutral_theta_rel_power'],

        var_name='blocks', value_name='frontal_theta_rel_power')

data15 =  pd.melt(data, id_vars=['participant'], value_vars=['frontal_nodis_theta_abs_power',
        
        'frontal_buzz_theta_abs_power','frontal_neutral_theta_abs_power'],

        var_name='blocks', value_name='frontal_theta_abs_power')

data16 =  pd.melt(data, id_vars=['participant'], value_vars=['frontal_neutral_log_psd_theta_power',
        
        'frontal_nodis_log_psd_theta_power','frontal_buzz_log_psd_theta_power'],

        var_name='blocks', value_name='frontal_log_psd_theta_power')

data17 =  pd.melt(data, id_vars=['participant'], value_vars=['frontal_neutral_declog_psd_theta_power',
        
        'frontal_buzz_declog_psd_theta_power','frontal_nodis_declog_psd_theta_power'],

        var_name='blocks', value_name='frontal_declog_psd_theta_power')

data18 =  pd.melt(data, id_vars=['participant'], value_vars=['neutral_declog_psd_theta_powerFz',
        
        'buzz_declog_psd_theta_powerFz','nodis_declog_psd_theta_powerFz'],

        var_name='blocks', value_name='declog_psd_theta_powerFz')

data19 =  pd.melt(data, id_vars=['participant'], value_vars=['neutral_log_psd_theta_powerFz',
        
        'nodis_log_psd_theta_powerFz','buzz_log_psd_theta_powerFz'],

        var_name='blocks', value_name='log_psd_theta_powerFz')






freq=pd.concat([data1,data2,data3,data4,data5,data6,data7,data8,data9,data10,data11,data12,data13,data14,data15,data16,data17,data18,data19],sort=False, ignore_index=True)





freq = freq.replace(             
   ['nodis_thetaPowerDecLogF1',
    'nodis_thetaPowerDecLogF2',
    'nodis_thetaPowerDecLogFz',
    'nodis_thetaPowerDecLogAFz',
    'nodis_theta_rel_powerF1',
    'nodis_theta_rel_powerF2',
    'nodis_theta_rel_powerFz',
    'nodis_theta_rel_powerAFz',
    'nodis_abs_theta_powerF1',
    'nodis_abs_theta_powerF2',
    'nodis_abs_theta_powerFz',
    'nodis_abs_theta_powerAFz',
    'frontal_nodis_thetaPowerDecLog',
    'frontal_nodis_theta_rel_power',
    'frontal_nodis_theta_abs_power',
    'frontal_nodis_log_psd_theta_power',
    'frontal_nodis_declog_psd_theta_power',
    'nodis_declog_psd_theta_powerFz',
    'nodis_log_psd_theta_powerFz',
    
    ],
                                  
    ['nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',
     'nodis_block',])

freq = freq.replace(             
   ['buzz_thetaPowerDecLogF1',
    'buzz_thetaPowerDecLogF2',
    'buzz_thetaPowerDecLogFz',
    'buzz_thetaPowerDecLogAFz',
    'buzz_theta_rel_powerF1',
    'buzz_theta_rel_powerF2',
    'buzz_theta_rel_powerFz',
    'buzz_theta_rel_powerAFz',
    'buzz_abs_theta_powerF1',
    'buzz_abs_theta_powerF2',
    'buzz_abs_theta_powerFz',
    'buzz_abs_theta_powerAFz',
    'frontal_buzz_thetaPowerDecLog',
    'frontal_buzz_theta_rel_power',
    'frontal_buzz_theta_abs_power',
    'frontal_buzz_log_psd_theta_power',
    'frontal_buzz_declog_psd_theta_power',
    'buzz_declog_psd_theta_powerFz',
    'buzz_log_psd_theta_powerFz',
    ],
                                  
    ['buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     'buzz_block',
     ])

freq = freq.replace(             
   ['neutral_thetaPowerDecLogF1',
    'neutral_thetaPowerDecLogF2',
    'neutral_thetaPowerDecLogFz',
    'neutral_thetaPowerDecLogAFz',
    'neutral_theta_rel_powerF1',
    'neutral_theta_rel_powerF2',
    'neutral_theta_rel_powerFz',
    'neutral_theta_rel_powerAFz',
    'neutral_abs_theta_powerF1',
    'neutral_abs_theta_powerF2',
    'neutral_abs_theta_powerFz',
    'neutral_abs_theta_powerAFz',
    'frontal_neutral_thetaPowerDecLog',
    'frontal_neutral_theta_rel_power',
    'frontal_neutral_theta_abs_power',
    'frontal_neutral_log_psd_theta_power',
    'frontal_neutral_declog_psd_theta_power',
    'neutral_declog_psd_theta_powerFz',
    'neutral_log_psd_theta_powerFz',
    ],
                                  
    ['neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     'neutral_block',
     ])


#Concat long format master data with  power estimates
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv')
#dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\MobileDNA\appevents_mean_allmerged_5days.csv')

master_data=pd.concat([dat1,freq],sort=False, ignore_index=True)

master_data.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv', index = None, header=True)     

info = master_data.describe()    

#Create long format with baseline block for plot

data = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_theta.csv')

data1 =  pd.melt(data, id_vars=['participant'], value_vars=['frontal_baseline_theta_abs_power',
        
        'frontal_buzz_theta_abs_power','frontal_neutral_theta_abs_power','frontal_nodis_theta_abs_power'],

        var_name='blocks', value_name='frontal_abs_theta_power')

data2 =  pd.melt(data, id_vars=['participant'], value_vars=['baseline_abs_theta_powerFz',
        
        'neutral_abs_theta_powerFz','nodis_abs_theta_powerFz','buzz_abs_theta_powerFz'],

        var_name='blocks', value_name='abs_theta_powerFz')

data3 =  pd.melt(data, id_vars=['participant'], value_vars=['frontal_buzz_log_psd_theta_power',
        
        'frontal_nodis_log_psd_theta_power','frontal_neutral_log_psd_theta_power','frontal_baseline_log_psd_theta_power'],

        var_name='blocks', value_name='frontal_log_psd_theta_power')

data4 =  pd.melt(data, id_vars=['participant'], value_vars=['baseline_log_psd_theta_powerFz',
        
        'neutral_log_psd_theta_powerFz','nodis_log_psd_theta_powerFz','buzz_log_psd_theta_powerFz'],

        var_name='blocks', value_name='Fz_psd_log_theta_power')



freqbase=pd.concat([data1,data2,data3,data4],sort=False, ignore_index=True)


freqbase = freqbase.replace(             
   ['frontal_baseline_theta_abs_power',
    'baseline_abs_theta_powerFz',
    'frontal_baseline_log_psd_theta_power',
    'baseline_log_psd_theta_powerFz',   
    
    'frontal_buzz_theta_abs_power',
    'buzz_abs_theta_powerFz',
    'frontal_buzz_log_psd_theta_power',
    'buzz_log_psd_theta_powerFz',
    
    'frontal_neutral_theta_abs_power',
    'neutral_abs_theta_powerFz',
    'frontal_neutral_log_psd_theta_power',
    'neutral_log_psd_theta_powerFz',    
    
    'frontal_nodis_theta_abs_power',
    'nodis_abs_theta_powerFz',
    'frontal_nodis_log_psd_theta_power',
    'nodis_log_psd_theta_powerFz',   
    
    
    ],
                                  
    ['baseline',
     'baseline',
     'baseline',
     'baseline',
     
     'buzz',
     'buzz',
     'buzz',
     'buzz',
     
     'neutral',
     'neutral',
     'neutral',
     'neutral',
     
     'nodis',
     'nodis',
     'nodis',
     'nodis',

     ])
freqbase.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\freq_long_with_baseline_theta.csv', index = None, header=True)     

#Merge wide format master data with theta
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_theta.csv')

merg=dat1.merge(dat2)

merg.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv', index = None, header=True)

