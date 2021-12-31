from time import sleep
import RPi.GPIO as GPIO
#
PUL = 17  # 
DIR = 27  # 
ENA = 22  # 
# mode/dir /home 
MODE = 2
MANUAL_DIR = 3
HOME_DETECT = 4

def initIO():
    print('IO Initialization Start')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(MODE, GPIO.IN)
    GPIO.setup(MANUAL_DIR, GPIO.IN)
    GPIO.setup(HOME_DETECT, GPIO.IN)

    print('IO Initialization Complete')
#
#
def cleanupIO(): 
    print('IO Cleanup started')
    GPIO.cleanup() # run this just to make sure 
#
#

def ismanualmode():
    ismanual = GPIO.input(MODE)
    return not ismanual
#
#
def ishome():  # normally 1  means  that 0 = is home. 
    ishome = GPIO.input(HOME_DETECT)
    return not ishome
#
#
def manualpositionleft():
    posleft = GPIO.input(MANUAL_DIR)
    return not posleft
#    

def gohome():
    GPIO.output(ENA, GPIO.LOW)

    GPIO.output(DIR, GPIO.HIGH)
  
    for y in range(5000):
        GPIO.output(PUL, GPIO.HIGH)
        GPIO.output(PUL, GPIO.LOW)
        sleep(.001)
        if ishome():
            break
   
    GPIO.output(ENA, GPIO.HIGH)
#
#
def takesteps(stepcount, direction):
   
    sleep(.1) # pause due to a possible change direction
    GPIO.output(ENA, GPIO.LOW) # enable 


    if direction == 0:
        GPIO.output(DIR, GPIO.LOW)  # RIGHT 
    else: 
        GPIO.output(DIR, GPIO.HIGH)  # LEFT
  
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

    # GPIO.output(ENA, GPIO.LOW)  # disable
   # sleep(.5) # pause for possible change direction
    GPIO.output(ENA, GPIO.HIGH) # disable, free up the motor. 
    return   



def goFarRightPostion():
    takesteps(2200,0)