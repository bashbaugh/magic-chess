import RPi.GPIO as GPIO
from time import sleep
from random import randrange

pin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, GPIO.LOW)
sleep(10)
GPIO.output(pin, GPIO.HIGH)

# while True:
#   GPIO.output(pin, GPIO.HIGH)
#   sleep(2)
#   GPIO.output(pin, GPIO.LOW)
#   sleep(2)
