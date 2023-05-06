#Viết chương trình mô phỏng điều hòa nhiệt độ, khi nhiệt độ cao thì bật quạt và role, nhiệt độ thấp
#thì để mình quạt, thấp nữa thì tắt hết
import time
import RPi.GPIO as GPIO
high_tmp = 40 
low_tmp =20 
very_low_tmp = 15 
def main(): 
    dht11 = 7 
    DIR = 25
    rl_1 = 16
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(DIR, GPIO.OUT) 
    GPIO.setup(rl_1, GPIO. OUT) 
    instance =DHT11(pin=dht11)
    PWD = GPIO.PWM(DIR, 100) # tần số 100Hz
    PWD.start(0)
    while True:
        temperature, humidity= instance.read()
        if temperature == 0 and humidity==0 and humidity < 20:
            continue
        if temperature >= high_tmp:
            PWD.ChangeDutyCycle(30) 
            GPIO.output(rl_1, True)
        elif very_low_tmp < temperature < high_tmp:
            PWD.ChangeDutyCycle(0)
            GPIO.output(rl_1, True)
        else:
            PWD.ChangeDutyCycle(0)
            GPIO.output(rl_1, False)
        print("Temp: %-3.1f C" % temperature)
        time.sleep(3)

class DHT11:
    def __init__(self, pin):
        self.pin = pin
        self.temperature = None
        self.humidity = None
    def read(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO. OUT)
        # HIGH
        GPIO.output(self.pin, GPIO.HIGH) 
        time.sleep(0.05)
        # LOW
        GPIO.output(self.pin, GPIO.LOW) 
        time.sleep(0.02)
        # chuyển nó sang input và pull up
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # thu thập dữ liệu
        count = 0
        last=-1 
        data= []
        while True:
            current = GPIO.input(self.pin) 
            data.append(current)
            if last != current:
                count = 0
                last=current
            else:
                count += 1
                if count >100:
                    break
        # phân tích độ dài của dữ liệu
        pull_up_lengths = self.parse_data_pull_up_lengths(data) 
        if len(pull_up_lengths) != 40:
            return(0, 0)
        # tính toán các bit
        bits = self.calculate_bits(pull_up_lengths) # khi có bit, tính toán các bye
        the_bytes = self.bits_to_bytes(bits)
        # ý nghĩa của các giá trị cảm biến được trả về
        #the_bytes [0]: humidity int
        #the_bytes [1]: humidity decimal #the_bytes [2]: temperature int
        #the_bytes [3]: temperature decimal
        self.temperature = the_bytes [2] + float(the_bytes [3]) / 10 
        self.humidity = the_bytes [0] + float(the_bytes [1]) / 10 
        return self.temperature, self.humidity # trả về kết quả 
    def parse_data_pull_up_lengths(self, data):
        STATE_INIT_PULL_DOWN = 1 
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5
        state = STATE_INIT_PULL_DOWN
        lengths = [] # nổ sẽ chứa độ dài dữ liệu trước 
        current_length = 0 # nó sẽ chứa độ dài dữ liệu sau 
        for i in range(len(data)) :
            current = data[i]
            current_length += 1
            if state== STATE_INIT_PULL_DOWN:
                if current == GPIO.LOW:
                    state = STATE_INIT_PULL_UP
                    continue
                else:
                # ok, chúng ta đã khởi tạo nó pull down 
                    continue
            if state== STATE_INIT_PULL_UP:
                if current == GPIO.HIGH:
                # ok, chúng ta đã khởi tạo nó pull up 
                    state = STATE_DATA_FIRST_PULL_DOWN 
                    continue
                else:
                    continue
            if state== STATE_DATA_FIRST_PULL_DOWN: 
                if current== GPIO.LOW:
                # chúng ta đã khởi tạo nó pull down # tiếp theo sẽ là dữ liệu pull up 
                    state= STATE_DATA_PULL_UP
                    continue
                else:
                    continue
            if state== STATE_DATA_PULL_UP:
                if current == GPIO.HIGH:
                # data pulled up, độ dài pull up quyết định đâu là 0 hoặc 1
                    current_length = 0
                    state = STATE_DATA_PULL_DOWN 
                    continue
                else:
                    continue
            if state== STATE_DATA_PULL_DOWN:
                if current == GPIO.LOW:
                #pulled down, chúng ta lưu trữ độ dài của pull up trước 
                    lengths.append(current_length)
                    state = STATE_DATA_PULL_UP 
                    continue
                else:
                    continue
        return lengths
    def calculate_bits(self, pull_up_lengths):
        # tìm khoảng thời gian ngắn nhất và dài nhất 
        shortest_pull_up = 1000
        longest_pull_up = 0
        for i in range(0, len(pull_up_lengths)): 
            length = pull_up_lengths [i]
            if length < shortest_pull_up:
                shortest_pull_up = length 
            if length > longest_pull_up:
                longest_pull_up = length
        # sử dụng haflway để xác định xem
        # khoảng thời gian đó là dài hay ngắn
        halfway =shortest_pull_up +(longest_pull_up -shortest_pull_up) / 2 
        bits = []
        for i in range(0, len(pull_up_lengths)):
            bit=False
            if pull_up_lengths [i]> halfway:
                bit = True
            bits.append(bit)
        return bits
    def bits_to_bytes(self, bits):
        the_bytes = []
        byte = 0
        for i in range(0, len(bits)):
            byte = byte << 1
            if(bits[i]):
                byte = byte | 1
            else:
                byte = byte | 0
            if((i+1)% 8 == 0):
                the_bytes.append(byte) 
                byte = 0
        return the_bytes
try:
    main()
except KeyboardInterrupt:
    print("Cleanup") 
    GPIO.cleanup()
