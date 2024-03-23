import Jetson.GPIO as GPIO
import time
import detectnet 
import server
class variables:
    sensor_pin = 15
    sensor_value = -1
    flag = 1
    # Motor Pin Configuration (assuming L298N motor driver)
    IN1 = 32  # IN1 pin of L298N
    IN2 = 36  # IN2 pin of L298N


# Set GPIO pin numbering mode
GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

# Set up GPIO pins for motor control (assuming L298N)
GPIO.setup(variables.IN1, GPIO.OUT)
GPIO.setup(variables.IN2, GPIO.OUT)

GPIO.setup(variables.sensor_pin, GPIO.IN)


def control():
    
    try:
        while True:
	    
            # Sensor value reading
            variables.sensor_value = GPIO.input(variables.sensor_pin)
            
            if variables.sensor_value == 0 and variables.flag==1:
                
                server.Main.elma=0
                server.Main.armut=0
                server.Main.cilek=0
                server.Main.portakal=0
                server.Main.muz=0
                server.Main.uzum=0

                detectnet.detect.frame =1
                GPIO.output(variables.IN1, GPIO.LOW)
                GPIO.output(variables.IN2, GPIO.LOW)
                #rint("Motor stopped...")
                #print("Engel algilandi!")
                time.sleep(3)
                variables.flag = 0

            elif variables.flag == 0 and variables.sensor_value == 0:
                GPIO.output(variables.IN1, GPIO.HIGH)
                GPIO.output(variables.IN2, GPIO.LOW)
                #print("Motor running...")
                #print("algilandiktan sonra kutu bitimine kadar devam.")
                variables.flag = 1
                server.Main.toplam_armut += round(server.Main.armut/detectnet.detect.frame)
                server.Main.toplam_elma += round(server.Main.elma/detectnet.detect.frame)
                server.Main.toplam_cilek += round(server.Main.cilek/detectnet.detect.frame)
                server.Main.toplam_muz += round(server.Main.muz/detectnet.detect.frame)
                server.Main.toplam_portakal += round(server.Main.portakal/detectnet.detect.frame)
                server.Main.toplam_uzum += round(server.Main.uzum/detectnet.detect.frame)
                server.Main.toplam_tanimsiz += round(server.Main.tanimsiz/detectnet.detect.frame)

                server.Main.elma=server.Main.elma/detectnet.detect.frame
                server.Main.armut=server.Main.armut/detectnet.detect.frame
                server.Main.cilek=server.Main.cilek/detectnet.detect.frame
                server.Main.portakal=server.Main.portakal/detectnet.detect.frame
                server.Main.muz=server.Main.muz/detectnet.detect.frame
                server.Main.uzum=server.Main.uzum/detectnet.detect.frame
                server.Main.tanimsiz=server.Main.tanimsiz/detectnet.detect.frame

                detectnet.detect.frame = 1
                time.sleep(3)

            else:  # This 'else' block might not be necessary
                GPIO.output(variables.IN1, GPIO.HIGH)
                GPIO.output(variables.IN2, GPIO.LOW)
                #print("Motor running...")
                #print("engel algilanmadi.")

    except KeyboardInterrupt:
        print("Program interrupted. Cleaning up...")
        GPIO.output(variables.IN1, GPIO.LOW)
        GPIO.output(variables.IN2, GPIO.LOW)
        GPIO.cleanup()