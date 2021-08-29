

# First we will create a utilities file in which we will add all the functions. Then we will import all the tello and the cv2 packages.

from djitellopy import Tello 
import cv2
#Then we will create the tello intitialization function that will setup the tello drone for flight and send commands. We will set all the dspeed to 0. We have 4 types of dspeeds

'''Forward Backwards
Left Right
Up Down
Yaw (rotation)'''
def intializeTello():
# CONNECT TO TELLO
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.dspeed =0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone
#Now we will call this function in the main script.



myDrone = intializeTello()
#Get Frame from Drone
#Once we have setup the tello drone we will get the frame/image from it. We will create a simple function for this, that will take the drone object as the input argument and return the current image.

def telloGetFrame(myDrone,w=360,h=240):
# GET THE IMGAE FROM TELLO
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img
#Now we will call this function inside a while loop.

while True:
## STEP 1
    img = telloGetFrame(myDrone)
# DISPLAY IMAGE
    cv2.imshow("MyResult", img)
# WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) and 0xFF == ord('q'):
# replace the 'and' with '&amp;' 
        myDrone.land()
    break


#Once we get the frames form the drone, then its time to find the faces in our image. We will create a function for this in the utilities file. We will be using the viola jones method to find the faces, so we have first get the haarcascade xml file. This will be added in the main directory. Now we can load this file and detect the faces.

def findFace(img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
#Now that we have the faces we will find their coordinates and display it on the image.

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#Once we have all the faces we will target one of them and use its coordinates to operate the drone. We will first create empty lists in which we will add the Center points of the detected faces and their areas.

    myFacesListC = []
    myFaceListArea = []
#Then we will find the center point and the area of each face and add this to our list

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = x + w//2
        cy = y + h//2
        area = w*h
        myFacesListC.append([cx,cy])
        myFaceListArea.append(area)
#Once we have all the faces we will find the closest one and return its coordinates. If no faces are found we will return 0.

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
# index of closest face
        return img,[myFacesListC[i],myFaceListArea[i]]
    else:
        return img, [[0,0],0]
#Lastly we will call this function in the main script

## STEP 2
img, c = findFace(img)


#To track the face we will create a function that will use the information of the face and try to follow it. We could simply assgin a value of dspeed but instead we will be using varying dspeed based on how far the face is. This can be achieved using PID controller. We will only use the Propotional and Derivative part of the controller.

# PID Controller
def trackFace(myDrone,c,w,pid,pError):
    print(c)
    speed= int(pid[0]*error + pid[1] * (error-pError))
    if c[0][0] != 0:
            myDrone.yaw_velocity = speed
    else:
        myDrone.left_right_velocity = 0
        myDrone.for_back_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0

    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,myDrone.for_back_velocity,
        myDrone.up_down_velocity, myDrone.yaw_velocity)

    return error
## PIDerror = c[0][0] - w//2   
# Current Value - Target Value
    
'''Sending Rotation to Drone
Once we have the speed value we can send it to the drone. But before we do that we will just make sure that the face is detected.'''

        
# SEND VELOCITY VALUES TO TELLO
        
#Now we will return the error since we will need it for the calculation of the Derivative part of the PID controller in the next frame.

     
#Lastly we will call this function in the main script.

## STEP 3
pError = trackFace(myDrone,c,w,pid,pError)
