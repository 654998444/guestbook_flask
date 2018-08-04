# -*- encoding:utf-8 -*-

import pandas as pd
import numpy as np
import json
from datetime import datetime

categories = ['Personal Life', 'Art & Entertainment', 'Chores', 'Social', \
        'No category', 'Transport', 'Professional Life', 'Sport & Fitness', \
        'Health & Hygiene', 'Resting', 'Hobbies']
colors = ['#FF00FF', '#484891', '#FFDC35', '#5B00AE', '#D0D0D0', '#0080FF', \
        '#AE0000', '#FFA042', '#8CEA00', '#00FFFF', '#7373B9']
cateDict = dict(zip(categories, colors))

df = pd.read_csv("templates/timeslots.csv",parse_dates=['Day', 'Timestamp UTC ms', \
	'Time'])
df['Duration_hrs'] = df['Duration ms'] / (60*60*1000)
df.drop(columns=['Timestamp UTC ms', 'Steps', 'Move'])
df['color'] = df['Activity Category'].map(cateDict)
df['Activity'] = df['Activity'].apply(lambda x: str(x).replace(': ','-'))

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


def generateData(start='2018-07-29', end='2018-07-31', 
    file_path='templates/data.json'):
    global df
    _ = [int(i) for i in start.split('-')]
    start = datetime(_[0],_[1],_[2])
    _ = [int(i) for i in end.split('-')]
    end = datetime(_[0],_[1],_[2])
    df_ = df[(df['Time'] > start) & (df['Time'] < end)]
    df_.loc[:,'act1'] = df_.loc[:,'Activity'].apply(actSplit).values
    df_.loc[:,'act2']= df_.loc[:,'Activity'].apply(actSplit, index=1).values

    with open(file_path, 'w') as f:
        print(activityData(df_, len(df_)))
        json.dump(activityData(df_, len(df_)), f)