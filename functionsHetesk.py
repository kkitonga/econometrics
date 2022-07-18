# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 06:48:16 2022

@author: Karengi
"""

#==========================IMPORT LIBRARIES==================================#

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.compat import lzip

#==========================LOAD DATA SETS=====================================#

data = sm.datasets.longley.load_pandas()
data1 = sm.datasets.engel.load_pandas()



#=========================DESCRIPTIVES FUNCTION===============================#

def descriptives_ftn (df) :
     print(df.data)
     print(df.names)
     
#calling on descriptives function
descriptives_ftn (data)
descriptives_ftn (data1)

#=============================REGRESSION FUNCTION============================#

#=========1.specifying regression function
def reg_ftn (y,x) :
                  #model specification and fitting
                  model = sm.OLS(y, x).fit()
                  modelSummary = print(model.summary())
                  resid= model.resid
                  #breusch pagan test for heteroskedasticiy
                  bpTestNames = ["lagrange multiplier","p-value",
                                 "f-value","f p-value"]
                  bpTest = np.round(sm.stats.diagnostic.het_breuschpagan
                                    (resid, x),2)               
                  bpTestResults = print((lzip(bpTestNames,bpTest)))
                  

#==========2.calling function on both datasets                 
                  
#1.Regression 1 :calling  defined regression function on dataframe=data
#endogneous and exogenous variables already predefined
reg_ftn(data.endog, data.exog)

#2.Regression 1 :calling  defined regression function on dataframe=data1
#endogenous and exogeneous varaibles already predefined
reg_ftn(data1.endog, data1.exog)

#==================================END=======================================#















