import random

import cv2, cvzone, time
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 470)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # ai vs player



while True:

    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # find hands
    hands, img = detector.findHands(imgScaled)  # with draw

    if startGame:

        if stateResult == False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 475), cv2.FONT_HERSHEY_PLAIN, 6, (255, 8, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 8

                if hands:
                    # if hand is detected
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # find how many fingers are up
                    print(fingers)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1

                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2

                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f"Resources/1.png", cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # player wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

    imgBG[233:653, 795:1195] = imgScaled

    if stateResult:
        imgAI = cv2.imread(f"Resources/1.png", cv2.IMREAD_UNCHANGED)
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(int(scores[0])), (410, 215), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 10)
    cv2.putText(imgBG, str(int(scores[1])), (1112, 225), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 10)

    # cv2.imshow("Image", img)
    cv2.imshow("Rock Paper Scissor", imgBG)
    # cv2.imshow("Scaled", imgScaled)

    key = cv2.waitKey(1)
    if key == ord("s"):
        startGame = True
        initialTime = time.time()
        stateResult = False

    if key == ord("q"):
        quit()


