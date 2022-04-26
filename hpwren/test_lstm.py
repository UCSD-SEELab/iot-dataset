# Code contributed by Xiyuan Zhang (https://xiyuanzh.github.io/) in 04/2022

import pandas as pd
import numpy as np
import torch
from models import RNN, LSTM, GRU, CNN, MLP
#from transformer import Transformer

##### helper function #####
def DataBatch(data, batchsize, shuffle=True):

    n = data.shape[0]
    if shuffle:
        index = np.random.permutation(n)
    else:
        index = np.arange(n)
    for i in range(int(np.ceil(n/batchsize))):
        inds = index[i*batchsize : min(n,(i+1)*batchsize)]
        yield inds, data[inds]

def sliding_window(data, win_size=48):

    train_data = []
    for t in range(win_size, len(data)):
        train_data.append(data[t-win_size:t])
    train_data = np.stack(train_data)
    train_data = torch.from_numpy(train_data).float()
    return train_data

def z_norm(x):

    mean = np.nanmean(x, axis=0)
    var = np.nanstd(x, axis=0)
    return mean, var

##### hyperparameters #####
num_epochs = 200
learning_rate = 0.001
batch_size = 32
win_size = 24

input_size = 12
output_size = 12
hidden_size = 128
num_layers = 1

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

##### data preparation #####
df = pd.read_csv('2021/MG.csv')
df = df.dropna()
data = df.values[:,4:] # shape = (T,12)
mean, var =  z_norm(data)
data = (data - mean) / var

test_samples_num = int(0.04 * data.shape[0])
train_data = data[:-test_samples_num]
test_data = data[-test_samples_num:]

train_data = sliding_window(train_data, win_size) # N_train, win_size, 12
test_data = sliding_window(test_data, win_size) # N_test, win_size, 12

########## model ##########
#model = RNN(input_size, hidden_size, output_size, num_layers).to(device)
model = LSTM(input_size, hidden_size, output_size, num_layers, device).to(device)
#model = GRU(input_size, hidden_size, output_size, num_layers).to(device)
#model = CNN(input_size, hidden_size, output_size, win_size-1).to(device)
#model = MLP(input_size, hidden_size, output_size, win_size-1).to(device)

criterion = torch.nn.MSELoss()    # mean-squared error for regression
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#optimizer = torch.optim.SGD(lstm.parameters(), lr=learning_rate)

##### Train the model #####
for epoch in range(num_epochs):

    total_loss = 0
    for inds, batch_data in DataBatch(train_data, batch_size):

        batch_data = batch_data.to(device)

        optimizer.zero_grad()

        input = batch_data[:,:-1,:]
        gt = batch_data[:,-1,:]

        pred = model(input)
        loss = criterion(gt, pred)
        total_loss += loss * len(batch_data)

        loss.backward()
        optimizer.step()

    print("Epoch: %d, loss: %1.5f" % (epoch, total_loss.item() / len(train_data)))

    err = 0
    for inds, batch_data in DataBatch(test_data, batch_size):

        batch_data = batch_data.to(device)

        input = batch_data[:,:-1,:]
        gt = batch_data[:,-1,:]

        pred = model(input)
        err += len(batch_data) * criterion(gt, pred)

    print("Epoch: %d, MSE: %1.5f" % (epoch, err.item() / len(test_data)))

    torch.save(model.state_dict(), 'global')
