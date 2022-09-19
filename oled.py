from oled.device import ssd1306
from oled.render import canvas
from PIL import ImageFont
import time


device = ssd1306(port=1, address=0x3C)
large_font = ImageFont.truetype('FreeMono.ttf', 24)

x = 0
while True:
    with canvas(device) as draw:
        draw.pieslice((x, 30, x+30, 60), 45, -45, fill=255)
        x += 10
    if x > 128:
        x = 0
    now = time.localtime()
    draw.text((0, 0), time.strftime('%H:%M:%S', now),
              font=large_font, fill=255)
    time.sleep(0.1)
