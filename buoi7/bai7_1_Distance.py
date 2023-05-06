# Viết chương trình bấm BT1 thì đo khoảng cách từ cảm biến siêu âm(liên tục), hiển thị
# khoảng cách đo được lên LCD(Không dùng thư viện có sẵn)
import RPi.GPIO as GPIO 
import time
# Define GPIO cho LCD 
LCD_RS = 23
LCD_E = 27
LCD_D4 = 18
LCD_D5 = 17
LCD_D6 = 14
LCD_D7 = 3
LED_ON = 2
# Define some device constants
LCD_WIDTH = 16
LCD_CHR = True
# Maximum characters per line
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line 
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line #Timing constants
E_PULSE = 0.00005 
E_DELAY = 0.00005 
def main():
    BT1 = 21
    TRIG = 15
    ECHO = 4
    lcd_init()
    GPIO.output(LED_ON, True)
    global pulse_end
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN) 
    GPIO.output(TRIG, False) 
    while True:
        if GPIO.input(BT1) == 0:
            print("Waiting For Sensor To Settle") 
            time.sleep(2)
            # bật, tắt sóng siêu âm
            GPIO.output(TRIG, True) 
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            # tính thời gian
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time() 
            while GPIO.input(ECHO) == 1: 
                pulse_end = time.time() 
            pulse_duration = pulse_end - pulse_start 
            # tính khoảng cách
            distance = pulse_duration * 17150 
            distance = round(distance, 2)
            if distance > 100:
                lcd("ERROR")
                print("ERROR, try again")
            else:
                lcd(distance)
                print("Distance: %scm" % distance)
            time.sleep(1)
def lcd_init():
    GPIO.setmode(GPIO.BCM) # Use BCM GPIO
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)#E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS 
    GPIO.setup(LCD_D4, GPIO.OUT) # DB4 
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5 
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO.OUT) # Backlight enable
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD) 
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
def lcd_string(message):
    lcd_byte(LCD_LINE_1, False)
    for i in range(len(message)):
        lcd_byte(ord(message [i]), LCD_CHR)
def lcd_clear():
    lcd_string("      ")
    
 # Very headache function
def lcd_byte(bits, mode): 
    # Send byte to data pins 
    # bits = data
    # mode = True for character
    #       False for command
    GPIO.output(LCD_RS, mode) # RS 
    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False) 
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)  
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True) 
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True) 
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True) 
    #Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False) 
    time.sleep(E_DELAY) 
    # Low bits
    GPIO.output(LCD_D4, False) 
    GPIO.output(LCD_D5, False) 
    GPIO.output(LCD_D6, False) 
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
     GPIO.output(LCD_D7, True)
    # Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY) 
def lcd(distance):
    lcd_clear()
    lcd_string(str(distance))
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()