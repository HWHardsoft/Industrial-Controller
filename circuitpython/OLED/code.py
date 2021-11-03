# CircuitPython Example Code for OLED shield
# Copyright 2021 Zihatec GmbH, www.zihatec.de
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions: The above copyright notice and this
# permission notice shall be included in all copies or substantial
# portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT
# WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import board
import busio
import displayio
import digitalio
import terminalio


#*********************************************************************
# Configuration MCP23008
#*********************************************************************
from adafruit_mcp230xx.mcp23008 import MCP23008
i2c = board.I2C()
mcp = MCP23008(i2c)  # MCP23008

# call the get_pin function to get an instance of a pin on the MCP23008
button1 = mcp.get_pin(0)
button2 = mcp.get_pin(1)
button3 = mcp.get_pin(2)
led1 = mcp.get_pin(4)
led2 = mcp.get_pin(5)
led3 = mcp.get_pin(6)
beep = mcp.get_pin(7)

# Setup button pins as an input with a pull-up resistor enabled
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

# Setup led pins and beeper as an output that's at a low logic level.
led1.switch_to_output(value=False)
led2.switch_to_output(value=False)
led3.switch_to_output(value=False)
beep.switch_to_output(value=False)


#*********************************************************************
# Configuration SH1106
#*********************************************************************
from adafruit_display_text import label
import adafruit_displayio_sh1106
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle

displayio.release_displays()

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# SH1107 is vertically oriented 64x128
WIDTH = 132 # very important 132 not 128 !!!
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_sh1106.SH1106(
    display_bus, width=WIDTH, height=HEIGHT, rotation=0
)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Load image 128x64
bitmap = displayio.OnDiskBitmap("/cp.bmp")

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
group = displayio.Group()
group.append(tile_grid)



def clearscreen():
    #clear screen
    rect = Rect(0, 0, 128, 64, fill=0x000000)
    splash.append(rect)


def intro():
    # print intro text
    clearscreen()
    text1 = "Display Shield"  # text in upper row
    text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=10, y=5)
    splash.append(text_area)
    text1 = "www.zihatec.de"  # text in middle row
    text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=10, y=26)
    splash.append(text_area)
    text1 = "Press a key!"  # text in lower row
    text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=10, y=48)
    splash.append(text_area)
    display.show(splash)

intro()

while True:
    if (button1.value == False): # button 1 (S1) pressed?
        print ("S1 pressed")
        led1.value = True   # LED D1 on
        beep.value = True   # beeper on

        #clear screen
        clearscreen()

        #showing a bitmap

        display.show(group)

        time.sleep(1)
        #intro()


    if (button2.value == False): # button 2 (S2) pressed?
        print ("S2 pressed")
        led2.value = True   # LED D2 on

        clearscreen()
        #drawing of different shapes
        #draw a circle
        circle = Circle(25, 31, 20, fill=0xFFFFFF, outline=0x000000)
        splash.append(circle)

        #draw a rectangle
        rect = Rect(50, 12, 40, 40, fill=0x000000, outline=0xFFFFFF)
        splash.append(rect)

        #draw a triangle
        triangle = Triangle(100, 52, 110, 12, 120, 52, fill=0xFFFFFF)
        splash.append(triangle)
        display.show(splash)

        time.sleep(1)
        #intro()


    if (button3.value == False): # button 3 (S3) pressed?
        print ("S3 pressed")
        led3.value = True   # LED D3 on

        clearscreen()

        text1 = "1234567890"  # text in upper row
        text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=10, y=5)
        splash.append(text_area)
        text1 = "ABCDEFGH"  # text in middle row
        text_area = label.Label(terminalio.FONT, text=text1, scale=2, color=0xFFFFFF, x=10, y=21)
        splash.append(text_area)
        text1 = "abcdefgh"  # text in lower row
        text_area = label.Label(terminalio.FONT, text=text1, scale=2, color=0x000000, background_color=0xFFFFFF, x=10, y=48)
        splash.append(text_area)

        display.show(splash)

        time.sleep(1)
        #intro()

    led1.value = False   # LED D1 off
    led2.value = False   # LED D2 off
    led3.value = False   # LED D3 off
    beep.value = False   # beeper off



