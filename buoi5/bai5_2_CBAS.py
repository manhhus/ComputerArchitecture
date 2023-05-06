# Viết chương trình mô phỏng công tắc đèn đường, khi trời tối bật role 1, sau 2s bật tiếp role 2,
# khi trời sáng thì tắt cả 2 role đồng thời (giải thích vì sao) 

# Việc đợi một khoảng thời gian nhất định trước khi bật role 2 có thể giúp giảm thiểu sự va 
# đập điện áp khi cả hai role được bật cùng lúc, giúp bảo vệ các thiết bị điện và kéo dài tuổi thọ của chúng.
import RPi.GPIO as GPIO 
import time
sensor = 5
rl_1 = 16 #giải thích ý nghĩa dòng lệnh 
rl_2 = 12
try:
    GPIO.setmode(GPIO. BCM)
    GPIO.setup(sensor, GPIO.IN, GPIO. PUD_UP) 
    GPIO.setup(rl_1, GPIO. OUT) 
    GPIO.setup(rl_2, GPIO.OUT) 
    while True:
        # toi
        if GPIO.input(sensor) == 1:
            GPIO.output(rl_1, 1) 
            for i in range(10):
                if GPIO.input(sensor) == 0: 
                    GPIO.output(rl_1, 0) 
                    GPIO.output(rl_2, 0) 
                    break
                if i== 9:
                    GPIO.output(rl_2, 1)
                time.sleep(0.2)
        # sang
        if GPIO.input(sensor) == 0:
            GPIO.output(rl_1, 0)
            GPIO.output(rl_2, 0)
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
