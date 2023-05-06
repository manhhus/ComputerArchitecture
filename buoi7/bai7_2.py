# Viết chương trình bấm BT1 thì mô phỏng cảm biến lùi của oto, khi khoảng cách nhỏ hơn 4cm
# thì bật role cảnh báo (cài số lùi) 
import RPi.GPIO as GPIO
import time 
def main():
    BT1 = 21
    TRIG = 15
    ECHO = 4
    rl_1 = 16
    global pulse_end
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (BT1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup (TRIG, GPIO. OUT)
    GPIO.setup (ECHO, GPIO.IN) 
    GPIO.setup (rl_1, GPIO.OUT) 
    GPIO.output (TRIG, False)
    while GPIO.input (BT1) != 0: 
        time.sleep(0.2)
    print("Bắt đầu mô phỏng cảm biến lùi ô tô")
    while True:
        #Waiting For Sensor To Settle 
        time.sleep (1)
        # bật, tắt sóng siêu âm 
        GPIO.output (TRIG, True)
        time.sleep(0.00001)
        GPIO.output (TRIG, False) 
        # tính thời gian
        while GPIO.input (ECHO) == 0: 
            pulse_start = time.time()
        while GPIO.input (ECHO) == 1: 
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start 
        # tính khoảng cách
        distance = pulse_duration * 17150
        distance = round (distance, 2)
        if distance <= 4:
            print ("Distance: %scm" % distance) 
            GPIO.output (rl_1, 1)
        else:
            GPIO.output (rl_1, 0)
    
try:
    main ()
except KeyboardInterrupt:
    GPIO.cleanup()