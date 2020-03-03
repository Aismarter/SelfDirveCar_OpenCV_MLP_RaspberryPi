
#MLP神经网络训练模块：使用反向传播训练神经网络

import cv2
import glob
import numpy as np
from sklearn.model_selection import train_test_split
import sys
import time


def retrieve_data_set():
    """从所有.npz文件中检索数据并将其聚合到MLP培训数据集"""
    #记录训练数据加载的开始时间
    start_time = cv2.getTickCount()
    # cv2.getTickCount()函数返回从参考点到这个函数被执行的时钟数

    print("Loading data set...")

    #载入训练数据
    image_array = np.zeros((1, 38400), 'float') #生成一个1行，38400列的零矩阵
    label_array = np.zeros((1, 4), 'float') #生成一个1行，4列的零矩阵

    # 检索与以下匹配的路径名列表
    data_set = glob.glob("training_data/*.npz") #搜寻指定文件位置

    if not data_set:
        print("No data set in directory, exiting!")
        sys.exit()

    for single_npz in data_set:  #一个一个的读取训练数据
        with np.load(single_npz) as data:
            temp_images = data["train"]   #训练的图片作为训练的依据
            temp_labels = data["train_labels"]   # 训练标签

        #对每张图片，空白图像和训练图像上下合并
        image_array = np.vstack((image_array, temp_images)) #把获取的训练图像与生成的空白图像合并
        label_array = np.vstack((label_array, temp_labels)) #把标签和空白数组合并

    X = np.float32(image_array[1:, :])
    Y = np.float32(label_array[1:, :])
    print("Image array shape: {0}".format(X.shape))
    print("Label array shape: {0}".format(Y.shape))

    #输出载入图片的时间
    end_time = cv2.getTickCount()
    print("Data set load duration: {0}"
          .format((end_time - start_time) // cv2.getTickFrequency()))
    #cv2.getTickFrequency()返回时钟频率。

    return X, Y


if __name__ == '__main__':
    X, Y = retrieve_data_set()

    # 8:2 分给训练和测试数据
    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2)

    #创建一个多层感知机
    start_time = cv2.getTickCount()
    #记录训练的开始时间

    layer_sizes = np.int32([38400, 64, 4])
    #设置层数，输入层38400（像素320*240），输出层4（上下左右四个方向），以及中间层32
    model = cv2.ml.ANN_MLP_create()  #建立模型
    model.setLayerSizes(layer_sizes)
    model.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP) #设置训练方式为反向传播
    model.setBackpropMomentumScale(0.0)
    #惯性项的强度（前两次迭代的权重之差）；
    #该参数提供了一些惯性来平滑权重的随机波动；
    model.setBackpropWeightScale(0.001) #权重梯度项的强度
    model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001)) #指定停止条件
    #设置终止条件，可以指定最大迭代次数（maxCount）或迭代之间的误差变化大小（epsilon）
    model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 2, 1)

    print("Training MLP...")
    model.train(train_X, cv2.ml.ROW_SAMPLE, train_Y)
    #这个函数利用输入的特征向量和对应的响应值(responses)来训练统计模型
    #tflag=CV_ROW_SAMPLE表示特征向量以行向量存储

    end_time = cv2.getTickCount() #记录训练停止时间，输出训练持续时间
    duration = (end_time - start_time) // cv2.getTickFrequency()
    #" // " 表示整数除法,返回不大于结果的一个最大的整数
    print("Training duration: {0}".format(duration))

    # 在训练集中的预测准确率,输出错误率
    ret_train, resp_train = model.predict(train_X)
    train_mean_sq_error = ((resp_train - train_Y) * (resp_train - train_Y)).mean()
    print("Train set error: {0:.2f}".format(train_mean_sq_error * 100))


    # 在测试数据的预测准确率，输出错误率
    ret_test, resp_test = model.predict(test_X)
    test_mean_sq_error = ((resp_test - test_Y) * (resp_test - test_Y)).mean()
    print("Test set error: {0:.2f}".format(test_mean_sq_error * 100))

    # 保存模型
    model.save("mlp_xml/mlp_{0}.xml".format(str(int(time.time()))))

