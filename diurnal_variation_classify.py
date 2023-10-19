# -*- coding: utf-8 -*-
"""
Created on Thu May 26 05:12:05 2022

@author: torai
"""
import pandas as pd
import numpy as np
import csv
import pprint
import datetime

#Input data detail
print('Input year of data')
year = input()

print('Input month of data as 2 digits')
month = input()
file_name = 'SLCP' + year + month

nyear = int(year)
nmonth = int(month)

#Read csv file
df = pd.read_csv("../Merged Data/"+ file_name + '.csv')
#print(df)

#PM_df = df.iloc[:,3:4]
#BC_df = df.iloc[:,1:2]
#print(PM_df)
#print(BC_df)

#Season define
season = ''

if nmonth == 3 or nmonth == 4 or nmonth == 5:
    season = 'Spring'
elif nmonth == 6 or nmonth == 7 or nmonth == 8:
    season = 'Summer'
elif nmonth == 9 or nmonth == 10 or nmonth == 11:
    season = 'Autumn'
elif nmonth == 12 or nmonth == 1 or nmonth == 2:
    season = 'Winter'

#print(season)

if season == 'Spring':
    PM_ave = 34.44
    PM_std = 24.16
    PM_err = 0.51708
    
    BC_ave = 2.24
    BC_std = 1.57
    BC_err = 0.04232
elif season == 'Summer':
    PM_ave = 18.39
    PM_std = 12.22
    PM_err = 0.27493
    
    BC_ave = 0.91181
    BC_std = 0.7741
    BC_err = 0.0307
elif season == 'Autumn':
    PM_ave = 37.44
    PM_std = 25.44
    PM_err = 0.54436
    
    BC_ave = 2.62
    BC_std = 2.36
    BC_err = 0.05169
elif season == 'Winter':
    PM_ave = 51.63
    PM_std = 42.84
    PM_err = 1.13845
    
    BC_ave = 2.35
    BC_std = 2.08
    BC_err = 0.06332


#Classify
n = 0
n = int(n)

#df_new = pd.DataFrame(index=range(len(df)),columns=range(1))
df['PM2.5_level'] = np.nan  #11
df['Time_Day'] = np.nan     #12
df['Time_Hour'] = np.nan    #13 
df['Timezone'] = np.nan     #14
df['Traffic'] = np.nan      #15
df['Traffic_Pattern'] = np.nan

while n < len(df):
    if df.iloc[n,3] > 40:
       df.iloc[n,11] = 'High'
    elif df.iloc[n,3] < 30:
         df.iloc[n,11] = 'Low'
    elif 30 <= df.iloc[n,3] <= 40:
         df.iloc[n,11] = 'Middle' 
    n = n+1


#Change to datetime data type
df.iloc[:,0] = pd.to_datetime(df.iloc[:,0])
#print(df.iloc[1,0].hour)

#Define Pattern 
n = 0
n = int(n)


while n < len(df):
    df.iloc[n,12] = int(df.iloc[n,0].day)
    df.iloc[n,13] = int(df.iloc[n,0].hour)
    
    if df.iloc[n,13] >= 6 and df.iloc[n,13] <= 18:
        df.iloc[n,14] = 'daytime'
    elif {df.iloc[n,13] >=0 and df.iloc[n,13] <= 5} or {df.iloc[n,13] >= 18 and df.iloc[n,13] <= 23}:
        df.iloc[n,14] = 'nighttime'
        
    if df.iloc[n,13] >= 7 and df.iloc[n,13] <= 9:
        df.iloc[n,15] = 'day_rushhour'
    elif df.iloc[n,13] >= 17 and df.iloc[n,13] <= 19:
        df.iloc[n,15] = 'night_rushhour'
        
    n = n+1

print(df)

df_new = pd.DataFrame(index=range(31),columns=range(3))
        
piece = dict(list(df.groupby([df.iloc[:,12], df.iloc[:,14]])))
piece_rush = dict(list(df.groupby([df.iloc[:,12],df.iloc[:,15]])))
#print(piece_rush)

n = 1
n = int(n)

while n <= 31:
    try:
        if (piece[n, 'daytime'].iloc[:,2].mean() > piece[n, 'nighttime'].iloc[:,2].mean()               #Large Ozone daytime 
            and (piece[n, 'daytime'].iloc[:,1].mean() < piece[n, 'nighttime'].iloc[:,1].mean()          #Large BC nightime
                 or piece[n, 'daytime'].iloc[:,3].mean() < piece[n, 'nighttime'].iloc[:,3].mean())):    #Large PM nightime
            df_new.iloc[n-1,2] = 'DNV'
        elif piece[n, 'daytime'].iloc[:,2].mean() < piece[n, 'nighttime'].iloc[:,2].mean():             #Large Ozone nighttime
            df_new.iloc[n-1,2] = 'UCV'
            
        if (piece[n, 'daytime'].iloc[:,2].mean() > piece[n, 'nighttime'].iloc[:,2].mean()                       #Large Ozone daytime
            and (piece_rush[n, 'day_rushhour'].iloc[:,3].max() == piece[n, 'daytime'].iloc[:,3].max()          #Large PM daytime rushhour
                 or piece_rush[n, 'night_rushhour'].iloc[:,3].max() == piece[n, 'nighttime'].iloc[:,3].max())):#Large BC nighttime rushhour
            df_new.iloc[n-1,1] = 'RHV'
        n = n+1
    except KeyError:
        n = n+1
        
for m in range(31):
    df_new.iloc[m,0] = int(m+1)

#print(df_new)

n = 0
n = int(n)

while n < len(df):
    A = df.iloc[n,12]
    for m in range(31):
        if df_new.iloc[m,0] == A:
            df.iloc[n,5] = df_new.iloc[m,2]
            df.iloc[n,16] = df_new.iloc[m,1]
    n = n+1

#Export to new csv file
df.to_csv('data/Dpattern_'+ file_name + '.csv')


