from math import floor
import time
import RPi.GPIO as GPIO
import subprocess

class Stepper:
    def __init__(self, pw: int, name: str, dirPin: int, stepPin: int, lowerLim: float, upperLim: float, encA: int, encB: int):
        self.pw = pw    # pulse width for moving the stepper, controlls the speed. Shorter p$
        self.currentAngle = 0   
        self.deltaAng = 1.8     # stepper is currently set to have 200 steps per revolution.$
        self.name = name
        self.dirPin = dirPin    # pin number to controll this stepper
        self.stepPin = stepPin
        self.lowerLim = lowerLim    #limits on how far stepper can turn
        self.upperLim = upperLim
        self.encA = encA
        self.encB = encB

        file = open("Calibration/" + self.name, "r")             # read where the stepper is from the txt file of the same name
        self.currentAngle = float(file.read())
        file.close()

    # move stepper motor to angle in degrees
    # if it is not a multiple of 1.8 it will be rounded down to a multiple of 1.8
    def moveToAngle(self, angle: float) -> None:
        angle = self.deltaAng * floor(angle/self.deltaAng)      # rounds angle down to multiples of 1.8

        theta = abs(angle - self.currentAngle)          # angle stepper needs to sweep through
        
        n = round(theta / self.deltaAng)      # number of steps to take for give 

        if (self.currentAngle > angle):
            GPIO.output(self.dirPin, 1)
        else:
            GPIO.output(self.dirPin, 0)
        # start encoder cpp program if we are gonna move
        if (n > 0):
            print(self.name + " encoder active")
            subprocess.Popen(["./Calibration/encoder", str(self.encA), str(self.encB), "Calibration/"+self.name])
            time.sleep(1)
        # pulses the gpio pin controlling stepper
        for i in range(n):
            GPIO.output(self.stepPin, 1)
            time.sleep(self.pw * 1e-6)
            GPIO.output(self.stepPin, 0)
            time.sleep(self.pw * 1e-6)
        time.sleep(1)

        file = open("Calibration/" + self.name, "r")             # read where the stepper is from the txt file of the same name
        self.currentAngle = float(file.read())
        file.close()

        if (round(self.currentAngle - angle) != 0):
            print("ENCODER : angle mismatch")
            self.moveToAngle(angle)

        print("moved stepper " + self.name + " to angle " + str(self.currentAngle) + " with " + str(n) + " steps!")
        GPIO.output(self.dirPin, 0)
        return

    # checks if stepper motor can move to a give angle based on its limits
    # returns false if angle is out of bounds, else true
    def canMoveTo(self, angle: float) -> bool:
        if(angle > self.upperLim):
            print(self.name + " Stepper cannot move to " + str(angle) + " degrees. the upper limit is " + str(self.upperLim) + " degrees \n")
            return 0
        elif(angle < self.lowerLim):
            print(self.name + " Stepper cannot move to " + str(angle) + " degrees. the lower limit is " + str(self.lowerLim) + " degrees \n")
            return 0
        else:
            return 1

    def status(self) -> None:
        print("\n" + self.name + " stepper's current status")
        print("-----------------------------------")
        print("current angle = " + str(self.currentAngle))
        print("pulse width = " + str(self.pw) + " microseconds + \n")
        return
