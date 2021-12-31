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

direction = "L"
if sys.argv:
    direction = sys.argv[1]

durationFwd = 2000 # This is the duration of the motor spinning. used for forward direction
durationBwd = 2000 # This is the duration of the motor spinning. used for reverse direction
delay = 0.2 # This is actualy a delay between PUL pulses - effectively sets the motor rotation speed.
#
cycles = 1000 # This is the number of cycles to be run once program is started.
#

def setup():
    GPIO.setmode(GPIO.BCM)
    # GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
    #
    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)

def rotate():
    GPIO.output(ENA, GPIO.HIGH)
    if direction == 'R':
        GPIO.output(DIR, GPIO.HIGH)   # RIGHT
    elif direction == 'L':
        GPIO.output(DIR, GPIO.LOW)   # LEFT
    elif direction == 'D+':
        GPIO.output(DIR, GPIO.LOW)
        return
    elif direction == 'D-':
        GPIO.output(DIR, GPIO.HIGH)
        return
    elif direction == 'E+':
        GPIO.output(ENA, GPIO.LOW)
        return
    elif direction == 'E-':
        GPIO.output(ENA, GPIO.HIGH)
        return
    elif direction == 'P+':
        GPIO.output(PUL, GPIO.LOW)
        return
    elif direction == 'P-':
        GPIO.output(PUL, GPIO.HIGH)
        return

    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
    # sleep(.1) # pause for possible change direction
    return

try:
    setup()
    rotate()
    while True:
        n = 0

finally:
    GPIO.output(ENA, GPIO.LOW)
*
print('Cycling Completed')
#
