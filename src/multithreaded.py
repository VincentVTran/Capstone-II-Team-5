from djitellopy import Tello
import cv2 
import pygame
import numpy as np
import time
import expertFSM
import threading

# Speed of the drone

S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.

FPS = 120
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
upperbody_cascade = cv2.CascadeClassifier('./src/cascades/haarcascade_upperbody.xml')
# Calculate center of frame
center_x = int(SCREEN_WIDTH/2)
center_y = int(SCREEN_HEIGHT/2)


#function to take in list of upperbodies and remove all but the one with the largest area
def targetUpperbodies(Upperbodies):
    Upperbodies=list(Upperbodies)
    if len(Upperbodies) != 0:
        max=-1
        maxIndex=0
        for i,upperbody in enumerate(Upperbodies):
            (x,y,w,h) = upperbody
            if w*h > max:
                max=w*h
                maxIndex=i
        return [np.array(Upperbodies[maxIndex])]
    return np.array([])

class FrontEnd(object):
 
    def __init__(self):
        # Init pygame
        
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Automatic Drone Tracking")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        
        self.drone = Tello()

        # Drone velocities between -100~100
        
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def annotateImage(self):
        frame_read = self.drone.get_frame_read()
        should_stop = False
        flag = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    # else:
                    #     self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            # Upperbody Detection Begins
            self.screen.fill([0, 0, 0])
            #----------------------------
            self.frame = frame_read.frame
            self.frame = cv2.resize(self.frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Draw circle at center of the frame
            cv2.circle(self.frame, (center_x, center_y), 10, (0, 255, 0))

            # Convert frame to grayscale in order to apply the haar cascade for upperbody identification
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            upperbodies = upperbody_cascade.detectMultiScale(gray, 1.3, minNeighbors=5)

            # If a upperbody is recognized, add to list of upperbodies and draw indicators to frame around upperbody
            upperbody_center_x = center_x
            upperbody_center_y = center_y
            z_area = 0

            upperbodies=targetUpperbodies(upperbodies)

            for upperbody in upperbodies:
                (x, y, w, h) = upperbody
                cv2.rectangle(self.frame,(x, y),(x + w, y + h),(255, 255, 0), 2)

                upperbody_center_x = x + int(h/2)
                upperbody_center_y = y + int(w/2)
                z_area = w * h
                cv2.circle(self.frame, (upperbody_center_x, upperbody_center_y), 10, (0, 0, 255))

            # Calculate recognized upperbody offset from center
            offset_x = upperbody_center_x - center_x
            offset_y = upperbody_center_y - center_y

            '''
            CALL FSM, adjustment made at top of loop
            = (10,10,0,0)
            FSM_TICK(update_X, update_Y, update_ROI):
            '''
            #pygame.time.wait(1000)
            if(flag is False):
                velocities = expertFSM.FSM_TICK(offset_x, offset_y, z_area)
                if(velocities != (0,0,0,0)):
                    self.left_right_velocity, self.for_back_velocity, self.up_down_velocity, self.yaw_velocity = velocities
                    flag = True
            
            #print(response)

            cv2.putText(self.frame, f'[{offset_x}, {offset_y}, {z_area}]', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            text = "Battery: {}%".format(self.drone.get_battery())
            cv2.putText(self.frame, text, (5, 650 - 5),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            if (self.left_right_velocity < 0):
                cv2.putText(self.frame, "Drone Instruction: Go Left", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            elif (self.left_right_velocity > 0):
                cv2.putText(self.frame, "Drone Instruction: Go Right", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            elif (self.for_back_velocity < 0):
                cv2.putText(self.frame, "Drone Instruction: Go Backwards", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            elif (self.for_back_velocity > 0):
                cv2.putText(self.frame, "Drone Instruction: Go Forwards", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            elif (self.up_down_velocity < 0):
                cv2.putText(self.frame, "Drone Instruction: Descend", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            elif (self.up_down_velocity > 0):
                cv2.putText(self.frame, "Drone Instruction: Ascend", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            elif (self.yaw_velocity > 0):
                cv2.putText(self.frame, "Drone Instruction: Yaw Counter-Clockwise", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            elif (self.yaw_velocity < 0):
                cv2.putText(self.frame, "Drone Instruction: Yaw Clockwise", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            else:
                cv2.putText(self.frame, "Drone Instruction: Hover", (10, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = np.rot90(self.frame)
            self.frame = np.flipud(self.frame)

            self.frame = pygame.surfarray.make_surface(self.frame)
            self.screen.blit(self.frame, (0, 0))
            # Write the output video 
            pygame.display.update()

            time.sleep(1 / FPS)

    def updateMovement(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self.update()
                if(flag is True):
                    pygame.time.wait(250)
                
                self.left_right_velocity, self.for_back_velocity, self.up_down_velocity, self.yaw_velocity = (0,0,0,0)
                self.update()
                flag = False
    
    def run(self):
        cv2.startWindowThread()

        # the output will be written to output.avi
        out = cv2.VideoWriter(
            'drone_demo.avi',
            cv2.VideoWriter_fourcc(*'MJPG'),
            15.,
            (SCREEN_WIDTH,SCREEN_HEIGHT))

        self.drone.connect()
        self.drone.set_speed(self.speed)

        #Streaming refresh if was already on
        self.drone.streamoff()
        self.drone.streamon()
        t1 = threading.Thread(target=self.annotateImage, args=(self))
        t2 = threading.Thread(target=self.updateMovement, args=(self))
        t1.start()
        t2.start()
        # Call it always before finishing. To deallocate resources.
        out.write(self.frame.astype('uint8'))
        self.drone.end()    

    def keyup(self, key):
        if key == pygame.K_t:  # takeoff
            self.drone.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.drone.land()
            self.send_rc_control = False

    def update(self):
        if self.send_rc_control:
            self.drone.send_rc_control(self.left_right_velocity, self.for_back_velocity,self.up_down_velocity, self.yaw_velocity)
            #print("Sending Velocities", self.left_right_velocity, self.for_back_velocity,self.up_down_velocity, self.yaw_velocity)


def main():
    frontend = FrontEnd()
    frontend.run()


if __name__ == '__main__':
    main()