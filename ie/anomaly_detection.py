import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pylab as plt
from datetime import datetime
import matplotlib.dates as mdates
import numpy as np
from scipy import signal
from scipy.fftpack import fft, ifft
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LSTM
import time
pd.set_option('display.max_columns', 51)
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 32}
plt.rc('font', **font)
import os

dir_path = os.getcwd()
data_dir = os.path.abspath(os.path.join(dir_path, '../data'))
combined_pkl = os.path.join(data_dir, 'combine.pkl')
part1_pkl = os.path.join(data_dir, "Part1.pkl")
part2_pkl = os.path.join(data_dir, "Part2.pkl")
file1 = os.path.join(data_dir,"Hackathon_DataSet_OctApr_Part1.txt")
file2 = os.path.join(data_dir,"Hackathon_DataSet_OctApr_Part2.txt")

#file1_df = pd.read_table(file1, sep='\t', header=0, parse_dates=['TimeStamp'], index_col=["Id"])
#file2_df = pd.read_table(file2, sep='\t', header=0, parse_dates=['TimeStamp'], index_col=["Id"])

#print(len(file1_df.columns))
#print(len(file2_df.columns))
#print(file1_df.columns)
#print(file2_df.columns)

#file_df = pd.merge(file1_df, file2_df, on="TimeStamp")
#file_df.to_pickle(combined_pkl)
file_df = pd.read_pickle(combined_pkl)

sequence_length = 1000

file_df.info()

#create model
model = Sequential()
layers = {'input': 1, 'hidden1': 64, 'hidden2': 256, 'hidden3': 100, 'output': 1}

model.add(LSTM( input_length=sequence_length,  input_dim=layers['input'],
            output_dim=layers['hidden1'],
            return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(layers['hidden2'],return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(layers['hidden3'], return_sequences=False))
model.add(Dropout(0.2))

model.add(Dense(output_dim=layers['output']))
model.add(Activation("linear"))

start = time.time()
model.compile(loss="mse", optimizer="rmsprop")
print ("Compilation Time : ", time.time() - start)

def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []
    #y values starts from index window_size till end
    y = series[window_size:]
    #x values ends windows_size before the end
    X = [series[:-window_size]]
    # Create window_size columns of shiffted x values
    for i in range(1,window_size):
        X = np.vstack((X, series[i:(i - window_size)]))
    # Transpose to rows
    X = X.T
    # reshape each
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y), 1)

    return X, y

start_time = datetime(2017, 3, 11,11,0)
end_time = datetime(2017, 3, 12, 12,0)
time_range= (file_df["TimeStamp"] < end_time) & (file_df["TimeStamp"] > start_time)
time_series = file_df[time_range]["21-LT-10516.PV_Prod_Sep_Oil_Interface_Level (%)"]
X,y = window_transform_series(time_series, sequence_length)

# split our dataset into training / testing sets
train_test_split = int(np.ceil(2*len(y)/float(3)))   # set the split point

# partition the training set
X_train = X[:train_test_split,:]
y_train = y[:train_test_split]

# keep the last chunk for testing
X_test = X[train_test_split:,:]
y_test = y[train_test_split:]

# NOTE: to use keras's RNN LSTM module our input must be reshaped to [samples, window size, stepsize]
X_train = np.asarray(np.reshape(X_train, (X_train.shape[0], sequence_length, 1)))
X_test = np.asarray(np.reshape(X_test, (X_test.shape[0], sequence_length, 1)))

# run your model!
model.fit(X_train, y_train, epochs=5, batch_size=50, verbose=1)

# generate predictions for training
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

import matplotlib.pyplot as plt
# plot original series
plt.plot(time_series,color = 'k')

split_pt = train_test_split + sequence_length
plt.plot(np.arange(sequence_length,split_pt,1),train_predict,color = 'b')

# plot testing set prediction
plt.plot(np.arange(split_pt,split_pt + len(test_predict),1),test_predict,color = 'r')

# pretty up graph
plt.xlabel('time ')
plt.ylabel('(normalized) price of Apple stock')
plt.legend(['original series','training fit','testing fit'],loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
