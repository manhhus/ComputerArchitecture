# Viết chương trình điều khiển tốc độ động cơ DC bằng nút bấm. Mỗi lần bấm BT1 tốc độ
# động cơ tăng thêm 20%, bấm BT2 giảm 20% và quay theo chiều kim đồng hồ. Bấm BT3
# tốc độ động cơ tăng 20%, bấm BT4 giảm 20% và ngược chiều kim đồng hồ. Hiển thị tốc
# độ (tương đối theo %) lên terminal mỗi lần bấm
import RPi.GPIO as GPIO 
import time 
def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20
    BT4 = 19
    DIR = 25
    PWD = 24
    GPIO.setmode(GPIO.BCM)
    # khởi tạo và pull up các bút bấm
    GPIO.setup(BT1, GPIO.IN, pull_up_down= GPIO.PUD_UP) 
    GPIO.setup(BT2, GPIO.IN, pull_up_down= GPIO.PUD_UP) 
    GPIO.setup(BT3, GPIO.IN, pull_up_down= GPIO.PUD_UP) 
    GPIO.setup(BT4, GPIO.IN, pull_up_down= GPIO.PUD_UP) # KHởi tạo động cơ DC
    GPIO.setup(DIR, GPIO.OUT) 
    GPIO.setup(PWD, GPIO.OUT)
    global PWD1, PWD2 # khởi tạo các biến global 
    PWD1 = GPIO.PWM(DIR, 100) # tần số 100Hz 
    PWD2 = GPIO.PWM(PWD, 100) # tần số 100Hz 
    PWD1.start(0) # khởi động
    PWD2.start(0)
    # Khởi động
    currentPWD1 = 20 # tốc độ hiện tại của PWD1 
    currentPWD2 = 20 # tốc độ hiện tại của PWD2 
    print("Chuẩn bị hoàn tất ok")
    while True:
        # Tăng tốc và chạy theo chiều kim đồng hồ 
        if GPIO.input(BT1) == 0:
            print("Press BT1")
            if currentPWD2 != 0:
                PWD2.ChangeDutyCycle(0) 
                time.sleep(1)
            upPWD = int(0.2*currentPWD1)
            currentPWD1 =(currentPWD1 + upPWD) if currentPWD1+upPWD < 100 else 100     
            if currentPWD1 == 0:
                currentPWD1 = 20
            # thay đổi tốc độ theo biến currentPWD1
            PWD1.ChangeDutyCycle(currentPWD1)
            print("Tốc độ hiện tại: " + str(currentPWD1)+ " theo chiều thuận")
            currentPWD2 = 0
            time.sleep(0.5)
        # Giảm tốc và chạy theo chiều kim đồng hồ
        if GPIO.input(BT2) == 0:
            print("Press BT2")
            PWD2.ChangeDutyCycle(0)
            downPWD = int(0.2*currentPWD1)
            currentPWD1 =(currentPWD1 - downPWD) if currentPWD1 - downPWD > 0 else 0 
            PWD1.ChangeDutyCycle(currentPWD1)
            print("Tốc độ hiện tại: " + str(currentPWD1)+ " theo chiều thuận")
            currentPWD2 = 0
            time.sleep(0.5)
        # Tăng tốc và chạy theo ngược kim đồng hồ
        if GPIO. input(BT3) == 0:
            print("Press BT3")
            if currentPWD1 != 0:
                PWD1.ChangeDutyCycle(0)
                time.sleep(1)
            upPWD = int(20/100 *currentPWD2)
            currentPWD2 =(currentPWD2+ upPWD) if currentPWD2+ upPWD < 100 else 100 
            if currentPWD2 == 0:
                currentPWD2 = 20
            # thay đổi tốc độ theo biến currentPWD2
            PWD2.ChangeDutyCycle(currentPWD2)
            print("Tốc độ hiện tại: " + '-' + str(currentPWD2)+ " theo chiều ngược")
            currentPWD1 = 0
            time.sleep(0.5)
        # Giảm tốc và chạy ngược chiều kim đồng hổ
        if GPIO. input(BT4) == 0:
            print("Press BT4")
            PWD1.ChangeDutyCycle(0)
            downPWD=int(20/100*currentPWD2)
            currentPWD2 =(currentPWD2 - downPWD) if currentPWD2 - downPWD > 0 else 0
            print("Tốc độ hiện tại: " + '-' + str(currentPWD2)+ " theo chiều ngược")
            PWD2.ChangeDutyCycle(currentPWD2)
            currentPWD1 = 0
            time.sleep(0.5)

try:
    main()
except KeyboardInterrupt:
    PWD1.stop()
    PWD2.stop()
    GPIO.cleanup()   