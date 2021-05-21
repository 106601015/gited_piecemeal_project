#using single variable and predict
import numpy as np
import os
import json
import matplotlib.pyplot as plt
#from pandas import read_csv
import keras
import math
from keras.layers import LSTM, Dense, SimpleRNN, RNN, Input, Bidirectional, TimeDistributed, Conv1D, MaxPooling1D, Flatten
from keras.models import Model, Sequential, load_model #model_from_json
#sklearn for predeal
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error


#parameter
train_ratio = 0.7
epochs = 20
batch_size = 32
reference_range = 300 #consider how many data to reference

root_path = os.path.abspath('.')
data_root_path = os.path.join(root_path, 'data_file')
npy_data_path = os.path.join(root_path, 'npy_data')
homogenize_npy_data_path = os.path.join(root_path, 'homogenize_npt_data')
'''
def create_newdataset(dataset):
    x, y = [], []
    for i in range(len(dataset)-forward-1): #-1 for y's tail
        x.append(dataset[i:(i+forward), 0])
        y.append(dataset[i+forward, 0])
    return np.array(x), np.array(y)
'''
def get_aero_data(key):
    #get data
    aero_data = np.load(npy_data_path + '\\' + key + '.npy')
    aero_data = np.reshape(aero_data, (len(aero_data), 1))
    print(aero_data.shape)

    #normalize
    scaler = MinMaxScaler(feature_range=(0, 1))
    nor_aero_data = scaler.fit_transform(aero_data)
    #split to train and test(split vs 1-split)
    nor_aero_data_split_point = int(len(aero_data)*train_ratio)
    nor_aero_data_train, nor_aero_data_test = nor_aero_data[0:nor_aero_data_split_point, :], nor_aero_data[nor_aero_data_split_point:len(nor_aero_data), :]
    print('I train :', len(nor_aero_data_train), 'test:',  len(nor_aero_data_test))

    return nor_aero_data_train, nor_aero_data_test

def get_cwb_data(key): #???????????????????
    a, b = 0, 0
    return a, b

if __name__ == '__main__':
    aero_temp_train, aero_temp_test = get_aero_data('temp')
    cwb_temp_train, cwb_temp_test = get_cwb_data('temp')

    train_now, train_next = create_newdataset(train, forward)
    test_now, test_next = create_newdataset(test, forward)
'''
#now series is input, next series is output, reshape for add 1D(raw, col => raw, 1, col)
train_now = np.reshape(train_now, (train_now.shape[0], 1, train_now.shape[1]))
test_now = np.reshape(test_now, (test_now.shape[0], 1, test_now.shape[1]))
#Samples, time steps, features
print('============>', train_now.shape, train_next.shape)
'''

'''
#call saved model or buildmodel
output_path = 'C:\\Users\\user\\Desktop\\test1_output\\'
model_name = 'Bidirectional_model_'+str(datadays)+'_'+str(split)+'_'+str(forward)+'_'+str(epochs)+'_'+str(batch_size)+'.h5'

try:
    model = load_model(model_name)
    print('---> call model')
    model.summary()
except:
    #Bidirectional
    model = Sequential()
    model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(1, forward)))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

    model.fit(train_now, train_next, epochs=epochs, batch_size=batch_size, verbose=2) #verbose 0=no display, 1=show schedule, 2=show each epochs schedule
    print('---> build and save model')
    model.save(model_name)
    model.summary()
'''
#others LSTM
'''
    normal LSTM
model = Sequential()
model.add(LSTM(4, input_shape=(1, forward))) #4=units, output dimention ((why 4????
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
'''
'''
    Vanilla LSTM
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(1, forward)))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
'''
'''
    Stacked LSTM
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(1, forward), return_sequence=True))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
'''
'''
    Bidirectional LSTM
model = Sequential()
model.add(Bidirectional(LSTM(50, activation='relu'), input_shape=(1, forward)))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
'''
'''
    CNN LSTM
model = Sequential()
model.add(TimeDistributed(Conv1D(filters=64, kernel_size=1, activation='relu'), input_shape=(None, 1, forward)))
model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
model.add(TimeDistributed(Flatten()))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
'''



'''
trainpredict = model.predict(train_now)
testpredict = model.predict(test_now)

trainpredict = scaler.inverse_transform(trainpredict)
testpredict = scaler.inverse_transform(testpredict)
train_next = scaler.inverse_transform([train_next])
test_next = scaler.inverse_transform([test_next])

trainscore = math.sqrt(mean_squared_error(train_next[0], trainpredict[:,0]))
testscore = math.sqrt(mean_squared_error(test_next[0], testpredict[:,0]))
print('trainscore(RMSE):', trainscore)
print('testscore(RMSE):', testscore)


trainpredictplot = np.empty_like(dataset)
trainpredictplot[:, :] = np.nan
trainpredictplot[forward:len(trainpredict)+forward, :] = trainpredict # +forward to translate

testpredictplot = np.empty_like(dataset)
testpredictplot[:, :] = np.nan
testpredictplot[len(trainpredict)+forward*2+2:len(dataset), :] = testpredict

#print(len(trainpredictplot), len(trainpredictplot[0]), trainpredictplot) #should be 4463 1 <list>

plt.plot(scaler.inverse_transform(dataset), color='black')
plt.plot(trainpredictplot, color='orange')
plt.plot(testpredictplot, color='blue')
plt.savefig(output_path+model_name+'.png')
'''