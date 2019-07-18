# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 18:37:06 2019

@author: Hrishikesh
"""

import random
import pandas as pd
df=pd.read_csv("Mean_Temp_IMD_2017.csv")
Crop=pd.read_csv("apy2.csv")
Rain=pd.read_csv("Future_Rain.csv")
df=df[["YEAR","ANNUAL"]]
#df=df.append({"YEAR":2018,"ANNUAL":25.42},ignore_index=True)
#df=df.append({"YEAR":2019,"ANNUAL":26.62},ignore_index=True)
#df=df.append({"YEAR":2020,"ANNUAL":24.57},ignore_index=True)
temp=df
i=0
final=pd.DataFrame()
for crop in Crop.Crop.unique():
    df1=Crop.loc[Crop["Crop"]==crop]
    for dist in df1.District_Name.unique():
        df2=df1.loc[df1["District_Name"]==dist]
        first=df2.Crop_Year.tolist()[0]
        last=df2.Crop_Year.tolist()[-1]
        if first > 2000:
            continue
        if last < 2013:
            continue
        final=final.append(df2,ignore_index=True)
        print(i)
        i=i+1
        
        
newdf=pd.DataFrame()        
for crop in final.Crop.unique():
    df1=final.loc[final["Crop"]==crop]
    for dist in df1.District_Name.unique():
        df2=df1.loc[df1["District_Name"]==dist]
        q=df2['ppa'].max()
        w=df2['ppa'].min()
        
       # print(df['Production'])
        df2.fillna(random.randint(int(w),int(q)),inplace=True)
        newdf=newdf.append(df2,ignore_index=True)
        
for crop in final.Crop.unique():
    df1=final.loc[final["Crop"]==crop]
    for dist in df1.District_Name.unique():
        df2=df1.loc[df1["District_Name"]==dist]
