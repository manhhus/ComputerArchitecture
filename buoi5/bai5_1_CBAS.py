# Viết chương trình đọc giá trị cảm biến ánh sáng, hiển thị trạng thái sáng-tối lên LCD (lấy tay
# che cảm biến để mô phỏng hiện tượng trời tối) 

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
LCD_CMD= False
LCD_LINE_1 = 0x80 # LCD_RAM address for the 1st line 
LCD_LINE_2 = 0xC0 # LCD_RAM address for the 2nD_line # Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005
sensor = 5 #tại sao?
def lcd_init():
    GPIO.setmode(GPIO.BCM)
    # Use BCM GPIO numbers
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO. OUT) #E
    GPIO.setup(LCD_RS, GPIO.OUT) # RS 
    GPIO.setup(LCD_D4, GPIO. OUT) # DB4 
    GPIO.setup(LCD_D5, GPIO.OUT) # DB5
    GPIO.setup(LCD_D6, GPIO.OUT) # DB6
    GPIO.setup(LCD_D7, GPIO.OUT) # DB7
    GPIO.setup(LED_ON, GPIO. OUT) # Backlight enable
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD) 
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x01, LCD_CMD) 
def lcd_string(message):
    message= message.center(LCD_WIDTH," ") 
    lcd_byte(LCD_LINE_1, False)
    for i in range(len(message)):
        lcd_byte(ord(message[i]), LCD_CHR)
def lcd_clear():
    lcd_string("                ")
def lcd_byte(bits, mode):
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
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor, GPIO.IN, GPIO. PUD_UP) 
    # khởi tạo lcD
    lcd_init()
    #sleep or bug 
    time.sleep(4)
    GPIO.output(LED_ON, True)
    while True:
        #sang
        print(GPIO.input(sensor))
        if GPIO.input(sensor) == 0:
            lcd_clear()
            print("sang")
            lcd_string("Sang")
            time.sleep(0.5)
        # toi
        else:
            lcd_clear()
            print("Toi")
            lcd_string("Toi")
            time.sleep(0.5)
except KeyboardInterrupt:
    lcd_clear()

