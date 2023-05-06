# Bấm BT1 servo quay góc 10, bấm BT2 quay góc 50, bấm BT3 quay góc 120

import RPi.GPIO as GPIO 
import time 
def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20
    GPIO.setmode (GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
    GPIO.setup(BT2, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
    GPIO.setup(BT3, GPIO.IN, pull_up_down = GPIO.PUD_UP) 
    global s
    s = sg90() # khởi tạo sg90
    # define các góc quay khi bấm các nút
    anglepulseBT1 = 10
    anglepulseBT2 = 50 
    anglepulseBT3 = 120
    print("Tất cả đã sẵn sàng")
    while True:
        if GPIO.input(BT1) == GPIO.LOW: 
            print("Quay 10 angle")
            controlservo(s, anglepulseBT1) 
        if GPIO.input(BT2) == GPIO.LOW: 
            print ("Quay 50 angle")
            controlservo(s, anglepulseBT2) 
        if GPIO. input (BT3) == GPIO.LOW: 
            print("Quay 120 angle")
            controlservo(s, anglepulseBT3) 
        time.sleep(0.2)
def controlservo (s, anglepulseBT):
    # Hàm này dùng để kiểm soát các các góc quay của servo
    # Giá trị anglepulseBT đưa vào sẽ làm vervo quay theo góc đó
    # Khi góc quay = 180độ thì lần quay tiếp theo sẽ quay theo chiều
    # ngược lại với góc quay <= 0độ
    # old code stuff
    # current = s.currentdirection ()
    # if current >= 180 or current <= 0:
    # anglepulseBT = -anglepulseBT
    # rotato = anglepulseBT + current # vị trí sẽ quay đến
    # xử lí rotator để tránh xảy ra vài lỗi
    # rotato = 180 if rotato >= 180 else 0 if rotato <= 0 else rotato
    # s.setdirection(rotato, 40) # quay đến vị trí rotator
    current = s.currentdirection ()
    # 180 is little dangerous. so cap at 160
    if current + anglepulseBT > 160:
        current == anglepulseBT
    else:
        current += anglepulseBT 
    if current < 0:
        print ("Illegal rotation")
        return anglepulseBT 
    # Trả về anglepulseBT mới để lần quay tiếp theo 
    # nó sẽ quay theo chiều âm hoặc dương return anglepulseBT
    s.setdirection (current, 10) 
    time.sleep(0.5)

class sg90:
    def __init__(self):
        self.pin = 6 # define pin SERVO
        GPIO.setmode (GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT) # setup nó thành OUTPUT
        self.servo = GPIO.PWM(self.pin, 50) # cho nó tần số 50Hz 
        self.servo.start(0.0) # khởi động
        self.direction = 90
    def cleanup (self):
        # dùng servo và giải phóng GPIO 
        self.servo.ChangeDutyCycle(self._henkan (0))
        time.sleep(0.3)
        self.servo.stop() 
        GPIO.cleanup()
    def currentdirection (self):
        # Hiển thị tốc độ hiện tại của servo 
        return self.direction
    def _henkan (self, value):
    # chuyển các giá trị 0 đến 180 thành 2 đến 12 
        return round (0.056*value + 2.0)
    def setdirection (self, direction, speed):
        for d in range (self.direction, direction, int (speed)):
            self.servo.ChangeDutyCycle(self._henkan (d)) 
            self.direction = d
        time.sleep(0.1)
        self.servo.ChangeDutyCycle (self._henkan(direction)) 
        self.direction = direction
try:
    main ()
except KeyboardInterrupt:
    s.cleanup()
