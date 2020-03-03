import threading
import socketserver
import serial
import cv2
import numpy as np
import math
import sys
import urllib.request
import socket
import struct


class NeuralNetwork(object):
#神经网络用的是opencv 自带的 ANN_MLP
    def __init__(self):
        self.model = cv2.ml.ANN_MLP_load('mlp_xml/mlp_1558587439.xml')
        #输入层是 38400  -> 32 ,其中 38400 是图片大小
        #从`mlp_xml/mlp.xml`加载网络结构和参数


    def predict(self, samples):
        ret, resp = self.model.predict(samples)
        return resp.argmax(-1)
        #预测下一步的动作

class RCControl(object):

    def __init__(self):
          self.ser = serial.Serial('COM6', 9600, timeout=1)

    def steer(self, prediction):
        if prediction == 2:
            self.ser.write(b'1')
            print("Forward")
        elif prediction == 0:
            self.ser.write(b'6')
            print("Left")
        elif prediction == 1:
            self.ser.write(b'5')
            print("Right")
        else:
            self.stop()

    def stop(self):
        self.ser.write(b'0')
        #根据预测值控制小车的方向
        #只有四种情况，2：向前，0：向左，1：向右，其他：不动。



class VideoStreamHandler(socketserver.StreamRequestHandler):
#视频流处理
        print('start videostream')
    

        model = NeuralNetwork()

        car = RCControl()

        def handle(self):      
                print('start image')
                # 获取视频帧
                try:

                    while True:
                        image_len = struct.unpack('<L', self.rfile.read(struct.calcsize('<L')))[0]
                        if not image_len:
                                break

                        recv_bytes = b''
                        recv_bytes += self.rfile.read(image_len)
                        gray = cv2.imdecode(np.frombuffer(recv_bytes, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                        image = cv2.imdecode(np.frombuffer(recv_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

                            # 取下半部分图像做特征向量
                        roi = gray[120:240, :]

                            # 拼接完整图像
                        image_array = roi.reshape(1, 38400).astype(np.float32)                     
                        cv2.imshow('image',image)
                       
    

                            # 预测
                        prediction = self.model.predict(image_array)

                            # 传输给小车

                        self.car.steer(prediction)
  

                    cv2.destroyAllWindows()

                finally:

                    print("Connection closed on the server video thread!")


    
class ThreadServer(object):
#线程管理器
    def server_thread(host, port):
        server = socketserver.TCPServer((host, port), VideoStreamHandler)  #实例化线程
        server.serve_forever()

    video_thread = threading.Thread(target=server_thread('192.168.43.113', 8000)) 
    video_thread.start()

if __name__ == '__main__':
    ThreadServer() 

