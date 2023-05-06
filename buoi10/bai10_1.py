# Với bài tập này chúng ta phải cài thêm gói thư viện xử lý ảnh của opencv-python, các bạn
# download tại đây: https://github.com/diy-hus/opencv
# Sau khi giải nén ta có tên: opencv_python-3.4.13.47-cp37-cp37m-linux_armv7l.whl
# Dùng lệnh pip3 install opencv_python-3.4.13.47-cp37-cp37m-linux_armv7l.whl để cài đặt.
# Nếu vẫn tiếp tục báo lỗi các bạn gõ dòng lệnh sudo apt-get install libatlas-base-dev trước rồi tiếp
# tục cài lại sau.
# CHÚ Ý: Sau buổi học các bạn phải xóa hết những gì các bạn đã download về và sử dụng dòng
# lệnh pip3 uninstall opencv_python-3.4.13.47-cp37-cp37m-linux_armv7l.whl để gỡ gói thư
# viện đã cài đặt (là một trong những yêu cầu lúc đi thi cuối kỳ) 


# Viết chương trình bấm BT1 chụp 1 ảnh từ camera và hiện ảnh lên màn hình
import cv2
import RPi.GPIO as GPIO 
import time
def main():
    BT1 = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO. IN, pull_up_down =GPIO.PUD_UP) 
    global namewindow
    namewindow = "Camera User"
    capture = cv2.VideoCapture(0) # khởi động camera 
    print("Capture đã ok")
    while True: # nếu camera được mở
        ret, frame = capture.read() # đọc video từ camera
    # frame được trả về là dạng ma trận; numpy.aray print(type(frame)) 
    # chiều dài và chiều rộng là cỡ của ma trận; print(frame.shape) 
        if GPIO.input(BT1) == GPIO.LOW:
            while True:
            # Hiện ảnh ra màm hình từ biến frame
            # cv2.imshow sẽ đọc frame, chuyển frame ra dạng hình ảnh 
                cv2.imshow("Ảnh chụp camera", frame) 
                cv2.waitKey()
                cv2.destroyWindow("Ảnh chụp camera")
                break
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyWindow(namewindow)

