import numpy as np
import cv2
import serial
import pygame
from pygame.locals import *
import urllib.request
import time
import os
import sys
import socket
import struct


class CollectTrainingData(object):
    
    def __init__(self):

        HOST = '192.168.43.113'
        PORT = 8000
        self.sock = socket.socket()
        # 启动socket，设置监听端口为8000，接受所有ip的连接
        self.sock.bind((HOST, PORT))
        self.sock.listen(1)
        # 接受一个客户端连接
        self.connection = self.sock.accept()[0].makefile('rb')       
        
        
        #连接到串口
        self.ser = serial.Serial('COM6', 9600, timeout=1)
        self.send_inst = True

        # 创建标签
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()
        pygame.display.set_mode((400, 300))
        self.collect_image()
    #收集图像
    def collect_image(self):

        saved_frame = 0   #已经保存的帧
        total_frame = 0   #所有的帧

        # 从摄像头收集图像
        print('Start collecting images...')
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))      #图像的大小是 1 * 38400   
        label_array = np.zeros((1, 4), 'float') #图像标签的大小是 1 * 4 

        #  逐帧获取图像
        try:
            frame = 1
            

            while self.send_inst:
                    # 获取数据帧
                    image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                    if not image_len:
                        break

                    recv_bytes = b''
                    recv_bytes += self.connection.read(image_len)
                    image = cv2.imdecode(np.frombuffer(recv_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    # 选择图片的下半部分
                    roi = image[120:240, :]
                    
                    # 保存整张图片
                    cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
                    
                    #展示整张图片
                    cv2.imshow('image', image)
                    
                    # 下半部分的图片转换成一维
                    temp_array = roi.reshape(1, 38400).astype(np.float32)
                    
                    frame += 1
                    total_frame += 1
                    #如果输入是指定小车运动的6个操作之一，
                    #那么这个frame 就保存起来，saved_frame += 1，
                    #而不管输入的操作是什么，`total_frame += 1`

                    # 获取用户的输入并执行
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # 复合操作
                            if key_input[pygame.K_o]and key_input[pygame.K_p]:
                                print("Forward Right")
                                image_array = np.vstack((image_array, temp_array))
                                #np.vstack:按垂直方向（行顺序）堆叠数组构成一个新的数组
                                label_array = np.vstack((label_array, self.k[1]))
                                #拼成一个整图片，上半部分是空白的， 下半部分是从摄像头中获取的，标签也类似
                                saved_frame += 1
                                self.ser.write(b'5')

                            elif key_input[pygame.K_i]and key_input[pygame.K_u]:
                                print("Forward Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.ser.write(b'6')

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                                print("Reverse Right")
                                self.ser.write(b'7')
                            
                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                                print("Reverse Left")
                                self.ser.write(b'8')

                            # 单个操作
                            elif key_input[pygame.K_UP]:
                                print("Forward")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                self.ser.write(b'1')

                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                self.ser.write(b'2')
                            
                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                self.ser.write(b'3')

                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.ser.write(b'4')

                            elif key_input[pygame.K_x] or key_input[pygame.K_q]:
                                print('exit')
                                self.send_inst = False
                                self.ser.write(b'0')
                                break
                                    
                        elif event.type == pygame.KEYUP:
                            self.ser.write(b'0')

            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # 把train的图片和label转换为numpy，保存
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:    
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            #如果你想将多个数组保存到一个文件中的话，可以使用numpy.savez函数。
            #savez函数的第一个参数是文件名，其后的参数都是需要保存的数组，
            #也可以使用关键字参数为数组起一个名字，
            #非关键字参数传递的数组会自动起名为arr_0, arr_1, …。
            #savez函数输出的是一个压缩文件(扩展名为npz)，
            #其中每个文件都是一个save函数保存的npy文件，文件名对应于数组名。
            #load函数自动识别npz文件，并且返回一个类似于字典的对象，
            #可以通过数组名作为关键字获取数组的内容：

            except IOError as e:
                print(e)

            e2 = cv2.getTickCount()
            # 计算服务持续的时间
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Streaming duration:', time0)

            print((train.shape))
            print((train_labels.shape))
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

        finally:
            print('Done')

if __name__ == '__main__':
    CollectTrainingData()
