# Viết chương trình đọc nút bấm, BT1 đèn sáng, BT2 đèn tắt, BT3 đèn nhấp nháy chu kỳ
# 1s, BT4 (lần 1 đèn sáng, lần 2 đèn tắt liên tục). hiển thị trạng thái của đèn lên terminal.

import RPi.GPIO as GPIO
import time
def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20
    BT4 = 19
    LED = 13
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED,GPIO.OUT)
    GPIO.output(LED, GPIO.HIGH)
    ispressBT4 = False
    ispressBT3 = False
    while True:
            if GPIO.input(BT1) == GPIO.LOW:
                print("BT1 pressed")
                ispressBT3 = False
                GPIO.output(LED, GPIO.LOW)
                time.sleep(0.5)
            if GPIO.input(BT2) == GPIO.LOW:
                print("BT2 pressed")
                ispressBT3 = False
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(0.5)
            if GPIO.input(BT3) == GPIO.LOW:
                print("BT3 pressed")
                ispressBT3 = True
                GPIO.output(LED, GPIO.LOW)
                time.sleep(0.5)
            if GPIO.input(BT4) == GPIO.LOW:
                print("BT4 pressed")
                ispressBT3 = False
                if ispressBT4:
                    GPIO.output(LED, GPIO.HIGH)
                    ispressBT4 = False
                    time.sleep(0.5) 
                    continue
                if not ispressBT4:
                    GPIO.output(LED, GPIO.LOW)
                    ispressBT4 = True
                    time.sleep(0.5) 
                    continue 
            if ispressBT3:
                print("Durring Blinking")
                if GPIO.input(LED) == GPIO.LOW:
                    GPIO.output(LED, GPIO.HIGH)
                    time.sleep(0.5) 
                if GPIO.input(LED) == GPIO.HIGH:
                    GPIO.output(LED, GPIO.LOW)
                    time.sleep(0.5)
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()               