# -*- encoding:utf-8 -*-

import pandas as pd
import numpy as np
import json

df = pd.read_csv("timeslots.csv",parse_dates=['Day', 'Timestamp UTC ms', \
	'Time'])
df_ = df[df['Day']>df['Day'][0]]
df_.drop(columns=['Timestamp UTC ms', 'Steps', 'Move'])
df_['Duration_min'] = df_['Duration ms']/60000

def act_split(strings, index=0):
    if pd.isnull(strings):
        return 'NaN'
    strings = strings.split(': ')
    if len(strings)==1:
        if index == 0:
            return strings[index]
        else:
            return 'NaN'
    return strings[index]

df_['act1']= df_['Activity'].apply(act_split)
df_['act2']= df_['Activity'].apply(act_split, index=1)

def activity_data(df, n=10):
	_ = []
	for i in df[['act1','act2','Duration_min']][:10]:
		children = dict{'name': i.act2,
		value: i.Duration_min}
		_.append(dict{'name': i.act1,
		'children': children})
	return _