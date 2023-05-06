# Viết chương trình bấm BT_1 điều khiển role 1, role 2, đèn LED với các kịch bản khác
# nhau 

import RPi.GPIO as GPIO
import time
import os
def main():
	LED = 13
	LED_ON = 2
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED, GPIO.OUT)
	GPIO.setup(LED_ON, GPIO.OUT)
	while True:
		if GPIO.input(LED) == GPIO.LOW:
			GPIO.output(LED, GPIO.HIGH)
			GPIO.output(LED_ON, True)
			time.sleep(1)
		if GPIO.input(LED) == GPIO.HIGH:
			GPIO.output(LED, GPIO.LOW)
			GPIO.output(LED_ON, False)
			time.sleep(1)
if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		GPIO.cleanup()