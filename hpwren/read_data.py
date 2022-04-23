#!/usr/bin/env python
# coding: utf-8

# In[22]:


import glob
import os
import pandas as pd
import json
import copy
import numpy as np
import argparse

FEATURE = 'Ta'
SEQ_LEN = 12

def read_data(file_name):
    df = pd.read_csv(file_name)
    X, y = [], []

    for i in range(df.shape[0]-SEQ_LEN-1):
        # Check for nan
        if df[FEATURE][i:i+SEQ_LEN+1].isnull().values.any():
            # print(df[FEATURE][i:i+SEQ_LEN+1].values.tolist())
            continue
        new_X = df[FEATURE][i:i+SEQ_LEN].values.tolist()
        new_y = float(df[FEATURE][i+SEQ_LEN])

        X.append(new_X)
        y.append(new_y)

    return X, y

def save_data(data_dict, file_name):
    # Save the data dictionary with 'users', 'user_data' and 'num_samples' to json file
    with open(file_name, 'w') as fp:
        json.dump(data_dict, fp,  indent=4)


# In[23]:

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tf', type=float, default=0.9,
                        help='fraction of data in the training set, written as a decimal.')
    args = parser.parse_args()

    folder = './2021'
    data_dict = {}
    data_dict['users'] = []
    data_dict['user_data'] = {}
    data_dict['num_samples'] = []

    for file_name in glob.glob(os.path.join(folder, '*.csv')):
        new_X, new_y = read_data(file_name)

        if len(new_X) <= 0:  # Skip the location with zero valid data
            continue
        user_name = file_name.split('/')[-1].split('.')[0]

        data_dict['users'].append(user_name)
        data_dict['user_data'][user_name] = {'x': new_X, 'y': new_y}
        data_dict['num_samples'].append(len(data_dict['user_data'][user_name]['x']))

        print('user name: {} num samples: {}'.format(user_name, data_dict['num_samples'][-1]))


    train_data_dict = copy.deepcopy(data_dict)
    test_data_dict = copy.deepcopy(data_dict)
    for user in data_dict['user_data']:  # Clear existing data in new train and test dict
        total_len = len(data_dict['user_data'][user]['x'])
        select = np.random.choice(total_len, int(0.9*total_len), replace=False)
        select.sort()
        not_select = list(set(np.arange(total_len)) - set(select))
        not_select.sort()
        train_data_dict['user_data'][user] = \
            {'x': [data_dict['user_data'][user]['x'][s] for s in select],
            'y': [data_dict['user_data'][user]['y'][s] for s in select]}
        test_data_dict['user_data'][user] = \
            {'x': [data_dict['user_data'][user]['x'][s] for s in not_select],
            'y': [data_dict['user_data'][user]['y'][s] for s in not_select]}

        user_idx = data_dict['users'].index(user)
        train_data_dict['num_samples'][user_idx] = len(train_data_dict['user_data'][user]['x'])
        test_data_dict['num_samples'][user_idx] = len(test_data_dict['user_data'][user]['x'])

    print('train users are: ', train_data_dict['user_data'].keys())
    print('train num_samples are: ', train_data_dict['num_samples'])

    print('test users are: ', test_data_dict['user_data'].keys())
    print('test num_samples are: ', test_data_dict['num_samples'])

    # Save data to json
    save_data(train_data_dict, 'train.json')
    save_data(test_data_dict, 'test.json')
    print('Data saved to json')


if __name__ == "__main__":
    main()
