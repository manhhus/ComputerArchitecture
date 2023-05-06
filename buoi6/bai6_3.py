# Viết chương trình điều khiển servo, quay từ 0-180 độ và quay ngược lại(liên tục). 
import RPi.GPIO as GPIO 
import time 
def main():
    BT4 = 19
    GPIO.setmode(GPIO. BCM)
    GPIO.setup(BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    global s
    s = sg90() # khởi tạo sg90 
    print("Tất cả đã sẵn sàng")
    angle = 10
    while True:
        if GPIO.input(BT4) == 0:
            print("Quay 10 angle")
            angle = controlservo(s, angle) 
        time.sleep(0.2)
def controlservo(s, anglepulseBT):
    # Hàm này dùng để kiểm soát các các góc quay của servo
    # Giá trị anglepulseBT đưa vào sẽ làm vervo quay theo góc đó # Khi góc quay >= 180độ thì lần quay tiếp theo sẽ quay theo chiều # ngược lại với góc quay <= 0độ
    current = s.currentdirection()
    if current + anglepulseBT > 180 or current + anglepulseBT < 0: 
        anglepulseBT = -anglepulseBT
    current += anglepulseBT 
    print(current)
    s.setdirection(current, 10)
    time.sleep(0.5)
    # Trả về anglepulseBT mới để lần quay tiếp theo 
    # # nó sẽ quay theo chiều âm hoặc dương 
    return anglepulseBT
class sg90:
    def __init__(self):
        self.pin = 6 # define pin SERVO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT) # setup nó thành OUTPUT 
        self.servo = GPIO.PWM(self.pin, 50) # cho nó tần số 50Hz 
        self.servo.start(0.0) # khởi động
        self.direction = 90
    def cleanup(self):
        # dùng servo và gải phóng GPIO
        self.servo.ChangeDutyCycle(self._henkan(0))
        time.sleep(0.3) 
        self.servo.stop() 
        GPIO.cleanup()
    def currentdirection(self):
        # Hiển thị tốc độ hiện tại của servo 
        return self.direction
    def _henkan(self, value):
    # chuyển các giá trị 0 đến 180 thành 2 đến 12
        return round(0.056 * value + 2.0)
    def setdirection(self, direction, speed):
        for d in range(self.direction, direction, int(speed)) : 
            self.servo.ChangeDutyCycle(self._henkan(d)) 
            self.direction = d
            time.sleep(0.1)
        self.servo.ChangeDutyCycle(self._henkan(direction)) 
        self.direction = direction
try:
    main()
except KeyboardInterrupt:
    s.cleanup()
