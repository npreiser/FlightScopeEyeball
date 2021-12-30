# Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=242928\.
#
# Software to drive 4 wire stepper motor using a TB6600 Driver
# PRi - RPi 3B
#
# Route 3.3 VDC to the controller "+" input for each: ENA, PUL, and DIR
#
# Connect GPIO pins as shown below) to the "-" input for each: ENA, PUL, and DIR
#
#
from time import sleep
import RPi.GPIO as GPIO
import sys, getopt
#
PUL = 17  # Stepper Drive Pulses
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
# DIRI = 14  # Status Indicator LED - Direction
# ENAI = 15  # Status indicator LED - Controller Enable
#
# NOTE: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.
# 

direction = sys.argv[1]

print('hello %d', direction)

GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
#
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
durationFwd = 2000 # This is the duration of the motor spinning. used for forward direction
durationBwd = 2000 # This is the duration of the motor spinning. used for reverse direction
delay = 0.0005 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
#
cycles = 1000 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
print('number of Cycles to Run set to ' + str(cycles))
#
def forward():
    GPIO.output(ENA, GPIO.HIGH)
    if direction == 'R':
        print("going right")
        GPIO.output(DIR, GPIO.HIGH)   # RIGHT
    else:
        print("going Left")
        GPIO.output(DIR, GPIO.LOW)   # LEFT

    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
       # sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    
    
    GPIO.output(ENA, GPIO.LOW)
    # sleep(.1) # pause for possible change direction
    return

forward()
GPIO.cleanup()
print('Cycling Completed')
#
