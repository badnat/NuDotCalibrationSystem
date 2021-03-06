# NuDotCalibrationSystem

This project is for the NuDot Experiment https://jgruszko.web.unc.edu/experiments/. I am a student at UNC who will be graduating in May 2022. I am working with Dr. Gruszko to develop the code and electronics to control the calibration system for the NuDot experiment. The goal of this experiment is to detect neutrinoless double beta decay. Neutrinoless double beta decay is a very rare phenomenon. Because of this, it is difficult to distinguish signal from background during detection. NuDots goal is to reduce the background by detecting cherenkov radiation from single electron events produced by background events as opposed to the double electrons given off by double beta decay. 
 
The goal of my code and electronics is to move a point beta ray source to an exact height, inclination, and rotation. Knowing these allows NuDot to calibrate the precise timings given by the detectors. These timings are extremely important for event building, where we determine details about the event causing the signal such as the position and energy. 

## My Approach and Method
Having previously taken a class full dedicated to working with microcontrollers, my first thought for this project was to use a Raspberry Pi. I ruled out Arduinos because I needed a file system to save multiple files and wanted the flexibility of a microcontroller with an OS for testing purposes. The problem ultimately boils down to moving 3 stepper motors into position, verifying the accuracy of that position, and recording that position for and future movements of the stepper. 
 
I achieved these objectives by using python code to control the stepper motors and a c++ program to read the data from the stepper encoders, interpret the data, and store the position in a file. The python code will only move the stepper and the c++ code will only determine its position. This allows me to independently verify the positions of the steppers and compensate for any step skipping that might occur. This ensures that we always accurately know the positions of the steppers which is important for both calibration and mechanical reasons. Obviously we need to accurately know the position of the beta source to calibrate the system, but there are also a few mechanical hard stops that the steppers would be unable to push past (blocked by a lot of metal). I could have used a sensor to determine the position in space but decided to make my code very robust to avoid the issue all together. 


#### Code Structure
I decided on an object oriented approach for ease of use and abstraction. The [Calibrator](https://github.com/badnat/NuDotCalibrationSystem/blob/main/calibrator.py) object is primarily for abstraction and handling error handling/edge cases. It holds all of the [Stepper](https://github.com/badnat/NuDotCalibrationSystem/blob/main/stepper.py) objects which send the signals to the stepper motors to move them. The [Stepper](https://github.com/badnat/NuDotCalibrationSystem/blob/main/stepper.py) objects also use bash commands to start up the [encoder](https://github.com/badnat/NuDotCalibrationSystem/blob/main/encoder.cpp) code for that stepper motor. 

## Assembled Calibration System
![Image](https://github.com/badnat/NuDotCalibrationSystem/blob/main/Calibration_installed.png)

## Challenges and Future Improvements
- Fully implementation of code and handling a few more edge cases (almost finished)
- Implement code for the Daq system to control the Rpi remotely using ssh keys
- Finalize Electronics using a custom PCB and CAT6 cable to send signals to the steppers and to the Pi from the encoders
