from bluestacks import BlueStacks
from time import sleep
import cv2

BR = cv2.imread("BR.jpg")
LT = cv2.imread("LT.jpg")
BLACK = cv2.imread("B.jpg")
WHITE = cv2.imread("W.jpg")

a = BlueStacks()
frame = a.Screenshot()
# match
BottomRight = a.Find(BR)
TopLeft = a.Find(LT)
# multi match 
black_mids = a.Multi_match(BLACK)
white_mids = a.Multi_match(WHITE)
# draw
cv2.circle(frame, BottomRight, 10, (0, 0, 255), -1)
cv2.circle(frame, TopLeft, 10, (0, 255, 0), -1)
go_w, go_h = BottomRight[0] - TopLeft[0], BottomRight[1] - TopLeft[1]
for j in range(TopLeft[1],BottomRight[1]+1,go_h//8):
    for i in range(TopLeft[0],BottomRight[0]+1,go_w//8):
        cv2.circle(frame,(i,j),5, (0, 0, 0), -1)

for i in black_mids:
    cv2.circle(frame,i,10, (0, 0, 0), -1)

for i in white_mids:
    cv2.circle(frame,i,10, (255, 255, 255), -1)
# show
a.Show_frame()
# click
for j in range(TopLeft[1],BottomRight[1]+1,go_h//8):
    for i in range(TopLeft[0],BottomRight[0]+1,go_w//8):
        a.Click((i,j))
        sleep(0.02)
a.Save_frame("demo")