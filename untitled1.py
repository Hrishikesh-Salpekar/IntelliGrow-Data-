# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 19:57:01 2019

@author: Hrishikesh
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style

df=pd.read_csv("combined5.csv")
fin=pd.DataFrame()
i=0
fin_crop=fin.Crop.unique()
fin_dist=fin.District_Name.unique()
forecast_col = 'ppa'
forecast_out=3
error=list()
for crop in df.Crop.unique():
    df1=df.loc[df["Crop"]==crop]
    for dist in df1.District_Name.unique():
        df2=df1.loc[df1["District_Name"]==dist]
        if crop in fin_crop and dist in fin_dist:
            i=i+1
            print(i)
            continue
        df3=df2
        
#        df2.ppa=df2.ppa[:-3]
        df2.set_index("YEAR",inplace=True)
        df2=df2[["Mean_Temp","Rain","ppa"]]
        
        df2['label'] = df2[forecast_col].shift(-forecast_out)
        
        
        X = np.array(df2.drop(['label'], 1))
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]
        
        df2.dropna(inplace=True)
        
        y = np.array(df2['label'])
        
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
        clf = LinearRegression(n_jobs=-1)
        clf.fit(X_train, y_train)
        confidence = clf.score(X_test, y_test)
        
        forecast_set = clf.predict(X_lately)
        
        df3.ppa[-forecast_out:]=forecast_set.tolist()
        fin=fin.append(df3,ignore_index=True)#6407
        try:
            title=dist+" "+crop
            df3.ppa.plot()
            plt.ylabel('Production per unit Area')
            plt.title(title)
            path=title+'.png'
            plt.savefig(path)
        except:
            error.append(title)
        i=i+1
        print(i)
        
        
fin.to_csv("findata10.csv")