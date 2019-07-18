# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:13:46 2019

@author: Hrishikesh
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import pickle
from math import avg

df=pd.read_csv("findata12.csv")
fin=pd.DataFrame()
i=0

forecast_col = 'prod'
forecast_out=3
error_fin=list()
for crop in df.crop.unique():
    df1=df.loc[df["crop"]=='Maize']
    error=list()
    for dist in df1.district.unique():
        df2=df1.loc[df1["district"]=='Nashik']
        df3=df2
        
        df2.set_index("year",inplace=True)
        df2=df2[["temp","rain","prod"]]
        
        df2['label'] = df2[forecast_col].shift(-forecast_out)
        
        df2=df2[["temp","rain","label"]]
        
        X = np.array(df2.drop(['label'], 1))
        X = preprocessing.scale(X)
        X_lately = X[-forecast_out:]
        X = X[:-forecast_out]
        
        df2.dropna(inplace=True)
        high=0.0
        y = np.array(df2['label'])
        for _ in range(5):
            X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
            clf = svm.SVR()#rbf
            clf.fit(X_train, y_train)
            confidence = clf.score(X_test, y_test)
            if confidence > high:
                high=confidence
                with open('crop.pickle','wb') as f:
                    pickle.dump(clf, f)
            clf = svm.SVR(kernel='linear')
            clf.fit(X_train, y_train)
            confidence = clf.score(X_test, y_test)
            if confidence > high:
                high=confidence
                with open('crop.pickle','wb') as f:
                    pickle.dump(clf, f)
        clf = LinearRegression()
        clf.fit(X_train, y_train)
        confidence = clf.score(X_test, y_test)
        if confidence > high:
            high=confidence
            with open('crop.pickle','wb') as f:
                pickle.dump(clf, f)
        pickle_in = open('crop.pickle','rb')
        clf = pickle.load(pickle_in)
        forecast_set = clf.predict(X_lately)
        error.extend([high*100])
        df3["prod"][-forecast_out:]=forecast_set.tolist()
        fin=fin.append(df3,ignore_index=True)
        
        i=i+1
        print(i)
        
    error_fin.extend([error])
        
#fin.to_csv("findata100.csv")
sum2=0
for er in error_fin:
    sum2=sum2+(sum(er)/len(er))
accu=sum2/len(error_fin)
