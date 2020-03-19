# SelfDirveCar_OpenCV_MLP_RaspberryPi

**基于树莓派与Opencv和MLP神经网络搭建的自动驾驶小车(Self driving car based on raspberry pie and opencv and MLP Neural Network)**

本项目采用的机器学习的MLP算法，本质上是一个多分类问题。系统复杂度低，集成性高。

## 说明

本项目使用arduino，树莓派等硬件模块，设计了一种采用摄像头，并使用MLP神经网络做出行为决策进行路径识别的自动驾驶小车。主要设计方法如下，用arduino、树莓派和摄像头等模块为主的硬件环境搭建小车。小车将摄像头采集到的数据发送到上位机。上位机保存图像作为神经网络训练集，调用OpenCV，numpy等工具进行处理。上位机搭建神经网络并训练模型。上位机接收图像数据，加载训练模型，解算图像得出控制参数发送给小车。

最终，通过对相关软件和硬件的开发，实现了对小车硬件环境的搭建和上位机软件环境的搭建。经过测试，验证了小车可以使用摄像头进行图像采集并由上位机处理保存，上位机可以训练MLP神经网络得到模型，通过调用网络模型小车可以在特定路径下做出沿当前路径行驶、转弯或停止等决策。

这个项目是基于OpenCV和树莓派的一个自动驾驶小车的系统设计与实现。项目整体分为两个部分，基于树莓派的硬件部分与基于opencv的算法部分。
OpenCV在该项目中主要使用在2个方面：

1、对输入图像的处理，调用了CV中的灰度化、感兴趣的区域选取等方法；

2、神经网络算法 ，调用了opencv的ML库中的多层感知机模型（MLP）来对输入图像进行分类。

树莓派在该项目中主要用在2个方面：

1、配合树莓派摄像头收集信息，

2、通过socket与上位机通讯。
另外，项目中的小车的硬件还使用了arduino、蓝牙、电机驱动器等模块。目的是通过蓝牙连接arduinoh和我的电脑，使我的电脑可以通过蓝牙发送指令给arduino来控制小车的前进、后退等行为。

想要实现这个项目，首先，自然需要搭建好一个小车。
该小车在搭建使用的硬件模块清单如下：
树莓派3b+， 树莓派原装摄像头， 包含电机的小车车体， 电机驱动模块，arduino nano开发版， 蓝牙主机模块， 蓝牙从机模块。
小车整体硬件主要的部分为以上所示但要做完整的小车搭建，还是需要一些其他实验工具来为小车做焊接固定、调试模块等工序的。
因此诸如电烙铁、螺钉、USB转TLL模块也是需要准备的。

## 自动驾驶小车的搭建

小车的硬件环境设计使用arduino为控制核心驱动电机运转，树莓派控制摄像头传感器采集路况信息，用于实现电机驱动小车运转以及传感器采集数据。此外在硬件方面还包括电源和蓝牙模块，用于给小车供电以及接受上位机数据。

### 小车硬件的整体设计 

本设计的项目总体设计图如图 所示。

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319204806868.png" alt="image-20200319204806868" style="zoom: 67%;" />

​														图  自动驾驶小车系统总体设计图

小车以 arduino 和树莓派为核心，并搭载有摄像头感器模块，蓝牙等硬件模块作为下位机的硬件部分，用 PC 机端相关程序为作为上位机。 Arduino 和 树莓派之间采用串口进行通信，Arduino 主要用于负责小车的运动控制，通过串口接收来自树莓派所发来的控制信息，树莓派主要负责图像的接收和发送，还有与上位机间的信息传递，树莓派与上位机之间通过无线局域网络进行连接。PC 机主要负责接收树莓派传来的图像数据，并利用 PC机对神经网络进行训练，预测小车的运动方向并返回给树莓派。

### 小车底层驱动的搭建

在获取到一个小车的车体后，就可以开始搭建小车的硬件模块了。下面是一些主要的部件。

### 电源

 电源模块主要由三块18650的电池构成和LM2596S DC-DC稳压降压模块构成，电源总电压12.8V。其中DC降压模块带有显示功能，可以显示当前电压以及输出电压的大小。186650电池如下左图所示，LM2596S DC-DC稳压模块如右图所示。

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319205413823.png" alt="image-20200319205413823" style="zoom: 50%;" />

### 底层驱动

 小车使用减速直流电机，如图2.2.2-1所示，使用TB6612FNG驱动模块，如图所示。通过写好的arduino程序，可以实现arduino控制器发送PWM波驱动TB6612FNG驱动器控制两路电机，利用差速转向，实现小车前进、后退、转向的功能。并且还可以通过打开串口接收由主机蓝牙模块发送过来的控制参数调整小车各引脚电平和PWM波的变化，来实现远程控制小车的功能。

点击驱动如下左图所示，TB6612FNG驱动模块如下右图所示。

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319205528969.png" alt="image-20200319205528969" style="zoom: 50%;" />

使用开源硬件arduino作为小车的底层驱控制核心，实现对小车方向进行控制，诸如，前进后退，差速转向等。arduino实物图如下：

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319205707973.png" alt="image-20200319205707973" style="zoom: 67%;" />

硬件原理图如下：

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319205724763.png" alt="image-20200319205724763" style="zoom: 67%;" />

### 蓝牙通信

 在采集训练数据训练神经网络训练和自动驾驶途中，都对小车的远程控制有一定要求，因此在这里采用蓝牙模块，来实现对小车的远程控制。其中小车搭载HC-06蓝牙（如图所示）从机接收模块，上位机接HC-05蓝牙主机（如图所示）发送模块。通过串口助手，USB转TLL等工具配置好蓝牙模块后，即可在主机端采集发送数据，从机端接收到数据。之后，便可在上位机端编程，实现上位机通过HC-05蓝牙主机模块发送控制信号，HC-06蓝牙从机模块接收到控制信息发送给arduino后，控制小车进行指定的动作。

蓝牙HC-06如左图所示，蓝牙HC-05如右图所示。

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319205901443.png" alt="image-20200319205901443" style="zoom:50%;" />

### 树莓派与摄像头

数据采集与处理模块在系统的硬件设计上，主要包含由树莓派摄像头Pi camera构成的数据采集模块以及有树莓派构成的数据处理模块。其中树莓派摄像头主要功能为采集视频和图像数据，树莓派主要功能包括，驱动摄像头运转以及通过socket网络通信，传输视频和图像数据到上位机做进一步处理。

树莓派实物如左图所示，树莓派摄像头如右图所示。

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319210059796.png" alt="image-20200319210059796" style="zoom: 33%;" />



### 小车实物

除了以上硬件模块，还需自购一块小车车体。以小车车体作为依托，完成硬件的连接，小车就算构建完成了。

小车构建完成的实物如下图所示：

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319210317681.png" alt="image-20200319210317681" style="zoom:50%;" />![image-20200319211131437](C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319211131437.png)



其次，在小车硬件环境搭建好后，需要完成arduino驱动程序和树莓派端的数据采集与发送程序的编写。

小车arduino的驱动程序路径为:  [SelfDirveCar_OpenCV_MLP_RaspberryPi/ fourlun / fourlun.ino](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/blob/master/fourlun/fourlun.ino)

树莓派上的程序路径为 : [SelfDirveCar_OpenCV_MLP_RaspberryPi/pi/stream_client.py /](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/blob/master/pi/stream_client.py)

在小车搭建完成后，我们就可以依托其进行后续神经网络和控制算法等功能的开发了。

## 小车神经网络和控制算法设计

遵循AI开发的数据收集->模型训练->模型部署的原则，我们的软件部分也分为以下3部分：
1.收集训练数据的程序
2.训练算法模型的程序
3.模型部署应用的程序
这三个部分，分别对应着我项目中的三个.py文件。

包括，收集训练数据的程序设计的实现；训练ANN_MLP模型的程序设计的实现；以及自动驾驶功能模块的软件设计的实现。

###  收集训练数据获取数据集

该模块的功能是在PC机上收集树莓派端传输的图像以作为训练数据并形成数据集的功能。

收集的数据应该是我们提前布置好的实验场景下的跑道图片，为了使特征明显，采用在深色地面上用白纸铺设跑道的方法。

在采集数据的过程中，要保证树莓派和上位机连在同一个网段下。具体的连接方法为：分别运行下面两个代码在上位机端和树莓派端。

收集训练数据制作数据集的代码路径如下:

上位机端运行的代码： [SelfDirveCar_OpenCV_MLP_RaspberryPi/collect_training_data3.py /](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/blob/master/collect_training_data3.py)

树莓派端运行的代码：[SelfDirveCar_OpenCV_MLP_RaspberryPi/pi/stream_client.py /](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/blob/master/pi/stream_client.py)

铺设好跑道后，小车树莓派摄像头采集到的图片，经过灰度处理后，如下所示：

![image-20200319221329518](C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319221329518.png)



其中，在采集训练数据阶段，我使用电脑通过蓝牙模块无线控制小车，在规定的跑道上行驶一圈。
树莓派与摄像头会在这段时间一直开启，如果我按下电脑上指定小车前进的按键后，小车就会向前一步，同时保存下按下按键时刻的视频帧作为训练图片和前进指令作为标签。

这样，当我绕实验环境的地形多行驶几圈后，小车就会收集够足够的带标签的训练数据。

项目上传的目录中，有已经收集到数据，路径为 [SelfDirveCar_OpenCV_MLP_RaspberryPi/training_images/](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/tree/master/training_images)

程序的运行方法结果如下：

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319213835555.png" alt="image-20200319213835555" style="zoom:50%;" />

我们使用的机器学习的MLP算法模型来进行训练，因此，数据需要手动进行特征提取与转换，才能得到可被模型接受的数据。

转换后的数据，在收集训练数据完成以后，会自动存放设定好的路径下。

转换后的数据存放路径为 ：[SelfDirveCar_OpenCV_MLP_RaspberryPi/training_data/](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/tree/master/training_data)

### 训练模型

运行训练算法模型的程序，我们就可以将MLP模型通过搜集好的训练数据，在上位机上训练了。

执行训练程序后，就可以完成训练，得到参数模型了。

训练模型的代码路径为： [SelfDirveCar_OpenCV_MLP_RaspberryPi/mlp_training.py /]( https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/blob/master/mlp_training.py)

训练之后，就可以得到mlp在我们获取的数据集的参数模型了。

参数模型的保存路径为：[SelfDirveCar_OpenCV_MLP_RaspberryPi/mlp_xml/](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/tree/master/mlp_xml)

模型训练的结果如下图所示：

![image-20200319221454960](C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319221454960.png)

可见输出结果中， 神经网络训练时间为 710秒， 训练集错误率 4.30%， 测试集错误率 6.40%。  



### 调用模型实现自动驾驶

最后，将模型应用到我们的布置的实验场景下，就可以实现小车自动驾驶功能了。

将小车放在预先铺设跑道好的实验环境下，并保证树莓派和上位机连接在同一个局域网下，具体的连接方法为：分别运行下面两个代码在上位机端和树莓派端。

上位机端运行的程序路径为：[SelfDirveCar_OpenCV_MLP_RaspberryPi/rc_driver.py /](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/blob/master/rc_driver.py)

树莓派端运行程序路径为：[SelfDirveCar_OpenCV_MLP_RaspberryPi/pi/stream_client.py /](https://github.com/Aismarter/SelfDirveCar_OpenCV_MLP_RaspberryPi/blob/master/pi/stream_client.py)

在这里又有2点需要强调一下。
1、首先，在小车自动驾驶的应用过程中，是复用了在收集训练数据中树莓派摄像头一直获取数据摄像头数据的代码的。
这段代码运行在树莓派里，通过socket与上位机通讯，一直将摄像头所看见的视频帧发送到上位机去处理。上位机收到图片，就调用MLP的模型参数，输出检测的结果。

2、其次，上位机输出的检测结果，是通过蓝牙发送arduino来控制小车的运转的。
这样，我的电脑作为服务器，一直监听小车上树莓派发送过来的摄像头捕获的数据。一旦收到数据，就在上位机执行inference过程，并通过蓝牙将数据发送给小车的arduino控制电机驱动模块。

上位机程序运行的效果如下图：

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319223942792.png" alt="image-20200319223942792" style="zoom:50%;" />

可以看见在被图过的黄色区域，有通过串口转蓝牙发送给小车的控制信号。

于是，小车将通过树莓派将数据传送到电脑上，电脑执行完推理过程得到下一步下车要运行的结果，再通过蓝牙将控制信息发送给小车，让小车做出前进、后退等行动。
通过这种机制，将小车放在一个实验环境下，小车就可以根据现场的环境信息，自动做出或是前进、或是停止的行为了。

附加几张小车在实验室环境下测试的图片。如下：

<img src="C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319224200922.png" alt="image-20200319224200922" style="zoom:50%;" />

![image-20200319224231347](C:\Users\zhangzhiyong\AppData\Roaming\Typora\typora-user-images\image-20200319224231347.png)

## 后续说明

本项目遵行**GNU GPLv2**协议

## 一点思考

整个项目完成了初步的小车自动驾驶功能，但后续仍然可以在此基础上做优化与改进。可以改进的点为：

1. 通过opencv的颜色识别算法来做红绿灯识别。
2. 通过改进双目摄像头测距，增加超声波或雷达模块，拓展小车的避障、超车等功能。
3. 通过深度学习方法，来改进传统视觉方法对光照、雾气、阴影等干扰过于敏感的问题。
4. 如果有场景需求，也可尝试与不同的调度算法融合，增强对场景的适应性。
5. 通过以上对硬件的扩展，可以尝试将算法应用不同的机械上，比如，无人机、机械臂、AGV小车等场景。
6. 通过对连接方法的拓展，结合物联网、云计算等技术、可以考虑在部分领域做进一步深化。
