import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


length = 10

for x in range(length):
    GPIO.setup(22, GPIO.OUT)

    print("LIGHT 1 ", x)

    GPIO.output(22,GPIO.HIGH)

    time.sleep(1)

    print('LIGHT 1 off')
    GPIO.output(22,GPIO.LOW)
    time.sleep(1)

    GPIO.setup(25, GPIO.OUT)

    print("LIGHT 1 ", x)

    GPIO.output(25,GPIO.HIGH)

    time.sleep(1)

    print('LIGHT 1 off')
    GPIO.output(25,GPIO.LOW)
    time.sleep(1)


    x += 1

    
    if x == 6:
        print('hit limit. stopping')
        break
