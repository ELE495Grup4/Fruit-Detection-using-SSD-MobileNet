from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput
import Jetson.GPIO as GPIO
import server
import control
import time

class detect:
     frame=1

import sys,argparse

def buildModel():


    # create video sources and outputs
    camera = videoSource("/dev/video1")
    output = videoOutput()

    net = detectNet(argv=[f"--model=/home/samil/Desktop/jetson-inference/python/training/detection/ssd/models/ssd-mobilenet-fruit/ssd-mobilenet.onnx", 
                        f"--labels=/home/samil/Desktop/jetson-inference/python/training/detection/ssd/models/ssd-mobilenet-fruit/labels.txt", 
                        f"--threshold=0.4", "--input-blob=input_0", "--output-cvg=scores", "--output-bbox=boxes"])
    
    return camera, net, output


def detectFruit(camera, net, output):
    # process frames until EOS or the user exits
    # parse the command line
    
    print(control.variables.sensor_value)
    time_flag =0
    while True:
        print("sensor:",control.variables.sensor_value)
        print("flag:",time_flag)
        if time_flag==1:
            time.sleep(3)
            time_flag=0
        while control.variables.sensor_value==1:
            print(control.variables.sensor_value)
            
        start_time=time.time()
        while control.variables.sensor_value==0 and time_flag == 0:
            print("sensor:",control.variables.sensor_value)
            print("flag:",time_flag)
        # capture the next image
            
            img = camera.Capture()
            if img is None: # timeout
                continue  
                
            # detect objects in the image (with overlay)
            detections = net.Detect(img) #overlay="box,labels,conf"

            if len(detections) > 3: # sadece 3 cisim iken calışır  
                continue

            if len(detections) != 0:
                detect.frame+=1
            
            print(detect.frame)

            # print the detections
            print("detected {:d} objects in image".format(len(detections)))
            
            detected_classes = []   
            for detection in detections:
                if(detection.Confidence < 0.35) : 
                    detection.ClassID = 0 # Unknown Object

                detected_classes.append(net.GetClassDesc(detection.ClassID))
                
            print(detected_classes)
            # render the image
            output.Render(img)

            for meyve in detected_classes:

                if meyve == "Apple":
                    server.Main.elma += 1
                if meyve == "Orange" :
                    server.Main.portakal += 1  
                if meyve == "Banana":
                    server.Main.muz += 1
                if meyve == "Pear" :
                    server.Main.armut += 1  
                if meyve == "Strawberry":
                    server.Main.cilek += 1 
                if meyve == "Grape":
                    server.Main.uzum += 1 
                if meyve == "Unknown" :
                    server.Main.tanimsiz += 1

            control.variables.sensor_value = GPIO.input(control.variables.sensor_pin)
            stop_time = time.time()
            passed_time=stop_time - start_time
            print("passed time:",passed_time)
            if int(passed_time) == 3:
                time_flag=1

            # update the title bar
            #output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))
            
            # print out performance info
            #net.PrintProfilerTimes()
            
            # exit on input/output EOS
            if not camera.IsStreaming() : #or not output.IsStreaming()
                break
        