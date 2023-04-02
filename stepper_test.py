import RPi.GPIO as GPIO
from time import sleep
from random import randrange

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SLEEP_PIN = 26
500 
GPIO.setup(SLEEP_PIN, GPIO.OUT)

MAX_STEPS_X = 1600
MAX_STEPS_Y = 1400

class StepperHandler():

  def __init__(self, stepPin1, directionPin1, stepPin2, directionPin2):
    self.StepPin1 = stepPin1
    self.DirectionPin1 = directionPin1
    self.StepPin2 = stepPin2
    self.DirectionPin2 = directionPin2

    # Setup gpio pins
    GPIO.setup(self.StepPin1, GPIO.OUT)
    GPIO.setup(self.DirectionPin1, GPIO.OUT)
    GPIO.setup(self.StepPin2, GPIO.OUT)
    GPIO.setup(self.DirectionPin2, GPIO.OUT)

  def bothHigh(self):
    GPIO.output(self.StepPin1, GPIO.HIGH)
    GPIO.output(self.StepPin2, GPIO.HIGH)

  def bothLow(self):
    GPIO.output(self.StepPin1, GPIO.LOW)
    GPIO.output(self.StepPin2, GPIO.LOW)

  def step(self, stepsToTake, direction = 1, delay = 0.004):
    GPIO.output(SLEEP_PIN, GPIO.HIGH)

    sleep(0.1)

    # Set the directions from direction between 1 and 4
    if direction == 1:
      GPIO.output(self.DirectionPin1, GPIO.LOW)
      GPIO.output(self.DirectionPin2, GPIO.LOW)
    elif direction == 2:
      GPIO.output(self.DirectionPin1, GPIO.HIGH)
      GPIO.output(self.DirectionPin2, GPIO.LOW)
    elif direction == 3:
      GPIO.output(self.DirectionPin1, GPIO.LOW)
      GPIO.output(self.DirectionPin2, GPIO.HIGH)
    elif direction == 4:
      GPIO.output(self.DirectionPin1, GPIO.HIGH)
      GPIO.output(self.DirectionPin2, GPIO.HIGH)

    # Take requested number of steps
    for x in range(stepsToTake):
      # print("Step " + str(x))
      self.bothHigh()
      sleep(delay)
      self.bothLow()
      sleep(delay)

    GPIO.output(SLEEP_PIN, GPIO.LOW)
    

s = StepperHandler(22, 23, 24, 25)

# s.step(100, 2)
# s.step(200, 3)

# s.step(300, 1)
# s.step(150, 2)
# s.step(150, 3)
# s.step(300, 4)

while True:
  com = input("Enter <steps direction delay?>:")
  direction = int(com.split(" ")[1])
  steps = int(com.split(" ")[0])
  delay = 0.004 if len(com.split(" ")) < 3 else float(com.split(" ")[2])

  s.step(steps, direction, delay)


