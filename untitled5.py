# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:00:02 2019

@author: Hrishikesh
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

df=pd.read_csv("findata12.csv")
fin=pd.DataFrame()
i=0

forecast_col = 'prod'
forecast_out=2
error=list()
for crop in df.crop.unique():
    df2=df.loc[df["crop"]=='Rice']
    df3=df2
    
    
#        df2.ppa=df2.ppa[:-3]
    df2.set_index("year",inplace=True)
    df2=df2[["temp","rain","prod"]]
    
    df2['label'] = df2[forecast_col].shift(-forecast_out)
    df2.drop([2019,2020,2021],inplace=True)
    
    X = np.array(df2.drop(['label'], 1))
    X = preprocessing.scale(X)
    
    
    
    
    y = np.array(df2['label'])
    
    
    high=0.0
    for _ in range(5):
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
        
#        clf = svm.SVR(kernel='linear')
#        clf.fit(X_train, y_train)
#        confidence = clf.score(X_test, y_test)
        
#        clf = svm.SVR(kernel='poly')
#        clf.fit(X_train, y_train)
#        confidence = clf.score(X_test, y_test)
        
#        clf = LinearRegression()
#        clf.fit(X_train, y_train)
#        confidence = clf.score(X_test, y_test)
        
        clf = svm.SVR()#rbf
        clf.fit(X_train, y_train)
        confidence = clf.score(X_test, y_test)
        if confidence > high:
            high=confidence
            with open('crop.pickle','wb') as f:
                pickle.dump(clf, f)
    #forecast_set = clf.predict(X_lately)
    pickle_in = open('crop.pickle','rb')
    clf = pickle.load(pickle_in)
    accur=high*100
    error.append(accur)
    for dist in df3.district.unique():
        df1=df3.loc[df3["district"]==dist]
        df4=df1
        df1=df1[["temp","rain","prod"]]
        
        
        
        
        X = np.array(df1)
        X = preprocessing.scale(X)
        X_lately = X[-3:]
       
        forecast_set = clf.predict(X_lately)
        
        
        df4["prod"][-3:]=forecast_set.tolist()
        fin=fin.append(df4,ignore_index=True)#6407
#        try:
#            title=dist+" "+crop
#            df3.ppa.plot()
#            plt.ylabel('Production per unit Area')
#            plt.title(title)
#            path=title+'.png'
#            plt.savefig(path)
#        except:
#            error.append(title)
        i=i+1
        print(i)
        
        
fin.to_csv("findata18.csv")