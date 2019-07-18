
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 15:10:09 2018

@author: Hrishikesh
"""
import datetime
import warnings
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
from matplotlib import style
style.use ('ggplot')

def mod(val):
    if val<0:
        return -1*val
    else:
        return val
def MAPE(test,predictions):
    sum=0.0
    n=len(predictions)
    for i in range(n):
        sum=sum+(mod(test[i]-predictions[i])/test[i])
    error=sum*100/n
    return error
def evaluate_arima_model(X, arima_order):
    size=int(len(X))
    test_size=int(0.3*size)
    train,test=X[0:-test_size],X[-test_size:]
    history=[x for x in train]
    predictions = list()
    for t in range(test_size):
        model = ARIMA(history,order=arima_order)
        model_fit=model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        yh=yhat[0]
        predictions.append(yh)
        history.append(test[t])
    error=MAPE(test,predictions)
    return error

def evaluate_models(dataset, p_values, d_values, q_values):
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order=(p,d,q)
                try:
                    mpe = evaluate_arima_model(dataset,order)
                    if mpe<best_score:
                        best_score,best_cfg=mpe,order
                    print("ARIMA%s MAPE=%.3f" %(order,mpe))
                except:
                    continue
    return best_cfg,best_score

df=pd.read_csv("India_Rainfall.csv")
fin=pd.DataFrame()
p_values=range(0,5)
d_values=range(0,5)
q_values=range(0,5)
warnings.filterwarnings("ignore")
for sub in df.SUBDIVISION.unique():
    df1=df.loc[df['SUBDIVISION']==sub]
    series=pd.Series(df1.ANNUAL.tolist())

    cfg,error=evaluate_models(series.values,p_values,d_values,q_values)
    try:
        history=[x for x in series]
        predictions=list()
        for t in range(4):
            model=ARIMA(history,order=cfg)#order=(4,0,4)
            model_fit=model.fit(disp=0)
            yhat=model_fit.forecast()[0]
            yh=mod(yhat[0])
            predictions.append(yh)
            history.append(yh)
    except:
        print("Error")
    df1=df1[['SUBDIVISION','YEAR','ANNUAL']]
    df1=df1.append(pd.DataFrame({'SUBDIVISION':[sub,sub,sub,sub],'YEAR':[2018,2019,2020,2021],'ANNUAL':predictions}))
    fin=fin.append(df1,ignore_index=True)
print(predictions)





#404














