# Viết chương trình bấm BT1 thì hiện cửa số hiện stream camera, 1 cửa sổ khác lọc hết các đối
# tượng khác, chỉ giữ lại vật có màu xanh và đỏ; Bấm BT2 thì vẽ đường bao màu đỏ lên đối
# tượng màu đỏ, đườngbao màu xanh lên đối tượng màu xanh
import cv2
import copy
import RPi.GPIO as GPIO 
def main():
    BT1 = 21
    BT2 = 26
    cap = cv2.VideoCapture(0) 
    print("capture is ok")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down =GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down =GPIO.PUD_UP)
    isdraw =False
    while True:
        if GPIO.input(BT1) ==GPIO.LOW:
            print("Press BT1")
            while True:
                ret, src = cap.read()
                frame =copy.copy(src)
                hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                green_mask= cv2.inRange(hsv,(35, 89, 107),(45, 241, 213))
                _,contoursGreen,_ =cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                red_mask= cv2.inRange(hsv,(0, 118, 130),(5, 255, 255))
                _,contoursRed, _= cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                # Họp xanh và đồ lại# Nhóm mask xanh và đồ lại bằng phép cộng mà trận
                group = green_mask + red_mask
                # Các phân tử trong ma trận(Lớn x 1 là True và ngược lại)
                group = group >= 1
                # Từ kiểu bài chuyển sang kiểu uint8, nhân với 255 để maskgroup có màu trắng
                # TỪ Kiểu bool chuyển sang kiểu uintô, nhân với 255 để maskgroup có màu trắng 
                group = group.astype('uint8')* 255
                result = cv2.bitwise_or(frame, frame, mask=group)
                #---BT2----
                if GPIO.input(BT2) ==GPIO.LOW:
                    isdraw=True
                if isdraw:
                    draw(contoursRed, contoursGreen, result)
                cv2.imshow("Threshold", result) 
                cv2.imshow('Camera', src)
                # Press q to exit
                if cv2.waitKey(1) & 0xFF== ord('q'):
                    GPIO.cleanup()
                    cv2.destroyAllWindows()
                    break
def nothing(x):
    pass
def draw(contoursRed, contoursGreen, frame) :
    for i in range(len(contoursRed)) :
        if cv2.contourArea(contoursRed[i]) > 300:
            hull =cv2.convexHull(contoursRed[i]) 
            cv2.drawContours(frame, [hull], -1,(0, 0, 255))
    for i in range(len(contoursGreen)):
        if cv2.contourArea(contoursGreen [i]) > 300:
            hull= cv2.convexHull(contoursGreen [i])
            cv2.drawContours(frame, [hull], -1,(0, 255, 0))
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyAllWindows()
