import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

length = 10

def led_on(pin):
##    GPIO.setup(pin, GPIO.OUT)
    print("LIGHT ON")
    GPIO.output(pin,GPIO.HIGH)

##    time.sleep(1)

def led_off(pin):
##    GPIO.setup(pin, GPIO.OUT)
    print('LIGHT off')
    GPIO.output(pin,GPIO.LOW)
##    time.sleep(1)


def other_light():
    GPIO.setup(25, GPIO.OUT)

    print("LIGHT 1 ", x)

    GPIO.output(25,GPIO.HIGH)

    time.sleep(1)

    print('LIGHT 1 off')
    GPIO.output(25,GPIO.LOW)
    time.sleep(1)

