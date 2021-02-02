from pingouin import mixed_anova, anova, pairwise_tukey
from pingouin import logistic_regression
import pprint
from statsmodels.multivariate.manova import MANOVA
from pingouin import ancova
data_long = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv')
aov_declog = pg.rm_anova(data=data_long, dv='frontal_thetaPowerDecLog', within= 'blocks', subject='participant', detailed=True)

print(aov_declog)
aov_declog = pg.rm_anova(data=data_long, dv='frontal_declog_psd_theta_power', within= 'blocks', subject='participant', detailed=True)

print(aov_declog)
aov_declogFz = pg.rm_anova(data=data_long, dv='Fz_declog_psd_theta_power', within= 'blocks', subject='participant', detailed=True)

print(aov_declogFz)
aov_declogFz = pg.rm_anova(data=data_long, dv='declog_psd_theta_powerFz', within= 'blocks', subject='participant', detailed=True)

print(aov_declogFz)
aov_relpow = pg.rm_anova(data=data_long, dv='frontal_theta_rel_power', within= 'blocks', subject='participant', detailed=True)

print(aov_relpow)
aov_relpowFz = pg.rm_anova(data=data_long, dv='theta_rel_powerFz', within= 'blocks', subject='participant', detailed=True)

print(aov_relpowFz)
X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontall_nodis_thetaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()
dat1 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
dat2 =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\data_frequency_theta.csv')

merg=dat1.merge(dat2)
merg.to_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv', index = None, header=True)
data_wide_mDNA =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
#
X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_nodis_thetaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()
X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_nodis_declog_psd_theta_power"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()
X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_buzz_thetaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()
X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_neutral_thetaPowerDecLog"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()
X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_neutral_declog_psd_thetapower"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()
X = data_wide_mDNA["socialmedia_mean"] ## X usually means our input variables (or independent variables)
y = data_wide_mDNA["frontal_neutral_declog_psd_theta_power"] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
model.summary()

## ---(Fri Mar  6 16:16:26 2020)---
from scipy import stats
import statsmodels.api as sm
import os
import pingouin as pg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels
from scipy.stats import spearmanr
from pingouin import mixed_anova, anova, pairwise_tukey
from pingouin import logistic_regression
import pprint
from statsmodels.multivariate.manova import MANOVA
from pingouin import ancova

#import data in long and wide format for different anlysis
data_long = pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_long_mDNA.csv')
#Exclude participant 26 for ERP analysis as we know that he is way off with amplitudes in this paradigm.
data_long = data_long[data_long.participant != 'P26']
data_long.describe()


data_wide_mDNA =pd.read_csv(r'C:\Users\user\Desktop\FOCUS\behavioral\ready_to_stat\master_data_wide_mDNA.csv')
#Exclude participant 26 for ERP analysis as we know that he is way off with amplitudes in this paradigm.
data_wide_mDNA = data_wide_mDNA[data_wide_mDNA.participant != 'P26']
data_wide_mDNA.describe()
aov_declog = pg.rm_anova(data=data_long, dv='parietal_AlphaPowerDecLog', within= 'blocks', subject='participant', detailed=True,correction=True)

print(aov_declog)