
import io
import socket
import struct
import time
import picamera


# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.43.123', 8000))
connection = client_socket.makefile('wb')

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)      # pi camera 设置
        camera.framerate = 10               # 10 frames/sec
        time.sleep(2)                       # 给 2 秒钟的时间让摄像头预热 
        
		# 记录一个开始时间，并构建一个流来存储捕获的图片数据
        # 我们可以直接讲捕获的数据流传给服务器，但为了捕获我们的图像长度，
        # 我们暂且阻碍传输，并等待捕获完成，并获取图长度组建数据包
		start = time.time()
        stream = io.BytesIO()
        
        # send jpeg format video stream # 将数据写入流中
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
             # 将数据流的指针指向起始位置
			connection.write(stream.read())
            
            # 如果我们的等待的连接时间大于600秒则退出循环
			if time.time() - start > 600:
                break
            stream.seek(0)
            stream.truncate()
			
    connection.write(struct.pack('<L', 0))
	 # 循环结束，写一个长度为0的数据包，告知服务器我们已经完成了整个操作。
finally:
    connection.close()
    client_socket.close()
