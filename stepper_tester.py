from stepper import gohome,takesteps,ismanualmode,manualpositionleft,initIO,cleanupIO,goFarRightPostion


initIO()


current_tray_position = 0
modeswitch_debounce = 0
positionswitch_debounce = 0

gohome()

MANUAL_MODE = ismanualmode()
POSITION_LEFT = manualpositionleft()
print("Manual Mode: %s" % MANUAL_MODE)
print("MM Position Left: %s" % POSITION_LEFT)

# switch to manul should go home... !!!


while True:
    # check for mode switch (manual vs auto) 
    if modeswitch_debounce > 0:
        modeswitch_debounce-=1

    temp = ismanualmode()  # check if we are in manual mode 
    if temp != MANUAL_MODE and modeswitch_debounce <= 0: # if its changed... 
        modeswitch_debounce = 1000
        MANUAL_MODE = temp
        modename = "Manual"
        if MANUAL_MODE == False:
            modename = "Auto"
        else:
            gohome()

        print("manual/auto  switched to:  %s " % modename)

    # check for manual postion change 
    if MANUAL_MODE == True and modeswitch_debounce <= 0: # if in manual and past debounce.. 

        if positionswitch_debounce > 0:
            positionswitch_debounce-=1

        temppos = manualpositionleft()
        if temppos != POSITION_LEFT and positionswitch_debounce <= 0:
            positionswitch_debounce = 1000
            POSITION_LEFT = temppos
            if POSITION_LEFT == True:
                gohome()
                print("Moved manual left position")
            else:
                goFarRightPostion()
                print("Moved manual right position")




# takesteps(500,0)
# gohome()  # go left until home 
# mm = ismanualmode()
# bog = ismanualmode()
# print(bog)