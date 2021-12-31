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
#
PUL = 17  # Stepper Drive Pulses
DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
#
# NOTE: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.
# 
GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
#
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

print('Initialization Completed')
#
# Could have usesd only one DURATION constant but chose two. This gives play options.
durationFwd = 2000 # This is the duration of the motor spinning. used for forward direction
durationBwd = 2000 # This is the duration of the motor spinning. used for reverse direction
#
delay = 0.00031 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
#
cycles = 1  # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
#
#
def takesteps(stepcount, direction):
    GPIO.output(ENA, GPIO.HIGH)
    sleep(.1) # pause due to a possible change direction
    if direction == 0:
        GPIO.output(DIR, GPIO.LOW)  # LEFT 
    else: 
        GPIO.output(DIR, GPIO.HIGH)  # Right (forward)
  
  # PARAMS for acceleration /decel..

    ACC_DCC_WINDOW_STEPS = 500 # how big of a window to accel or decel over .. 
    ACC_DCC_RATE = .000001 # rate at which to inc/dec the delay... 

    accend = ACC_DCC_WINDOW_STEPS
    dccstart = stepcount-ACC_DCC_WINDOW_STEPS  # decel starts at end-500 steps

    mydelay = .001  # starting delay.. it will inc/dec from here... 

    # accel range
    printmax = False
    for x in range(stepcount): 
        GPIO.output(PUL, GPIO.HIGH)
        # sleep(mydelay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(mydelay)
        
        if x < accend:
            #if x % 10 == 0:  # evey 10 steps  
            mydelay -= ACC_DCC_RATE # reduce delay down.. 
                # print("delay %s" % mydelay)
        elif x > dccstart:
            #if x % 10 == 0:
            mydelay += ACC_DCC_RATE  #  ramp delay up = slow it down... 
                # print("delay %s" % mydelay)
        else:
            if printmax == False:
                printmax = True
                print("max speed delay:  %5f" % mydelay)

    GPIO.output(ENA, GPIO.LOW)  # disable
   # sleep(.5) # pause for possible change direction
    return   

#
#
def forward():
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    print('ENA set to HIGH - Controller Enabled')
    #
    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)
    # GPIO.output(DIRI, GPIO.LOW)
    print('DIR set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL being driven.')
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    print('ENA set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return
#
#
def reverse():
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    print('ENA set to HIGH - Controller Enabled')
    #
    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.LOW)
    # GPIO.output(DIRI, GPIO.HIGH)
    print('DIR set to HIGH - Moving Backward at ' + str(delay))
    print('Controller PUL being driven.')
    #
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    print('ENA set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return

while cyclecount < cycles:
    takesteps(2500,1)  # 1 forward (right)

    print("Long wait: ")
    sleep(1.5)
   
    takesteps(2500,0)
   #  forward()
   #  reverse()
    cyclecount = (cyclecount + 1)
    print('Number of cycles completed: ' + str(cyclecount))
    print('Number of cycles remaining: ' + str(cycles - cyclecount))
#



GPIO.cleanup()
print('Cycling Completed')
#
