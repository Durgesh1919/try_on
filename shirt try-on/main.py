

#imports
import os
# from turtle import width
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector

#initializtions
cap = cv2.VideoCapture(0)
detector = PoseDetector()

# set the width and the height of the window
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

shirtFolderPath = "./resources/Shirts"
listShirts = os.listdir(shirtFolderPath)

#width of shirt divided by width of points 11 & 12
fixedRatio = 262/190 
shirtRatioHeightWidth = 581/440

#index of the images
imageNumber = 0

# importing the buttons
imgButtonRight = cv2.imread("./resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight,1)

# Button Press Counters
counterRight = 0;
counterLeft = 0;

# selection Animation Speed
selectionSpeed = 10
#main loop
while True:
   #getting the image from the web cam
   success, img = cap.read()
   #Getting the pose from the image
   img = detector.findPose(img)
   #Flipping the image
#    img = cv2.flip(img.1)
   #Getting the landmark and bounding box info
   lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False,draw=False)
   #if you find something then
   if lmList:
        #getting the coordinates for the position of the shirt
        lm11 = lmList[11][1:3]
        lm12 = lmList[12][1:3]
        #importing the image of the shirt
        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)

        widthOfShirt = int((lm11[0]-lm12[0])*fixedRatio)
        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shirtRatioHeightWidth)))
        currentScale = (lm11[0]-lm12[0])/190
        offset = int(44*currentScale),int(48*currentScale)
        try:
            img = cvzone.overlayPNG(img, imgShirt,(lm12[0]-offset[0],lm12[1]-offset[1]))
        except:
            pass
        
        # Displaying the Buttons
        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][1] < 300:
            counterRight += 1;
            cv2.ellipse(img,(139,360),(66,66),0,0,counterRight*selectionSpeed,(0,255,0),20)

            if counterRight*selectionSpeed > 360:
                counterRight=0
                if imageNumber < len(listShirts)-1:
                    imageNumber += 1
        elif lmList[15][1] > 1000:
            counterLeft += 1;
            cv2.ellipse(img,(1138,360),(66,66),0,0,counterLeft*selectionSpeed,(0,255,0),20)

            if counterLeft*selectionSpeed > 360:
                counterLeft=0
                if imageNumber > 0:
                    imageNumber -= 1
        else:
            counterRight = 0
            counterLeft = 0
   #Displaying the image from the web cam
   cv2.imshow("Image",img)
   if cv2.waitKey(1) == ord('x'):
       break 