# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 00:11:41 2019

@author: Hrishikesh
"""

import pandas as pd
data=pd.read_csv("apy.csv")
final=pd.DataFrame()
i=0
for dist in data.District_Name.unique():
    d=data.loc[data["District_Name"]==dist]
    for crop in d.Crop.unique():
        c=d.loc[d["Crop"]==crop]
        for yr in c.Crop_Year.unique():
            y=c.loc[c["Crop_Year"]==yr]
            state=y.State_Name.tolist()[0]
            dis=y.District_Name.tolist()[0]
            year=y.Crop_Year.tolist()[0]
            cr=y.Crop.tolist()[0]
            ar=sum(y.Area)
            prod=sum(y.Production)
            fin=pd.DataFrame({"State_Name":state,"District_Name":dis,"Crop_Year":year,"Crop":cr,"Area":ar,"Production":prod},index=["0"])
            final=final.append(fin)
            print(i)
            i=i+1
