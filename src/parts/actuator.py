"""Piece movement

Move pieces on board
"""

from time import sleep
from threading import Thread
from gpiozero import OutputDevice, Button
from enum import Enum
from constants import Pins, MAX_STEPS_X, MAX_STEPS_Y, STEPS_PER_SQUARE
import RPi.GPIO as GPIO
from logger import logger

GPIO.setmode(GPIO.BCM)

DEFAULT_DELAY = 0.001

class StepperMagnetActuator:
    def __init__(self):
        self.homeX = Button(Pins.HOME_X, pull_up=True)
        self.homeY = Button(Pins.HOME_Y, pull_up=True)
        self.steppers = A4988HBotSteppers()

        self.x = None
        self.y = None

    def shutdown(self):
        self.steppers.shutdown()
    
    def home(self):
        self.steppers.disable_sleeping()

        # Move forward slightly to avoid hitting Y homing switch
        self.steppers.step(50, MoveDirection.UP)

        # Move to X home
        steps = 0
        while not self.homeX.is_pressed:
            self.steppers.step(20, MoveDirection.LEFT, .0035)
            steps += 1
            if steps > MAX_STEPS_X:
                raise Exception("X home not found")

        # Move to Y home
        steps = 0
        while not self.homeY.is_pressed:
            self.steppers.step(1, MoveDirection.DOWN, .004)
            steps += 1
            if steps > MAX_STEPS_Y:
                raise Exception("Y home not found")

        self.x = 0
        self.y = 0

        self.setSquare(0, 1)

        self.steppers.enable_sleeping()

    def setXY(self, x, y):
        if self.x is None or self.y is None:
            self.home()

        if x > MAX_STEPS_X or y > MAX_STEPS_Y:
            raise ValueError("Position out of range")

        if x == self.x and y == self.y:
            return

        # Move to Y
        if y > self.y:
            self.steppers.step((y - self.y), MoveDirection.UP)
        elif y < self.y:
            self.steppers.step((self.y - y), MoveDirection.DOWN)

        # Move to X
        if x > self.x:
            self.steppers.step((x - self.x), MoveDirection.RIGHT)
        elif x < self.x:
            self.steppers.step((self.x - x), MoveDirection.LEFT)

        self.x = x
        self.y = y

    def setSquare(self, x, y):
        # Squares 1-8 are chessboard squares. In the X dimension, 0 is the empty space next to the left-most file
        h = STEPS_PER_SQUARE // 2
        self.setXY((x + 1) * STEPS_PER_SQUARE - h, y * STEPS_PER_SQUARE - h)


MoveDirection = Enum('Direction', ['RIGHT', 'LEFT', 'UP', 'DOWN'])
    
class A4988HBotSteppers:
    def __init__(self):
        self.step1 = OutputDevice(Pins.STEP1)
        self.step2 = OutputDevice(Pins.STEP2)
        self.dir1 = OutputDevice(Pins.DIR1)
        self.dir2 = OutputDevice(Pins.DIR2)
        self.slp = OutputDevice(Pins.STEPSLP)

        self.thread = None
        self._disable_sleep = False

        self.reset()

    def reset(self):
        if self.thread and self.thread.is_alive():
            self.thread.join()
        
        self.step1.off()
        self.step2.off()
        self.dir1.off()
        self.dir2.off()
        self.slp.off() if not self._disable_sleep else self.slp.on()

    def shutdown(self):
        self.reset()
        # Sleep drivers before shutdown
        self.slp.close()

        GPIO.setup(Pins.STEPSLP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        logger.debug("Steppers shutdown")

    def disable_sleeping(self):
        self.slp.on()
        self._disable_sleep = True
        sleep(0.1)

    def enable_sleeping(self):
        sleep(0.1)
        self.slp.off()
        self._disable_sleep = False

    def step(self, steps, direction: MoveDirection, delay = DEFAULT_DELAY, threaded = False):
        self.reset()
        if threaded:
            self.thread = Thread(target=self._step, args=(steps, delay, direction))
            self.thread.start()
        else:
            self._step(steps, delay, direction)

    def _step(self, steps, delay, direction):
        if not self._disable_sleep:
            self.slp.on()
            sleep(0.1)

        if direction == MoveDirection.RIGHT:
            self.dir1.off()
            self.dir2.on()
        elif direction == MoveDirection.LEFT:
            self.dir1.on()
            self.dir2.off()
        elif direction == MoveDirection.UP:
            self.dir1.on()
            self.dir2.on()
        elif direction == MoveDirection.DOWN:
            self.dir1.off()
            self.dir2.off()
        else:
            raise ValueError("Invalid move direction")

        for i in range(steps):
            self.step1.on()
            self.step2.on()
            sleep(delay)
            self.step1.off()
            self.step2.off()
            sleep(delay)

        if not self._disable_sleep:
            sleep(0.1)
            self.slp.off()