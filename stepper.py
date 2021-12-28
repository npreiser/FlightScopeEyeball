# Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=242928\.
#
from time import sleep
import RPi.GPIO as GPIO
# input pins (for mode / position. )
MANUAL_AUTO_PIN = 2
MANUAL_POSITION_PIN = 3
#
PUL = 17  # Stepper Drive Pulses
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

delay = .0000001 #.1us 

def initIO():
    print('IO Initialization Start')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(MANUAL_AUTO_PIN, GPIO.IN)
    GPIO.setup(MANUAL_POSITION_PIN, GPIO.IN)
    print('IO Initialization Complete')
#
#
def cleanupIO():
    print('IO Cleanup started')
    GPIO.cleanup() # run this just to make sure 
#
#
def ismanualmode():
    ismanual = GPIO.input(MANUAL_AUTO_PIN)
    return ismanual
#
#
def manualpositionleft():
    posleft = GPIO.input(MANUAL_POSITION_PIN)
    return posleft
#    
#    
def stepforward(stepcount):
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
   # print('ENA set to HIGH - Controller Enabled')
    #
    sleep(.1) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.LOW)
    # GPIO.output(DIRI, GPIO.LOW)
   # print('DIR set to LOW - Moving Forward at ' + str(delay))
   # print('Controller PUL being driven.')
    for x in range(stepcount): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
   # print('ENA set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return   
#
#
def stepreverse(stepcount):
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
   # print('ENA set to HIGH - Controller Enabled')
    #
    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)
    # GPIO.output(DIRI, GPIO.HIGH)
   # print('DIR set to HIGH - Moving Backward at ' + str(delay))
   # print('Controller PUL being driven.')
    #
    for y in range(stepcount):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    #print('ENA set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return