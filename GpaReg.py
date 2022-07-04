# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 12:22:08 2022

@author: Kavengi
Date:01/07/2022
topic:linear regression
"""

#==========================LOADING LIBRARIES=================================#
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

#=======================LOADING DATA=========================================#

#loading as is 
spector_data = sm.datasets.spector.load()

#loading as  a dataframe
spect = sm.datasets.spector.load_pandas()['data']

#to add an intercept 
spector_data.exog = sm.add_constant(spector_data.exog, prepend=False)


#============================DESCRIPTIVES====================================#

print(spect.head())
print(spect.tail())

#=======================REGRESSION===========================================#

#Assigning regression object name (mod)
mod = sm.OLS(spector_data.endog, spector_data.exog)


#fitting regression
res = mod.fit()

#regression results
print(res.summary())

#==============================PLOTS========================================#
#GpaScatter.png
spect.plot(x ='TUCE', y='GPA', kind = 'scatter',s=100,color='purple')
plt.title("Scatterplot of GPA vs TUCE")
plt.show()



