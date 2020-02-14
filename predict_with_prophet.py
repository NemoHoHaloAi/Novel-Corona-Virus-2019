#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet

df_train = pd.read_csv('./data_new/中国.csv', parse_dates=['timestamp'])
df_train['timestamp'] = df_train['timestamp'].apply(lambda ts:pd.Timestamp(int(ts), unit='ms'))
#df_train.sort_values(['timestamp'],inplace=True)

# confirmedCount
df_train_confirmed = df_train[['timestamp','confirmedCount']].copy()
df_train_confirmed = df_train_confirmed.rename(index=str, columns={"timestamp": "ds", "confirmedCount": "y"})
# suspectedCount
df_train_suspected = df_train[['timestamp','suspectedCount']].copy()
df_train_suspected = df_train_suspected.rename(index=str, columns={"timestamp": "ds", "suspectedCount": "y"})
# deadCount
df_train_dead = df_train[['timestamp','deadCount']].copy()
df_train_dead = df_train_dead.rename(index=str, columns={"timestamp": "ds", "deadCount": "y"})
# curedCount
df_train_cured = df_train[['timestamp','curedCount']].copy()
df_train_cured = df_train_cured.rename(index=str, columns={"timestamp": "ds", "curedCount": "y"})

# test
df_test = pd.DataFrame({})
df_test['ds'] = pd.date_range(start=df_train_confirmed.ds.max(), freq="H", periods=24)

m = Prophet()
#m.fit(df_train_confirmed)
m.fit(df_train_suspected)
#m.fit(df_train_dead)
#m.fit(df_train_cured)

forecast = m.predict(pd.concat([df_train_confirmed[['ds']],df_test[['ds']]]))

#print forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
m.plot(forecast)
plt.xlabel('Date')
plt.ylabel('Cured Count')
plt.show()
