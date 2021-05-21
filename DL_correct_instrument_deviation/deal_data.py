import os
import numpy as np
import json
from datetime import datetime
import matplotlib.pyplot as plt

root_path = os.path.abspath('.')
data_root_path = os.path.join(root_path, 'data_file')
npy_data_path = os.path.join(root_path, 'npy_data')
homogenize_npt_data_path = os.path.join(root_path, 'homogenize_npt_data')
keys = ['pressure', 'light', 'rh', 'recv_time', 'pm2.5', 'temp', 'co2']

# 將原始的json資料創建成npy檔案，但是recv_time不連續(只是單純append進來)、無資料區以-1.0取代、原始檔案也有可能有誤差
# 主要處理原始資料有兩階段不同的json格式，以split_str這個檔名為分界點
def create_npy():
    json_list = []
    for root, subdirs, files in os.walk(data_root_path):
        for f in files:
            if f.endswith('.json'):json_list.append(os.path.join(root, f))

    all_data = {'pressure':[], 'light':[], 'rh':[], 'recv_time':[], 'pm2.5':[], 'temp':[], 'co2':[]}
    split_str = r'C:\Users\user\Desktop\DL_correct_instrument_deviation\data_file\2019_09_17\219_0_0_10\DL2018DataRes_21.json'

    #part 1 format data
    for json_name in json_list[:json_list.index(split_str)]:
        print(json_name)
        with open(json_name, 'r') as f:
            one_json_data_list = json.load(f) #list
            for single_data in one_json_data_list: #dict
                for key in keys:
                    if key == 'recv_time':continue #deal later
                    if single_data[key] == 'nodata':all_data[key].append(-1.0)
                    else:all_data[key].append(float(single_data[key]))
                #recv_time
                if single_data['recv_time'] == 'nodata':
                    all_data['recv_time'].append(-1.0)
                else:
                    recv_time = datetime.strptime(single_data['recv_time'], '%Y-%m-%d %H:%M:%S')
                    all_data['recv_time'].append(recv_time.strftime('%Y-%m-%d %H:%M:%S'))

    #part 2 format data
    for json_name in json_list[json_list.index(split_str):]:
        print(json_name)
        with open(json_name, 'r') as f:
            one_json_data_list = json.load(f) #list
            for single_data in one_json_data_list: #dict
                for key in keys:
                    if key == 'recv_time' or key == 'pm2.5':continue #deal later
                    if single_data[key] == 'nodata':all_data[key].append(-1.0)
                    else:all_data[key].append(float(single_data[key]))
                #pm2.5
                if single_data['pm2_5'] == 'nodata':
                    all_data['pm2.5'].append(-1.0)
                else:
                    all_data['pm2.5'].append(single_data['pm2_5'])
                #recv_time
                if single_data['instance_create_time'] == 'nodata':
                    all_data['recv_time'].append(-1.0)
                else:
                    recv_time = datetime.strptime(single_data['instance_create_time'], '%Y/%m/%d %H:%M:%S %z')
                    all_data['recv_time'].append(recv_time.strftime('%Y-%m-%d %H:%M:%S'))

    for key in keys:
        data_npy = np.array(all_data[key])
        np.save(npy_data_path+'/'+key+'.npy', data_npy)
        print(data_npy.shape)


def remove_extreme_nodata_errors():
    print('remove_extreme_nodata_errors gogo')

#見test裡面動態產生變數
    for key in keys:
        npy = np.load(npy_data_path+'/'+key+'.npy')
        print(type(npy[0]))


def look():
    temp = np.load(npy_data_path + '/temp.npy')
    recv_time = np.load(npy_data_path + '/recv_time.npy')

    data = temp[:]
    for i in range(len(data)):
        if data[i] < 3 or data[i] > 40:
            data[i] = data[i-1]


    fig = plt.figure()
    ax = fig.add_subplot(111)
    # my_x_ticks = np.arange(-5, 5, 0.5)
    # plt.xticks(my_x_ticks)
    plt.plot(data, recv_time)
    plt.show()




if __name__ == '__main__':
    #create_npy()
    #remove_extreme_nodata_errors()
    look()