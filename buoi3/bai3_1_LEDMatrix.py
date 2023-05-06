# Đối với bài này chúng ta sử dụng thư viện Max7219, download tại đây (chú ý sau buổi thực hành
# chúng ta phải xóa thư viện và gỡ cài đặt) https://github.com/diy-hus/max7219
# Sau khi git về Raspberry, giải nén và sử dụng lệnh sau để cài đặt:
# python3 -m pip install --upgrade luma.led_matrix
# Khi thực hành xong, chúng ta xóa thư mục max7219 vừa download về và sử dụng lệnh sau để gỡ:
# python3 -m pip uninstall --upgrade luma.led_matrix 
######################## sudo raspi-config để tìm SPI bật lên
#Viết chương trình hiển thị chữ "hello worl" chạy trên màn hình LED matrix từ trái sang phải.
import re
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop 
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT 
def main(cascaded, block_orientation, rotate):

    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=cascaded, block_orientation=block_orientation, rotate=rotate) 
    device.contrast(20)
    #debugging purpose
    print("[-] Matrix initialized")
    # print hello world on the matrix display
    msg= "hello world"
    #debugging purpose
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)



if __name__ == "__main__":
#cascaded = Number of cascaded MAX7219 LED matrices, default=1 
#block_orientation choices 0, 90, -90, Corrects block orientation, default=0 
#rotate choices 0, 1, 2, 3, Rotate display 0=0°, 1-90°, 2=180°, 3=270°, default=0
    try:
        main(cascaded=1, block_orientation=-90, rotate=1) 
    except KeyboardInterrupt:
        pass
