import numpy as np
import os

keys = ['pressure', 'light', 'rh', 'recv_time', 'pm2.5', 'temp', 'co2']
npy_data_path = os.path.abspath('./npy_data')

for key in keys:
    print('key:', key)
    locals()['%s'%key] = np.load(npy_data_path + '\\' + key + '.npy') # create keys var

print(locals()['__name__'])
print(locals()['pressure'], len(locals()['pressure']))
print(locals()['co2'])
#print(locals()) #印出所有潛在變數

'''
# 資料探測中，溫度小於5度的只有自定義無資料的-1.0(542290)跟儀器測資0.0(13350)
# 高於40.0度(4803)
# npy裡面資料類別都是一致的
con, con2 = 0, 0
under, upper = 0, 0
for t in temp:
    if t == -1.0:con+=1
    if t == 0.0:con2+=1
    if t > 40.0:
        upper+=1
        #print(t)
    if t < 5.0:under+=1
print(con, con2)
print(upper, under)

'''