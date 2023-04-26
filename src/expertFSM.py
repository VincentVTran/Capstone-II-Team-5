from pickle import TRUE

# INIT = 'INIT'
# TAKEOFF = 'TAKEOFF'
# LAND = 'LAND'
# IDLE = 'IDLE'
# MOVE_LEFT = 'MOVE_LEFT'
# MOVE_RIGHT = 'MOVE_RIGHT'
# MOVE_DOWN = 'MOVE_DOWN'
# MOVE_UP = 'MOVE_UP'
# MOVE_FORWARD = 'MOVE_FORWARD'
# MOVE_BACKWARD = 'MOVE_BACKWARD'
# X = 100
# PrevX = 0
# Y = 0
# PrevY = 0
# ROI = 0
# PrevROI = 0
# next_state = 1

next_state = 1

def INIT():
    #print("INIT STATE")
    global next_state
    next_state = 2 # move to TAKEOFF STATE
    command = ""
    return (0,0,0,0)

def TAKEOFF():
    #print("TAKEOFF_STATE")
    global next_state
    next_state = 4 # move to idle state
    command = "takeoff"
    return (0,0,0,0)
    

def LAND():
    #print("LAND_STATE")
    command = "land"
    return (0,0,0,0)
    
# To-Do: check buffer/thresholds (20 at the moment). Or replace with ABS value percentage comparisons
def IDLE():
    #print("IDLE_STATE")
    global next_state, X, Y, ROI
    if X < 0 - 200:
        next_state = 5 #MOVE_LEFT #5
    elif X > 0 + 200:
        next_state = 6 #MOVE_RIGHT #6
    elif ROI > 50000 and ROI != 0:
        next_state = 10 # MOVE_BACKWARD #10
    elif ROI < 30000 and ROI !=0:
        next_state = 9 #MOVE_FORWARD #9
    elif Y < 0 - 25:
        next_state = 8 #MOVE_UP #8
    elif Y > 0 + 25:
        next_state = 7 #MOVE_DOWN #7
    else:
        next_state = 4
        
	#elif(battery < battery_shutoff):
	#	next_state = FINAL
    command = ""
    return (0,0,0,0)

def MOVE_LEFT():
    print("MOVE_LEFT_STATE", "X:", X, "PrevX:", PrevX)
    global next_state
    next_state = 4
    command = "left 20"
    return (0,0,0,-40)
    

def MOVE_RIGHT():
    #print("MOVE_RIGHT_STATE")
    global next_state
    next_state = 4
    command = "right 20"
    return (0,0,0,40)
    

def MOVE_DOWN():
    #print("MOVE_DOWN_STATE")
    global next_state
    next_state = 4
    command = "down 20"
    return (0,0,-20,0)


def MOVE_UP():
    #print("MOVE_UP_STATE")
    global next_state
    next_state = 4
    command = "up 20"
    return (0,0,20,0)

def MOVE_FORWARD():
    #print("MOVE_FORWARD_STATE")
    global next_state
    next_state = 4
    command = "forward 20"
    return (0,40,0,0)

def MOVE_BACKWARD():
    #print("MOVE_BACKWARD_STATE")
    global next_state
    next_state = 4
    command = "back 20"
    return (0,-40,0,0)

states = {
    1: INIT, 
    2: TAKEOFF, 
    3: LAND, 
    4: IDLE, 
    5: MOVE_LEFT, 
    6: MOVE_RIGHT,
    7: MOVE_DOWN, 
    8: MOVE_UP, 
    9: MOVE_FORWARD, 
    10: MOVE_BACKWARD
    }

def FSM_TICK(update_X, update_Y, update_ROI): # Main FSM call
    global X, Y, ROI, PrevX, PrevY, PrevROI, next_state

    # Update FSM variables with AI variables
    X = update_X
    Y = update_Y
    ROI = update_ROI

    # Find command from FSM
    command = states.get(next_state)()

    # Store AI variables (after they've been used) for use in next FSM_TICK call
    PrevX = X
    PrevY = Y
    PrevROI = ROI

    # print ("PrevX: " + str(PrevX))
    # print ("PrevY: " + str(PrevY))
    # print ("PrevROI: " + str(PrevROI))

    return command 

