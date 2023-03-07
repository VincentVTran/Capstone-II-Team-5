# import the necessary packages
import numpy as np
import cv2
 
# initialize the cv descriptor/person detector
upperbody_cascade = cv2.CascadeClassifier('./src/cascades/haarcascade_upperbody.xml')
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
center_x = int(SCREEN_WIDTH/2)
center_y = int(SCREEN_HEIGHT/2)

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)
# the output will be written to output.avi
out = cv2.VideoWriter(
    'webcam_test.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (SCREEN_WIDTH,SCREEN_HEIGHT))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Draw circle at center of the frame
    cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0))

    # Convert frame to grayscale in order to apply the haar cascade for upperbody identification
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    upperbodies = upperbody_cascade.detectMultiScale(gray, 1.3, minNeighbors=5)

    # If an upperbody is recognized, add to list of upperbodies and draw indicators to frame around upperbody
    upperbody_center_x = center_x
    upperbody_center_y = center_y
    z_area = 0
    z_area = 0
    for upperbody in upperbodies:
        (x, y, w, h) = upperbody
        cv2.rectangle(frame,(x, y),(x + w, y + h),(255, 255, 0), 2)

        upperbody_center_x = x + int(h/2)
        upperbody_center_y = y + int(w/2)
        z_area = w * h
        cv2.circle(frame, (upperbody_center_x, upperbody_center_y), 10, (0, 0, 255))
    # Calculate recognized upperbody offset from center
    offset_x = upperbody_center_x - center_x
    offset_y = upperbody_center_y - center_y

    cv2.putText(frame, f'[{offset_x}, {offset_y}, {z_area}]', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    
    # Write the output video 
    out.write(frame.astype('uint8'))
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)