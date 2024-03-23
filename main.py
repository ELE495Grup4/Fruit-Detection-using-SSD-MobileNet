#!/usr/bin/env python3
import threading
from server import start_server_in_thread
from control import control
from detectnet import detectFruit, buildModel

if __name__ == '__main__':
    
    camera, net,output = buildModel()
    start_server_in_thread()
    thread=threading.Thread(target=control)
    thread.start()
    detectFruit(camera, net,output)
# Do other things here while the server is running in a separate thread
