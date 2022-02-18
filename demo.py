import numpy as np
import math
import torch

BATCH_SIZE = 8
HIDDEN_SIZE = 8
SEQ_LEN = 8
INPUT_SIZE = HIDDEN_SIZE

def demo(xss, h0, batch_size, seq_len, hidden_size, input_size):
    # x.shape = (batch_size, seq_len, input_size)
    # h0.shape = (batch_size, hidden_size)
    u = np.random.uniform(size=(hidden_size, hidden_size))
    w = np.random.uniform(size=(hidden_size, input_size))
    y = np.zeros((batch_size, seq_len, hidden_size))
    for i in range(batch_size):
        for j in range(seq_len):
            if j == 0:
                # y_ij = (hs, )
                y[i][j] = w @ xss[i][j] + u @ h0[i]
            else:
                y[i][j] = w @ xss[i][j] + u @ y[i][j-1]
    return y

xss = np.random.uniform(size=(BATCH_SIZE, SEQ_LEN, INPUT_SIZE))
h0 = np.random.uniform(size=(BATCH_SIZE, HIDDEN_SIZE))
demo(xss, h0, BATCH_SIZE, SEQ_LEN, HIDDEN_SIZE, INPUT_SIZE)