clc;clear;
train_path='C:\Users\user\Desktop\程式語言\DeepLearning\database\train_images\';
test_path='C:\Users\user\Desktop\程式語言\DeepLearning\database\test_images\';
small_test_path='C:\Users\user\Desktop\程式語言\DeepLearning\database\small_test_images\';
net = alexnet;

pre_train_ds = imageDatastore(train_path,'IncludeSubfolders',true,'LabelSource','foldernames');
pre_test_ds = imageDatastore(test_path);
pre_small_test_ds = imageDatastore(small_test_path);
train_ds = augmentedImageDatastore([227 227],pre_train_ds,'ColorPreprocessing','gray2rgb');
test_ds = augmentedImageDatastore([227 227],pre_test_ds,'ColorPreprocessing','gray2rgb');
small_test_ds = augmentedImageDatastore([227 227],pre_small_test_ds,'ColorPreprocessing','gray2rgb');
%train_ds.Labels() %沒labels了
numClasses = numel(categories(pre_train_ds.Labels))%numel=取數量

layers = net.Layers
layers(end-2) = fullyConnectedLayer(numClasses);
layers(end) = classificationLayer;

options = trainingOptions('sgdm', ...
    'MaxEpochs', 30, ...
    'InitialLearnRate', 0.001, ...
    'MiniBatchSize', 32 , ...
    'Plots','training-progress');

[newnet,info] = trainNetwork(train_ds, layers, options);
testpreds = classify(newnet,test_ds);
testpreds2 = classify(newnet,small_test_ds);
%% output
table = readtable('C:\Users\user\Desktop\程式語言\DeepLearning\database\test.csv','ReadVariableNames', true, 'Delimiter',',');
C = categorical([0,1,2,3,4,5])
for i=1:10142
    test_array = strsplit(test_ds.Files{i},'\');
    test_filename = test_array{9};
    table_array=table{i,1};
    table_filename = table_array{1,1};
    if testpreds(i)==C(1)
        cel={0};
    elseif testpreds(i)==C(2)
        cel={1};
    elseif testpreds(i)==C(3)
        cel={2};
    elseif testpreds(i)==C(4)
        cel={3};
    elseif testpreds(i)==C(5)
        cel={4};
    elseif testpreds(i)==C(6)
        cel={5};
    end
    table(i,2)=cel;
end
writetable(table,'C:\Users\user\Desktop\程式語言\DeepLearning\database\test.csv')
fprintf('ok la!!\n')
%% output
%writematrix(TXT,'C:\Users\user\Desktop\程式語言\DeepLearning\database\test.csv')
%近來TXT，從1('ID')~10015迴圈，strsplit(test_ds.Files{3126},'\')的{9}為檔名，對照並寫值進入TXT(10143+1+i)
%合併用cat(1,a,b)

%options = trainingOptions('sgdm', ...
%    'LearnRateSchedule','piecewise', ...
%    'LearnRateDropFactor',0.2, ...
%    'LearnRateDropPeriod',5, ...
%    'MaxEpochs',20, ...
%    'MiniBatchSize',64, ...
%    'Plots','training-progress')

%options = trainingOptions('sgdm', ...
%    'MaxEpochs',8, ...
%    'ValidationData',{XValidation,YValidation}, ...
%    'ValidationFrequency',30, ...
%    'Verbose',false, ...
%    'Plots','training-progress');
%net = trainNetwork(XTrain,YTrain,layers,options);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%分層查找+漂亮作圖
%ly=net.Layers();
%in_layer = ly(1)
%out_layer=ly(25)
%in_name = in_layer.Name()
%多方法可查找如InputSize()
%categorynames = out_layer.Classes();
%[pred, scores] = classify(net,img1)
%bar(scores)
%highscores = scores > 0.01;
%bar(scores(highscores))
%xticklabels(categorynames(highscores))
%%%thresh = median(scores) + std(scores)
%動態閾值


%大數量圖片管理+同時操作
%chan_path='database\test_images\test*.png';
%path=[cons_path,chan_path]
%train_ds = imageDatastore(path)
%fname = train_ds.Files()
%imgno7 = readimage(train_ds,7)
%preds = classify(net,train_ds)
%全部ds中做預測
%%auds = augmentedImageDatastore([227 227],train_ds)
%auds為整個圖庫預處理

%灰階轉彩色
%montage(imds)
%顯示all imds圖片
%auds = augmentedImageDatastore([227 ...
%227],imds,'ColorPreprocessing','gray2rgb')
%整個灰階資料庫轉rgb

%存儲的子資料夾也搜索
%flwrds = imageDatastore('Flowers','IncludeSubfolders',true)

%%遷移學習=>需要預處理網路+已確認圖像+演算法變量
%flwrds = imageDatastore(pathToImages,'IncludeSubfolders',true, ...
%    'LabelSource','foldernames')
%將子資料夾明子設為標籤的存儲
%flowernames = flwrds.Labels()
%得一組labels
%[flwrTrain,flwrTest] = splitEachLabel(flwrds,0.8,'randomized')
%分割成訓練組跟試驗組且隨機
%[flwrTrain,flwrTest] = splitEachLabel(flwrds,50)
%每個標籤給ds1的數量=50，避免網路玩概率

%%%%%%%%23層全連接輸出，24層皈依畫分數%%%%%%%%
%fc = fullyConnectedLayer(12)
%創建全連接層(12種)
%layers(23)=fc
%換掉23層
%layers(25)=classificationLayer
%new掉25層
%opts = trainingOptions('sgdm','InitialLearnRate',0.001)
%創建訓練選項(sgdm),且學習綠改為0.001
%學習綠<<則局部最佳非最佳，過大則震盪

%評估
%load pathToImages
%load trainedFlowerNetwork flowernet info
%plot(info.TrainingLoss)
%畫損失率(也可以TrainingAccurary或是BaseLearnRate)
%最後用試煉組跑一次看正確率

%flwrActual = testImgs.Labels
%正確label
%numCorrect=nnz(flwrPreds == flwrActual)
%fracCorrect = numCorrect/numel(flwrPreds)
%比對正確有幾個，再除總數拿正確率
%confusionchart(testImgs.Labels, flwrPreds)
%混淆矩陣試驗