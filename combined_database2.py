# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 00:24:21 2018

@author: Hrishikesh
"""

import pandas as pd
mergedBD=pd.read_csv("MergedDB1.csv")
print(mergedBD.head())
mergedBD=mergedBD[["ANNUAL","Area","Crop","District_Name","Production","Season","YEAR"]]
print(mergedBD.head())
mergedBD.to_csv("MergedDB1.csv")