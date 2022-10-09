from djitellopy import Tello
import cv2
import numpy as np
'''Forward Backwards, Left Right, Up Down, Yaw (rotation)'''
# CONNECT TO TELLO
def intializeTello():
       myDrone = Tello()
       myDrone.connect()
       myDrone.for_back_velocity = 0
       myDrone.left_right_velocity = 0
       myDrone.up_down_velocity = 0
       myDrone.yaw_velocity = 0
       myDrone.speed =0
       print(myDrone.get_battery())
       myDrone.streamoff()
       myDrone.streamon()
       return myDrone

# GET THE IMAGE FROM TELLO
def telloGetFrame(myDrone,w=360,h=240):
       myFrame = myDrone.get_frame_read()
       myFrame = myFrame.frame
       img = cv2.resize(myFrame, (w, h))
       return img

#find the faces in our image using the viola jones method
def findFace(img):
      faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
      imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #gray image to reduce processing
      faces = faceCascade.detectMultiScale(imgGray, 1.1, 4) #skinfactor, minimum neighbours

      #creating a list to store faces and areas to find closest face
      myFacesListC = [] #co-ordiantes
      myFaceListArea = []

      #fetching coordinates of faces
      for (x, y, w, h) in faces:
             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2) #image, starting pos, ending pos, RGB, width

             #find the center point and the area of each face
             cx = x + w // 2
             cy = y + h // 2
             area = w * h
             myFacesListC.append([cx, cy])
             myFaceListArea.append(area)

             if len(myFaceListArea) != 0:
                    # index of closest face (largest area)
                    i = myFaceListArea.index(max(myFaceListArea))
                    return img, [myFacesListC[i], myFaceListArea[i]] #returning closest face
             else:
                    return img, [[0, 0], 0] #if no face found


#track face using pid controller for smooth transitions
def trackFace(myDrone,info,w,pid,pError):

      #PID
      error = info[0][0] - w//2   #(where we are - actual value)
      speed = int(pid[0]*error + pid[1] * (error-pError))
      speed = int(np.clip(speed,-100,100)) #fixing speed range

      #detecting face
      if info[0][0] != 0: #face exists
             myDrone.yaw_velocity = speed
      # no face detected
      else:
             myDrone.left_right_velocity = 0
             myDrone.for_back_velocity = 0
             myDrone.up_down_velocity = 0
             myDrone.yaw_velocity = 0
             error = 0

      # SEND VELOCITY VALUES TO TELLO
      if myDrone.send_rc_control:
             myDrone.send_rc_control(myDrone.left_right_velocity, myDrone.for_back_velocity, myDrone.up_down_velocity, myDrone.yaw_velocity)

      return error

