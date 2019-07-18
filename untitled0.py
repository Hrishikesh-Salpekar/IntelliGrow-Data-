# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 12:10:56 2019

@author: Hrishikesh
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np 
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
from statistics import mean
def best_fit_slope(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)**2) - mean(xs**2)))
    return m

df=pd.read_csv("findata10.csv")
df1=df.loc[df["Crop"]=="Cotton(lint)"]
df2=df1.loc[df1["District_Name"]=="LUDHIANA"]
plt.scatter(df2["ppa"],df2["Rain"],label='skitscat', color='k', s=25, marker="o")
plt.xlabel("Yield")
plt.ylabel("Rain")
plt.title("Yield against Rain")
plt.savefig("scatter1.jpg")
def ys(xs,m,b):
    y=list()
    for x in xs:
        y.extend((m*x+b,))
    return y
def plot(district, i):
    df2=df1.loc[df1["District_Name"]==district]
    plt.scatter(df2["ppa"],df2["Mean_Temp"],label='skitscat', color='k', s=25, marker="o")
    plt.xlabel("Yield")
    plt.ylabel("Temperature")
    plt.title("Yield against Temperature")
    m=best_fit_slope(df2["ppa"],df2["Mean_Temp"])
    b = mean(df2["Mean_Temp"].tolist()) - m*mean(df2["ppa"].tolist())
    xs=df2["ppa"].tolist()
    Ys=ys(xs,m,b)
    plt.plot(xs,Ys)
    plt.savefig("scatter"+str(i)+".jpg")
    plt.show()
for i, dis in enumerate(df1.District_Name.unique().tolist()):
    plot(dis,i)
forecast_col = 'prod'
forecast_out=3

df = pd.read_csv('findata12.csv')
df['District_Name'] = df['District_Name'].apply(lambda x : x.lower().title())
df['ppa'] = df['ppa'].apply(lambda x : abs(x) if x > -1 else 0)

df2.set_index("Year",inplace=True)
df2=df2[["Mean_Temp","Rain","ppa"]]
df2['label'] = df2[forecast_col].shift(-forecast_out)
        
        
X = np.array(df2.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]

df2.dropna(inplace=True)

y = np.array(df2['label'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)
clf = svm.SVR(kernel='linear')
clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)
