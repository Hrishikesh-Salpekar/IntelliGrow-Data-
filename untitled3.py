# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 22:36:57 2019

@author: Hrishikesh
"""

import pandas as pd
import random
from statistics import mean

def pred(ppa,yr):
    last=yr[-1]
    x=mean(yr)
    y=mean(ppa)
    xy=mean([a*b for a,b in zip(yr,ppa)])
    x2=x**2
    X2=mean([a*a for a in yr])
    m=((x*y)-xy)/(x2-X2)
    b=y-m*x
    forecast=list()
    for x in range(last,2021):
        yh=m*x+b
        forecast.append(yh)
        
    return forecast
    
    

df=pd.read_csv("apy6.csv")
df["ppa"]=df["Production"]/df["Area"]
newdf=pd.DataFrame()        
i=0
for crop in df.Crop.unique():
    df1=df.loc[df["Crop"]==crop]
    for dist in df1.District_Name.unique():
        df2=df1.loc[df1["District_Name"]==dist]
        q=df2['ppa'].max()
        w=df2['ppa'].min()
        
       # print(df['Production'])
        df2.fillna(random.randint(int(w),int(q)),inplace=True)
        newdf=newdf.append(df2,ignore_index=True)
        print(i)
        i=i+1

final=pd.DataFrame()
k=0 #8635
for crop in newdf.Crop.unique():
    df1=newdf.loc[newdf["Crop"]==crop]
    for dist in df1.District_Name.unique():
        df2=df1.loc[df1["District_Name"]==dist]
        k=k+1
        df2=df2[["Crop","Crop_Year","District_Name","State_Name","ppa"]]
        last=df2.Crop_Year.tolist()[-1]
        state=df2.State_Name.tolist()[-1]
        ppa=df2.ppa.tolist()
        forecast=pred(ppa,df2.Crop_Year.tolist())
        mi=min(ppa)
        ma=max(ppa)
        err=0.01*(ma-mi)
        final=final.append(df2)
        j=1
        for i in forecast:
            rand=random.randint(0,10)
            error=err*rand
            yh=i+error
            year=last+j
            final=final.append(pd.DataFrame({"Crop":crop,"Crop_Year":year,"District_Name":dist,"State_Name":state,"ppa":yh},index=['0']),ignore_index=True)
            j=j+1
        print(k)
        
        
