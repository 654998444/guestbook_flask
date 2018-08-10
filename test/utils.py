# -*- encoding:utf-8 -*-

import pandas as pd
import numpy as np
import json
from datetime import datetime, date, timedelta

CSV_PATH = 'templates/data.json'

categories = ['Personal Life', 'Art & Entertainment', 'Chores', 'Social', \
        'No category', 'Transport', 'Professional Life', 'Sport & Fitness', \
        'Health & Hygiene', 'Resting', 'Hobbies']
colors = ['#FF00FF', '#484891', '#FFDC35', '#5B00AE', '#D0D0D0', '#0080FF', \
        '#AE0000', '#FFA042', '#8CEA00', '#00FFFF', '#7373B9']
values = np.array([0.5, 0.5, 5, -3, 0, 0, 5, 1, 0, -.5, 1.5], dtype=np.float32)
cateDict = dict(zip(categories, colors))
valuesDict = dict(zip(categories, values))

df = pd.read_csv("templates/timeslots.csv",parse_dates=['Day', 'Timestamp UTC ms', \
	'Time'])
df['Time'] = df['Time'] - pd.Timedelta(hours=8)
df['Day'] = df['Time'].apply(lambda x: x.strftime('%Y-%m-%d'))
df['Duration_hrs'] = df['Duration ms'] / (60*60*1000)
df.drop(columns=['Timestamp UTC ms', 'Steps', 'Move'])
df['color'] = df['Activity Category'].map(cateDict)
df['Activity'] = df['Activity'].apply(lambda x: str(x).replace(': ','-'))
df['point'] = df['Activity Category'].apply(lambda x: valuesDict[x]) * \
                    df['Duration_hrs']

dailyPoint = pd.Series([0]*365, index=pd.date_range(start='01/01/2018', \
                    end='31/12/2018', freq='D'), dtype=float)
tmp = df.groupby(df['Time'].apply(lambda x: x.strftime('%Y-%m-%d')))\
                ['point'].sum()
dailyPoint[[pd.to_datetime(x) for x in tmp.index.tolist()]] = tmp.values


def generateDailyPoint(df, file_path='templates/dailyPoint.json'):
    tmp = dict(zip([x.strftime('%Y-%m-%d') for x in df.index], \
                                                    df.values))
    with open(file_path, 'w') as f:
        json.dump(tmp, f)

def actSplit(strings, index=0):
    if pd.isnull(strings):
        return 'NaN'
    strings = strings.split('-')
    if len(strings)==2:
        return strings[index]
    return strings[0]

def activityData(df, n=10, type=1):
    '''
    type = 1
    return:
        [{"itemStyle": {"color": df.color, \
            "name": df[Activity Category], \
            "children": [
            {"itemStyle": {"color": df.color}, \
                "name": df.Activity, \
                "value": df.Duration_hrs}
                ]
        },
        ...
        ]

    type = 2
    return: 
        [{"itemStyle": {"color": df.color, \
            "name": df.act1, \
            "children": [
            {"itemStyle": {"color": df.color}, \
                "name": df.act2 || df.act1, \
                "value": df.Duration_hrs}
                ]
        },
        ...
        ]
    '''
    _ = []
    if type == 2:
        for i in range(n):
            children = dict({'name': df.iloc[i,:].act2,
            'value': df.iloc[i,:].Duration_hrs,
            'itemStyle': dict(color=df.iloc[i,:].color)})
            _.append(dict({'name': df.iloc[i,:].act1,
            'children': [children],
            'itemStyle': dict(color=df.iloc[i,:].color)}))
        return _
    for i in range(n):
        children = dict({'name': df.iloc[i,:].Activity,
        'value': df.iloc[i,:].Duration_hrs,
        'itemStyle': dict(color=df.iloc[i,:].color)})
        _.append(dict({'name': df.iloc[i,:]['Activity Category'],
        'children': [children],
        'itemStyle': dict(color=df.iloc[i,:].color)}))
    return _

def timeSplit(string):
    _ = [int(i) for i in string.split('-')]
    return datetime(_[0],_[1],_[2])

def generateData(start=None, end=None, 
    file_path=CSV_PATH):
    '''
    return:
        df[time in yesterday] as default, or df[time in start day],
        else df[time in start before end]
    '''
    global df
    if start == None:
        start = (date.today() - timedelta(days=1)).\
                    strftime('%Y-%m-%d')
    start = timeSplit(start) if type(start) == str() else start
    if end == None:
        end = date.today().strftime('%Y-%m-%d')
    end = timeSplit(end) if type(end) == str() else end

    df_ = df[(df['Time'] >= start) & (df['Time'] < end)]
    df_.loc[:,'act1'] = df_.loc[:,'Activity'].apply(actSplit).values
    df_.loc[:,'act2']= df_.loc[:,'Activity'].apply(actSplit, index=1).values

    with open(file_path, 'w') as f:
        # print(activityData(df_, len(df_)))
        json.dump(activityData(df_, len(df_)), f)

if __name__ == '__main__':
    generateDailyPoint(dailyPoint)
    generateData()
