# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 01:07:28 2019

@author: Hrishikesh
"""

import pandas as pd
df=pd.read_csv("apy10.csv")
crop=pd.read_csv("apy11.csv")
rain=pd.read_csv("Future_Rain.csv")
temp=pd.read_csv("Mean_Temp_IMD_2017.csv")
#['Assam','Meghalaya','Jammu and Kashmir','Andhra Pradesh','Kerala','Bihar','Chhattisgarh','Goa','Madhya Pradesh','Maharashtra','Nagaland','Tripura','Sikkim','West Bengal','Telangana ','Uttarakhand','Arunachal Pradesh','Dadra and Nagar Haveli','Himachal Pradesh','Uttar Pradesh','Odisha','Tamil Nadu','Punjab','Karnataka','Puducherry']
crop=pd.read_csv("apy11.csv")
comb=pd.read_csv("combined3.csv")
df2=crop.join(temp.set_index("YEAR"),on="YEAR")
df2=df2[["Crop","YEAR","District_Name","State_Name","ppa","ANNUAL"]]
df2.to_csv("combined3.csv")
test=pd.merge(comb,rain,how='left',left_on=["YEAR","State_Name"],right_on=["YEAR","SUBDIVISION"])
test.to_csv("combined4.csv")

test=test[["Crop","YEAR","District_Name","State_Name","ppa","Mean_Temp","ANNUAL"]]
test.to_csv("combined5.csv")