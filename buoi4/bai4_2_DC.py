# Viết chương trình điều khiển tốc độ động cơ DC bằng nút bấm. Mỗi lần bấm BT1 tốc độ
# động cơ tăng thêm 20%, bấm BT2 giảm 20% và quay theo chiều kim đồng hồ. Bấm BT3
# tốc độ động cơ tăng 20%, bấm BT4 giảm 20% và ngược chiều kim đồng hồ. Hiển thị tốc
# độ (tương đối theo %) lên LCD mỗi lần bấm
# Giống bài 1 nhưng hiển thị lên LCD.
import RPi. GPIO as GPIO 
import time
3 # Define GPIO cho LCD
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
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line LCD LINE 2 = 0xC0 # LCD RAM address for the 2nd line # Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005 
def lcd_init():
    GPIO.setmode (GPIO.BCM)
    GPIO.setwarnings (False)
    # Use BCM GPIO numbers
    GPIO.setup (LCD_E, GPIO. OUT) # E 
    GPIO.setup (LCD_RS, GPIO.OUT) # RS 
    GPIO.setup (LCD_D4, GPIO.OUT) # DB4 
    GPIO.setup (LCD_D5, GPIO.OUT) # DB5 
    GPIO.setup (LCD_D6, GPIO.OUT) # DB6 
    GPIO.setup (LCD_D7, GPIO. OUT) # DB7
    GPIO.setup (LED_ON, GPIO. OUT) # Backlight enable
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)

    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x06, LCD_CMD) 
    lcd_byte(0x01, LCD_CMD) 
    
def lcd_string (message):
    lcd_byte(LCD_LINE_1, False)
    for i in range (len(message)):
        lcd_byte(ord(message [i]), LCD_CHR)
        
def lcd_clear():
    lcd_string("     ")

def lcd_byte(bits, mode):
    GPIO.output (LCD_RS, mode) # RS # High bits
    GPIO.output (LCD_D4, False)
    GPIO.output (LCD_D5, False)
    
    GPIO.output (LCD_D6, False) 
    GPIO.output (LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output (LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output (LCD_D5, True) 
    if bits&0x40==0x40:
         GPIO.output (LCD_D6, True) 
    if bits&0x80==0x80:
        GPIO.output (LCD_D7, True) # Toggle 'Enable' pin 
        time.sleep (E_DELAY)
    GPIO.output (LCD_E, True) 
    time.sleep (E_PULSE)
    GPIO.output (LCD_E, False)
    time.sleep (E_DELAY)
    # Low bits
    GPIO.output (LCD_D4, False) 
    GPIO.output (LCD_D5, False)
    GPIO.output (LCD_D6, False)
    GPIO.output (LCD_D7, False)
    if bits&0x01==0x01:
         GPIO.output (LCD_D4, True) 
    if bits&0x02==0x02:
        GPIO.output (LCD_D5, True) 
    if bits&0x04==0x04:
        GPIO.output (LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output (LCD_D7, True) # Toggle 'Enable' pin 
        time.sleep (E_DELAY)
    GPIO.output (LCD_E, True) 
    time.sleep (E_PULSE)
    GPIO.output (LCD_E, False) 
    time.sleep (E_DELAY)
def main():
    BT1 = 21
    BT2 = 26
    BT3 = 20
    BT4= 19
    DIR = 25
    PWD = 24
    GPIO.setmode (GPIO.BCM)
    # khởi tạo Icd
    lcd_init()
    GPIO.output (LED_ON, True)
    # khởi tạo và pull up các bút bấm
    GPIO.setup (BT1, GPIO. IN, pull_up_down=GPIO. PUD_UP) 
    GPIO.setup (BT2, GPIO.IN, pull_up_down =GPIO.PUD_UP) 
    GPIO.setup (BT3, GPIO.IN, pull_up_down =GPIO. PUD_UP) 
    GPIO.setup (BT4, GPIO. IN, pull_up_down=GPIO. PUD_UP) # Khởi tạo động cơ DC
    GPIO.setup (DIR, GPIO.OUT)
    GPIO.setup (PWD, GPIO.OUT)
    global PWD1, PWD2 # khởi tạo các biến global 
    PWD1 = GPIO.PWM(DIR, 100) # tần số 100Hz 
    PWD2 = GPIO.PWM(PWD, 100) # tần số 100Hz 
    PWD1.start (0) # khởi động

    PWD2.start (0) # 
    currentPWD1 = 20 
    currentPWD2 = 20 
    print("Chuẩn bị hoàn tất ok") 
    while True:
    # Tăng tốc và chạy theo chiều kim đồng hồ 
        if GPIO.input (BT1) == 0:   
            print("Press BT1")
            if currentPWD2 != 0:
                PWD2.ChangeDutyCycle (0)
                time.sleep(1)
            upPWD = int(0.2* currentPWD1)
            currentPWD1 = currentPWD1 + upPWD if currentPWD1 + upPWD < 100 else 100 
            if currentPWD1 == 0:
                currentPWD1 = 20
            # thay đổi tốc độ theo biến currentPWD1 
            PWD1.ChangeDutyCycle (currentPWD1)
            print("Tốc độ hiện tại: " +str(currentPWD1) + " theo chiều thuận")
            lcd_clear()
            lcd_string (str (currentPWD1))
            currentPWD2 = 0
            time.sleep(0.5)
        # Giảm tốc và chạy theo chiều kim đông hô
        if GPIO.input (BT2) == 0:
            print("Press BT2")
            PWD2.ChangeDutyCycle(0)
            downPWD = int(0.2* currentPWD1)
            currentPWD1 = (currentPWD1 - downPWD) if currentPWD1 - downPWD > 0 else 0 
            PWD1.ChangeDutyCycle(currentPWD1)
            print("Tốc độ hiện tại: " + str(currentPWD1) + " theo chiều thuận")
            lcd_clear()
            lcd_string (str (currentPWD1))
            currentPWD2 = 0
            time.sleep(0.5)
        # Tăng tốc và chạy theo ngược kim đồng hồ
        if GPIO.input (BT3) == 0:
            print("Press BT3")
            if currentPWD1 != 0:
                PWD1. ChangeDutyCycle (0)
                time.sleep(1)
            upPWD = int(20/100 * currentPWD2)
            currentPWD2 = (currentPWD2+ upPWD) if currentPWD2+ upPWD < 100 else 100
            if currentPWD2 == 0:
                currentPWD2 = 20
            # thay đổi tốc độ theo biến currentPWD2
            PWD2. ChangeDutyCycle (currentPWD2)
            print("Tốc độ hiện tại: " + '-' + str(currentPWD2))
            lcd_clear()
            lcd_string (str (currentPWD2))
            currentPWD1 = 0
            time.sleep(0.5)
        # Giảm tốc và chạy ngược chiều kim đồng hồ 
        if GPIO.input (BT4) == 0:
            print("Press BT4") 
            PWD1.ChangeDutyCycle (0) 
            downPWD = int (20/100 *currentPWD2)
            currentPWD2= (currentPWD2 - downPWD) if currentPWD2 - downPWD > 0 else 0
            print("Tốc độ hiện tại: " + '-' + str(currentPWD2))
            lcd_clear()
            lcd_string (str (currentPWD2))
            PWD2.ChangeDutyCycle (currentPWD2) 
            currentPWD1 = 0
            time.sleep(0.5)

try :
    main()
except KeyboardInterrupt:
    PWD1.stop()
    PWD2.stop()
    lcd_clear()