# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 18:29:10 2019

@author: lenovo
"""

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import numpy as np
#import config

# =============================================================================
# Data
# =============================================================================
engine = create_engine('postgresql://postgres:Zpch9AQR6pPecJB7SYnc@ds4acolombia.cl3uubspnmbm.us-east-2.rds.amazonaws.com/datathon')

yellow_2 = pd.read_sql('select * from transport.yellow_counts', engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
yellow_2['neig'] = [a[:2] for a in yellow_2['nta']]

green = pd.read_sql('select * from transport.green_counts', engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
green['neig'] = [a[:2] for a in green['nta']]

uber = pd.read_sql('select * from transport.uber_counts', engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
uber['neig'] = [a[:2] for a in uber['nta']]


we='''
SELECT 
	EXTRACT(YEAR FROM DATE) AS YEAR,
	EXTRACT(MONTH FROM DATE) AS MONTH,
	EXTRACT(DAY FROM DATE) AS DAY,
	max_temp,
	min_temp,
	avg_temp,
	precipitation,
	snowfall,
	snow_depth,
	location
FROM other.weather
'''

weather = pd.read_sql(we, engine.connect(), parse_dates=('OCCURRED_ON_DATE',))

# =============================================================================
# ver diferencias entre años
# =============================================================================
def borough_comparison_2014_2015(boro,transport):
    bor_2014 = transport[(transport['month']>3) & (transport['month']<7)].groupby(['year','neig'])['count'].sum()[2014,boro]
    bor_2015 = transport[(transport['month']>3) & (transport['month']<7)].groupby(['year','neig'])['count'].sum()[2015,boro]
    boro_nta_2014 = transport[(transport['neig']==boro) & (transport['year']==2014) & (transport['month']>3) & (transport['month']<7)].groupby('nta')['count'].sum()
    boro_nta_2015 = transport[(transport['neig']==boro) & (transport['year']==2015) & (transport['month']>3) & (transport['month']<7)].groupby('nta')['count'].sum()
    return pd.DataFrame([(boro_nta_2014/bor_2014)*100,(boro_nta_2015/bor_2015)*100]).T.plot(title=boro)

#Para yellow
yellow_2.groupby(['year','month'])['count'].sum()
borough_comparison_2014_2015(yellow_2['neig'].unique()[0],yellow_2)
borough_comparison_2014_2015(yellow_2['neig'].unique()[1],yellow_2)
borough_comparison_2014_2015(yellow_2['neig'].unique()[2],yellow_2)
borough_comparison_2014_2015(yellow_2['neig'].unique()[3],yellow_2)
borough_comparison_2014_2015(yellow_2['neig'].unique()[4],yellow_2)

#Para green
green.groupby(['year','month'])['count'].sum()
borough_comparison_2014_2015(green['neig'].unique()[0],green)
borough_comparison_2014_2015(green['neig'].unique()[1],green)
borough_comparison_2014_2015(green['neig'].unique()[2],green)
borough_comparison_2014_2015(green['neig'].unique()[3],green)
borough_comparison_2014_2015(green['neig'].unique()[4],green)
 
#Para uber
uber.groupby(['year','month'])['count'].sum()
borough_comparison_2014_2015(uber['neig'].unique()[0],uber)
borough_comparison_2014_2015(uber['neig'].unique()[1],uber)
borough_comparison_2014_2015(uber['neig'].unique()[2],uber)
borough_comparison_2014_2015(uber['neig'].unique()[4],uber)
borough_comparison_2014_2015(uber['neig'].unique()[5],uber)


# =============================================================================
# Diferencias entre meses
# =============================================================================
plt.figure()
(yellow_2[(yellow_2['month']==4)].groupby('dow')['count'].sum()/yellow_2[yellow_2['month']==4]['count'].sum()).plot()
(yellow_2[(yellow_2['month']==5)].groupby('dow')['count'].sum()/yellow_2[yellow_2['month']==5]['count'].sum()).plot()
(yellow_2[(yellow_2['month']==6)].groupby('dow')['count'].sum()/yellow_2[yellow_2['month']==6]['count'].sum()).plot()
(yellow_2[(yellow_2['month']==7)].groupby('dow')['count'].sum()/yellow_2[yellow_2['month']==7]['count'].sum()).plot()
(yellow_2[(yellow_2['month']==8)].groupby('dow')['count'].sum()/yellow_2[yellow_2['month']==8]['count'].sum()).plot()
(yellow_2[(yellow_2['month']==9)].groupby('dow')['count'].sum()/yellow_2[yellow_2['month']==9]['count'].sum()).plot()

#Los meses no se comportan de la misma manera

# =============================================================================
# Comparación de horas del día en todos los meses
# =============================================================================
plt.figure()
[(yellow_2[(yellow_2['month']==a)].groupby('hour').sum()['count']/yellow_2[(yellow_2['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]
plt.figure()
[(green[(green['month']==a)].groupby('hour').sum()['count']/green[(green['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]
plt.figure()
[(uber[(uber['month']==a)].groupby('hour').sum()['count']/uber[(uber['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]


# =============================================================================
# Comparación entre días entre semana y fines de semana
# =============================================================================
#Yellow
plt.figure()
[(yellow_2[(yellow_2['month']==a) & ((yellow_2['dow']==0) | (yellow_2['dow']==6))].groupby('hour').sum()['count']/yellow_2[(yellow_2['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]
plt.figure()
[(yellow_2[(yellow_2['month']==a) & (yellow_2['dow']>0) & (yellow_2['dow']<6)].groupby('hour').sum()['count']/yellow_2[(yellow_2['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]

#Green
plt.figure()
[(green[(green['month']==a) & ((green['dow']==0) | (green['dow']==6))].groupby('hour').sum()['count']/green[(green['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]
plt.figure()
[(green[(green['month']==a) & (green['dow']>0) & (green['dow']<6)].groupby('hour').sum()['count']/green[(green['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]

#Uber
plt.figure()
[(uber[(yellow_2['month']==a) & ((uber['dow']==0) | (uber['dow']==6))].groupby('hour').sum()['count']/uber[(uber['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]
plt.legend(['Apr','May','Jun','Jul','Aug','Sep'])
plt.figure()
[(uber[(uber['month']==a) & (uber['dow']>0) & (uber['dow']<6)].groupby('hour').sum()['count']/uber[(uber['month']==a)]['count'].sum()).plot() for a in np.arange(4,10)]


# =============================================================================
# Weekdays and weekends by borough
# =============================================================================
#Manhattan-yellow
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='MN']['nta'].unique()]
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='MN']['nta'].unique()]

#Brooklyn yellow
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='BK']['nta'].unique()]
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='BK']['nta'].unique()]

#Queens yellow
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='QN']['nta'].unique()]
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='QN']['nta'].unique()]

#Bronx yellow
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='BX']['nta'].unique()]
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='BX']['nta'].unique()]

#Staten Island yellow
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='SI']['nta'].unique()]
plt.figure()
[(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']>0) & (yellow_2['dow']<6))]['count'].sum()).plot() for a in yellow_2[yellow_2['neig']=='SI']['nta'].unique()]


# =============================================================================
# Comportamiento similar a través de ntas en con los meses
# QN98 son los aeropuertos
# =============================================================================
# Yellow
for b in yellow_2['neig'].unique():
    plt.figure()
    nta_yes = []
    for a in yellow_2[yellow_2['neig']==b]['nta'].unique():
        if min(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum())>1:
            (yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum()/yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))]['count'].sum()).plot()
            nta_yes.append(a)
        else:
            print(min(yellow_2[(yellow_2['nta']==a) & ((yellow_2['dow']==0)|(yellow_2['dow']==6))].groupby('hour')['count'].sum()))
    plt.legend(nta_yes)        

# Green
for b in green['neig'].unique():
    plt.figure()
    nta_yes = []
    for a in green[green['neig']==b]['nta'].unique():
        if min(green[(green['nta']==a) & ((green['dow']==0)|(green['dow']==6))].groupby('hour')['count'].sum())>1:
            (green[(green['nta']==a) & ((green['dow']==0)|(green['dow']==6))].groupby('hour')['count'].sum()/green[(green['nta']==a) & ((green['dow']==0)|(green['dow']==6))]['count'].sum()).plot()
            nta_yes.append(a)
        else:
            print(min(green[(green['nta']==a) & ((green['dow']==0)|(green['dow']==6))].groupby('hour')['count'].sum()))
    plt.legend(nta_yes)        

# Uber
for b in uber['neig'].unique():
    plt.figure()
    nta_yes = []
    for a in uber[uber['neig']==b]['nta'].unique():
        if min(uber[(uber['nta']==a) & ((uber['dow']==0)|(uber['dow']==6))].groupby('hour')['count'].sum())>1:
            (uber[(uber['nta']==a) & ((uber['dow']==0)|(uber['dow']==6))].groupby('hour')['count'].sum()/uber[(uber['nta']==a) & ((uber['dow']==0)|(uber['dow']==6))]['count'].sum()).plot()
            nta_yes.append(a)
        else:
            print(min(uber[(uber['nta']==a) & ((uber['dow']==0)|(uber['dow']==6))].groupby('hour')['count'].sum()))
    plt.legend(nta_yes)        

     
# =============================================================================
# Diferencia de meses por nta
# =============================================================================
# Yellow
for nt in yellow_2[yellow_2['neig']=='MN']['nta'].unique():
    if yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)].groupby(['hour'])['count'].sum()/yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()).plot()
        plt.title(nt)
        

for nt in yellow_2[yellow_2['neig']=='BK']['nta'].unique():
    if yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)].groupby(['hour'])['count'].sum()/yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()).plot()
        plt.title(nt)
            
for nt in yellow_2[yellow_2['neig']=='BX']['nta'].unique():
    if yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()>30:
        plt.figure()
        for a in np.arange(4,10):
            (yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)].groupby(['hour'])['count'].sum()/yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()).plot()
        plt.title(nt)
        
for nt in yellow_2[yellow_2['neig']=='QN']['nta'].unique():
    if yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)].groupby(['hour'])['count'].sum()/yellow_2[(yellow_2['nta']==nt) & (yellow_2['month']==a)]['count'].sum()).plot()
        plt.title(nt)

# Green
for nt in green[green['neig']=='MN']['nta'].unique():
    if green[(green['nta']==nt) & (green['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (green[(green['nta']==nt) & (green['month']==a)].groupby(['hour'])['count'].sum()/green[(green['nta']==nt) & (green['month']==a)]['count'].sum()).plot()
        plt.title(nt)
        

for nt in green[green['neig']=='BK']['nta'].unique():
    if green[(green['nta']==nt) & (green['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (green[(green['nta']==nt) & (green['month']==a)].groupby(['hour'])['count'].sum()/green[(green['nta']==nt) & (green['month']==a)]['count'].sum()).plot()
        plt.title(nt)
            
for nt in green[green['neig']=='BX']['nta'].unique():
    if green[(green['nta']==nt) & (green['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (green[(green['nta']==nt) & (green['month']==a)].groupby(['hour'])['count'].sum()/green[(green['nta']==nt) & (green['month']==a)]['count'].sum()).plot()
        plt.title(nt)
        
for nt in green[green['neig']=='QN']['nta'].unique():
    if green[(green['nta']==nt) & (green['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (green[(green['nta']==nt) & (green['month']==a)].groupby(['hour'])['count'].sum()/green[(green['nta']==nt) & (green['month']==a)]['count'].sum()).plot()
        plt.title(nt)

#Uber
for nt in uber[uber['neig']=='MN']['nta'].unique():
    if uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (uber[(uber['nta']==nt) & (uber['month']==a)].groupby(['hour'])['count'].sum()/uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()).plot()
        plt.legend(np.arange(4,10))
        plt.title(nt)
        

for nt in uber[uber['neig']=='BK']['nta'].unique():
    if uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (uber[(uber['nta']==nt) & (uber['month']==a)].groupby(['hour'])['count'].sum()/uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()).plot()
        plt.title(nt)
            
for nt in uber[uber['neig']=='BX']['nta'].unique():
    if uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (uber[(uber['nta']==nt) & (uber['month']==a)].groupby(['hour'])['count'].sum()/uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()).plot()
        plt.title(nt)
        
for nt in uber[uber['neig']=='QN']['nta'].unique():
    if uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()>30*24:
        plt.figure()
        for a in np.arange(4,10):
            (uber[(uber['nta']==nt) & (uber['month']==a)].groupby(['hour'])['count'].sum()/uber[(uber['nta']==nt) & (uber['month']==a)]['count'].sum()).plot()
        plt.title(nt)

uber[uber['nta']=='MN28'].groupby('month')['count'].sum().sum()
uber[uber['nta']=='MN25'].groupby('month')['count'].sum().sum()
uber[uber['nta']=='MN24'].groupby('month')['count'].sum().sum()
uber[uber['nta']=='MN23'].groupby('month')['count'].sum().sum()
uber[uber['nta']=='MN22'].groupby('month')['count'].sum().sum()
uber[uber['nta']=='MN21'].groupby('month')['count'].sum().sum()
uber[uber['nta']=='MN20'].groupby('month')['count'].sum().sum()

plt.figure()
for a in np.arange(4,10):
    (yellow_2[(yellow_2['nta']=='MN28') & (yellow_2['month']==a)].groupby(['hour'])['count'].sum()/yellow_2[(yellow_2['nta']=='MN28') & (yellow_2['month']==a)]['count'].sum()).plot()
plt.figure()
for a in np.arange(4,10):
    (green[(green['nta']=='MN28') & (green['month']==a)].groupby(['hour'])['count'].sum()/green[(green['nta']=='MN28') & (green['month']==a)]['count'].sum()).plot()
plt.figure()    
for a in np.arange(4,10):
    (uber[(uber['nta']=='MN28') & (uber['month']==a)].groupby(['hour'])['count'].sum()/uber[(uber['nta']=='MN28') & (uber['month']==a)]['count'].sum()).plot()
        
# =============================================================================
# Ver si existe relación entre el clima y la agrupación de meses
# =============================================================================
weather.groupby('month').mean().iloc[:,2:].plot()


weather.groupby('month').mean()['precipitation'].plot()

weather_normalized = (weather.iloc[:,3:-1]-weather.iloc[:,3:-1].min())/(weather.iloc[:,3:-1].max()-weather.iloc[:,3:-1].min())

weather_normalized['year']  = weather['year']
weather_normalized['month'] = weather['month']
weather_normalized['day'] = weather['day']

weather_normalized.groupby('month').mean().iloc[:,:-2].plot()

weather_normalized['days'] = [str(int(weather['year'][a]))+("%02d" % weather['month'][a])+str("%02d" % weather['day'][a]) for a in range(len(weather))]
weather['days'] = [str(int(weather['year'][a]))+("%02d" % weather['month'][a])+str("%02d" % weather['day'][a]) for a in range(len(weather))]


weather_normalized[(weather_normalized['days']>'20140401') & (weather_normalized['days']<'20141001')].groupby('days').mean()['avg_temp'].plot()
weather_normalized[(weather_normalized['days']>'20140401') & (weather_normalized['days']<'20141001')].groupby('days').mean()['min_temp'].plot()
plt.legend(['avg','min'])

weather_normalized[(weather_normalized['days']>'20140401') & (weather_normalized['days']<'20141001')].groupby('days').mean()['precipitation'].plot()

#Comparación de temperatura media y mínima 
weather[(weather['days']>'20140401') & (weather['days']<'20141001')].groupby('days').mean()['avg_temp'].plot()
weather[(weather['days']>'20140401') & (weather['days']<'20141001')].groupby('days').mean()['min_temp'].plot()
plt.axvline(x='20190701')
plt.legend(['avg','min'])



# =============================================================================
# 
# =============================================================================
#Comparison between mean_income and counts per nta
a = demo[demo['borough']=='Manhattan'][['nta_code','mean_income']].sort_values(by='mean_income')
b = yellow_2[yellow_2['neig']=='MN'].groupby('nta').sum().sort_values(by='count')['count']

a.merge(b, right_on='nta',left_on='nta_code').plot()

c = demo[demo['borough']=='Manhattan'][['nta_code','population']].sort_values(by='population')
c.merge(b, right_on='nta',left_on='nta_code').plot()

d = demo[demo['borough']=='Manhattan'][['nta_code','median_age']].sort_values(by='median_age')
d.merge(b, right_on='nta',left_on='nta_code').plot()

