# Code contributed by Xiyuan Zhang (https://xiyuanzh.github.io/) in 04/2022

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import Variable

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(RNN, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size

        self.rnn = nn.RNN(input_size=input_size,
                          hidden_size=hidden_size,
                          num_layers=num_layers,
                          batch_first=True)

        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.rnn(x)
        out = out[:, -1, :]
        out = self.fc(out)

        return out

class LSTM(nn.Module):

    def __init__(self, input_size, hidden_size, output_size, num_layers, device):
        super(LSTM, self).__init__()
        
        self.num_layers = num_layers

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.device = device
        
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                            num_layers=num_layers, batch_first=True)

        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):

        h_0 = torch.zeros(self.num_layers, x.shape[0], self.hidden_size).to(self.device)
        c_0 = torch.zeros(self.num_layers, x.shape[0], self.hidden_size).to(self.device)

        out, (h_out, c_out) = self.lstm(x, (h_0, c_0))  # b, t, output_size   

        out = self.fc(out)   
        out = out[:, -1, :]

        return out

class GRU(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(GRU, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size

        self.gru = nn.GRU(input_size=input_size,
                          hidden_size=hidden_size,
                          num_layers=num_layers,
                          batch_first=True)

        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.gru(x)
        out = out[:, -1, :]
        out = self.fc(out)

        return out

class CNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, seq_len):
        super(CNN, self).__init__()

        self.conv = nn.Conv1d(in_channels=input_size, out_channels=hidden_size, kernel_size=1)
        self.relu = nn.ReLU()

        self.flat = nn.Flatten()

        self.fc = nn.Linear(hidden_size*seq_len, output_size)
    
    def forward(self, x):
        out = self.conv(x.permute(0,2,1))
        out = self.flat(self.relu(out))

        out = self.fc(out)

        return out

class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, seq_len):
        super(MLP, self).__init__()

        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

        self.fc3 = nn.Linear(seq_len, 1)

    def forward(self, x):

        out = self.relu(self.fc1(x))
        out = self.fc2(out) #b,t,c
        out = self.fc3(out.permute(0,2,1)) #b,c,1

        return out.squeeze()