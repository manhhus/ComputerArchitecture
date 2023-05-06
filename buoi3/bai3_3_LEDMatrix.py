# Viết chương trình hiển thị các số từ 0-9 chạy liên tục trên LED matrix từ phải sang trái.
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
    device = max7219(serial, cascaded=cascaded, block_orientation=block_orientation, rotate=2) 
    device.contrast (20)
    #debugging purpose
    print("[-] Matrix initialized")
    # print hello world on the matrix display
    msg= "  0  1  2  3  4  5  6  7  8  9"
    #debugging purpose
    print("[-] Printing: %s" % msg)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)
if __name__ == "__main__":
#cascaded = Number of cascaded MAX7219 LED matrices, default=1 
#block_orientation choices 0, 90, -90, Corrects block orientation, default=0 
#rotate choices 0, 1, 2, 3, Rotate display 0=0°, 1-90°, 2=180°, 3=270°, default=0
    try:
        main(cascaded=1, block_orientation=-90, rotate=0) 
    except KeyboardInterrupt:
        pass
