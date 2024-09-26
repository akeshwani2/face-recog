# 1. Import packages
import cv2 # OpenCV camera
import numpy as np # Numpy array
import sqlite3 # Database

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml'); # To detect faces in the camera
cam=cv2.VideoCapture(0) # 0 is the webcam number, (0) is default

def insertorupdate(ID, NAME, AGE): # Function for sqlite database
    conn=sqlite3.connect("sqlite.db") # 'conn' is the connection variable, this line also denotes that we are usong sqlite3 to connect our database
    cmd="SELECT * FROM STUDENTS WHERE ID="+str(ID) # We select particular details about the student based on their user defined ID
    cursor=conn.execute(cmd) # Cursor to execute statement
    recordExist=0 # Assume there are no records in our table
    for row in cursor: # Checking each line if any records exist. If exists, it's considered as 1, else 0
        recordExist=1
    if(recordExist==1): # If there is a record, we update name and age
        conn.execute("UPDATE STUDENTS SET NAME=? WHERE ID=?", (NAME, ID)) # Corrected parameter passing
        conn.execute("UPDATE STUDENTS SET AGE=? WHERE ID=?", (AGE, ID)) # Corrected parameter passing
    else: # If the record doesn't exist, we insert the values
        conn.execute("INSERT INTO STUDENTS (ID, NAME, AGE) values(?, ?, ?)", (ID, NAME, AGE))

    conn.commit() # Commit the connection
    conn.close() # Close the connection

# 2. Insert user defined values into table
ID=input("Enter user ID: ")
NAME=input("Enter user name: ")
AGE=input("Enter user age: ")

insertorupdate(ID, NAME, AGE) # Inserts user defined values

# 3. Face detection through camera
sampleNum=0; # This assumes that there are no samples in the dataset
while(True):
    ret, img = cam.read() # This opens camera and reads the images in the camera
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Corrected the usage of cv2
    faces=faceDetect.detectMultiScale(gray, 1.3, 5) # 'gray' is the input image in grayscale, '1.3' is the scale factor (specifies how much the image size is reduced at each image scale/step), '5' is the minNeighbors parameter (specifies how many neigbors each candidate rectangle should have to return it. The higher the value, the fewer the detections but the better the quality)
    for(x, y, w, h) in faces: # width and height
        sampleNum += 1 # If face detected, sample number += 1
        # This is when I created the 'dataset' folder, if faces get detected, that's where it stores them
        cv2.imwrite("dataset/"+str(NAME)+"-"+str(ID)+"-"+str(sampleNum)+".jpg",gray[y:y+h,x:x+w]) # This specifies the format in which the faces will be stored
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) # If faces get detected in camera, we draw a rectangle around the face to show that it has been detected
        cv2.waitKey(100) # Delay time 100 seconds
    cv2.imshow("Face", img) # Show faces detected in camera
    cv2.waitKey(1)
    if (sampleNum>20): # If dataset created is more than 20, we break the loop. '20' can be manipulated to the amount of datasets desired
        break

cam.release()
cv2.destroyAllWindows() # Closing windows