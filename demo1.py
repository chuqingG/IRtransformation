import numpy as np
import math
import torch


def demo(xss, h0, batch_size, seq_len, hidden_size, input_size):
    
    u = np.random.uniform(size=(hidden_size, hidden_size))
    w = np.random.uniform(size=(hidden_size, input_size))
    y = np.zeros((batch_size, seq_len, hidden_size))
    for i in range(batch_size):
        for j in range(seq_len):
            y[i][j] = w @ xss[i][j] + u @ h0[i]

    return y

xss = np.random.uniform(size=(8,8,8))
h0 = np.random.uniform(size=(8,8))
demo(xss, h0, 8,8,8,8)