from utilis import *
import cv2

w,h = 360,240
pid = [0.5,0.5,0] #kp,kd,ki
myDrone = intializeTello()
pError = 0
startCounter = 0 #flight->0, no flight->1

while True:
      #flight
      if startCounter == 0:
             myDrone.takeoff()
             startCounter = 1
      ## STEP 1
      img = telloGetFrame(myDrone)
      ## STEP 2
      img, info = findFace(img) #info - x pos of closest image, area of image
      ## STEP 3
      pError = trackFace(myDrone, info, w, pid, pError) #for pid controller and sending velocity to tello

      # DISPLAY IMAGE
      cv2.imshow("MyResult", img)
      # WAIT FOR THE 'Q' BUTTON TO STOP
      if cv2.waitKey(1) and 0xFF == ord('q'):
              myDrone.land()
              break