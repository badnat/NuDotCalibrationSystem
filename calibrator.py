from stepper import Stepper
import time
import RPi.GPIO as GPIO
from math import pi

class Calibrator:
    def __init__(self, zStep: Stepper, rotStep: Stepper, incStep: Stepper):
        self.zStep = zStep
        self.rotStep = rotStep
        self.incStep = incStep
        
        GPIO.setwarnings(0)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.zStep.dirPin, GPIO.OUT)
        GPIO.setup(self.zStep.stepPin, GPIO.OUT)
        GPIO.setup(self.rotStep.dirPin, GPIO.OUT)
        GPIO.setup(self.rotStep.stepPin, GPIO.OUT)
        GPIO.setup(self.incStep.dirPin, GPIO.OUT)
        GPIO.setup(self.incStep.stepPin, GPIO.OUT)

    def calibrate(self, zAng: float, rotAng: float, incAng: float) -> None:
        b = self.moveSteppers(zAng, rotAng, incAng)
        if (b):
            print("steppers moved into position")
            return
        else:
            return

    
    # return 1 if succesfully move all steppers
    # return 0 if any angles are out of bounds
    def moveSteppers(self, zAng: float, rotAng: float, incAng: float) -> bool:
        # check if angles provided are allowed
        b = 1
        b = b and self.zStep.canMoveTo(zAng)
        b = b and self.rotStep.canMoveTo(rotAng)
        b = b and self.incStep.canMoveTo(incAng)

        # Cancel calibration if any checks return 0
        # move steppers to desired angles if all checks are 1
        if (not b):
            print("Canceling Calibration")
            return 0
        else:
            self.zStep.moveToAngle(zAng)
            time.sleep(1)
            self.rotStep.moveToAngle(rotAng)
            time.sleep(1)
            self.incStep.moveToAngle(incAng)
            return 1

    def recordCalibration(self) -> None:
        return

    def zero(self) -> None:
        self.moveSteppers(0, 0, 0)
        return
    
    # returns the angle the stepper needs to go to inorder to move the z motor a distance in meters
    # distance in meters, radius in meters
    def distanceToAngle(self, distance: float, radius: float) -> float:
        return (distance/radius) * (180 / pi)
    
