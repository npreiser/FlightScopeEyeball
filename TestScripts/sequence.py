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
import sys, re
#
PUL = 17  # Stepper Drive Pulses
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
# DIRI = 14  # Status Indicator LED - Direction
# ENAI = 15  # Status indicator LED - Controller Enable
#
# NOTE: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.
# 

durationFwd = 2000 # This is the duration of the motor spinning. used for forward direction
delay = 0.002 # This is actualy a delay between PUL pulses - effectively sets the motor rotation speed.
pulsedelay = 0.002
#
cycles = 1000 # This is the number of cycles to be run once program is started.
#

delPattern = re.compile("d(.*)")
pulPattern = re.compile("p(.*)")

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)

def docmd(cmd):
    global delay
    global pulsedelay
 
    if cmd == 'D+':
        print("Set DIR +")
        GPIO.output(DIR, GPIO.HIGH)
        return
    elif cmd == 'D-':
        print("Set DIR -")
        GPIO.output(DIR, GPIO.LOW)
        return
    elif cmd == 'E+':
        print("Set ENA +")
        GPIO.output(ENA, GPIO.HIGH)
        return
    elif cmd == 'E-':
        print("Set ENA -")
        GPIO.output(ENA, GPIO.LOW)
        return
    elif cmd == 'P+':
        print("Set PUL +")
        GPIO.output(PUL, GPIO.HIGH)
        return
    elif cmd == 'P-':
        print("Set PUL -")
        GPIO.output(PUL, GPIO.LOW)
        return
    elif cmd == 'P':
        print("Do Single Pulse")
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        return

    match = delPattern.match(cmd)
    if match:
        delay = float(match.group(1))
        print ("Set Delay:", delay)
        return

    match = pulPattern.match(cmd)
    if match:
        pulsedelay = float(match.group(1))
        print ("Set Pulse Length:", pulsedelay)
        return

    durationFwd = int(cmd)
    print("Do", durationFwd, "pulses")
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(pulsedelay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)

    return

setup()
inputArgs = sys.argv
for i in inputArgs[1:]:
    docmd(i)
