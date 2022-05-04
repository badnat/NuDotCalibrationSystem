import sys
from stepper import Stepper
from calibrator import Calibrator

# step and dir are pin numbers
# A and B are GPIO numbers

zPW = 5000
zDir = 15
zStep = 13
# angle upper and lower bound
zLower = 0
zUpper = 5730
zA = 2
zB = 3

rotPW = 5000
rotDir = 10
rotStep = 8
# angle upper and lower bound
rotLower = -180
rotUpper = 180
rotA = 5
rotB = 6


incPW = 5000
incDir = 16
incStep = 18
# angle upper and lower bound
incLower = -90
incUpper = 90
incA = 8
incB = 25

# returns a tuple of floats 
# z (in meters), rot (in degrees), inc (in degrees)
def readCoords():
    args = sys.argv[1:]
    return (float(args[0]), float(args[1]), float(args[2]))


def main():
    try:
        zDist, rotAng, incAng = readCoords()
    except IndexError:
        print("please enter params: <z distance in meters> <rotation angle in degrees> <inclination angle in degrees>")
        return
        
    zStepper = Stepper(zPW, "z", zDir, zStep, zLower, zUpper, zA, zB)
    rotStepper = Stepper(rotPW, "rot", rotDir, rotStep, rotLower, rotUpper, rotA, rotB)
    incStepper = Stepper(incPW, "inc", incDir, incStep, incLower, incUpper, incA, incB)
    cal = Calibrator(zStepper, rotStepper, incStepper)
    zAng = cal.distanceToAngle(zDist, 1e-2)
    cal.calibrate(zAng, rotAng, incAng)

if __name__ == "__main__":
    main()
