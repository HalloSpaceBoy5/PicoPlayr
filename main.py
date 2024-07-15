from wavplayer import WavPlayer
from machine import Pin,SPI,freq
from dpot import MCP4241
import sdcard
from time import sleep
import os
from st7789 import ST7789
from math import ceil, floor 
sck_pin = Pin(8)   # Serial clock output
ws_pin = Pin(9)    # Word clock output
sd_pin = Pin(7)
sck = Pin(2)
mosi = Pin(3)
miso = Pin(4)
cs = Pin(16)

# Initialize SPI without MISO
mcp4241 = MCP4241(SPI(0, baudrate=10_000_000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso), cs)
buttonpin=Pin(1, Pin.IN, Pin.PULL_UP)
Display=ST7789()
sd=sdcard.SDCard(SPI(1,baudrate=40_000_000,sck=Pin(10),mosi=Pin(11),miso=Pin(12)),Pin(13))
sd.init_spi(25_000_000)
vfs=os.VfsFat(sd)

# Mount the SD card
os.mount(sd,'/sd')
Player=WavPlayer(0,sck_pin,ws_pin,sd_pin,40000)
Player.play("Test.wav")



state=False
counter=0


# deprecated volume mod function, works with faster processor
def check_vol():
    if Player.beginwrite:
        for i in range(0, Player.num_read, 2):
            if Player.beginwrite==False:
                print("stopped early")
                return
            integer = Player.wav_samples_mv[i] | (Player.wav_samples_mv[i+1] << 8)
            integer=int(integer*Player.volume)
            if integer < -32768:
                integer = -32768
            elif integer > 32767:
                integer = 32767
            
            Player.wav_samples_mv_buf[i]=integer & 0xFF
            Player.wav_samples_mv_buf[i]=(integer >> 8) & 0xFF
        """
        for f in range(0, len(Player.wav_samples_mv_buf), 2):
            if Player.beginwrite==False:
                print("stopped early")
                break
            integer = Player.wav_samples_mv[f] | (Player.wav_samples_mv[f+1] << 8)
            integer=int(integer*Player.volume)
            if integer < -32768:
                integer = -32768
            elif integer > 32767:
                integer = 32767
            
            Player.wav_samples_mv_buf[f]=integer & 0xFF
            Player.wav_samples_mv_buf[f]=(integer >> 8) & 0xFF
        Player.beginwrite=False
        """
        
# Write volume level to pots 0 and 1 on the MCP4241
mcp4241.write_pot(0, 10)
mcp4241.write_pot(1, 10)
while True:  
    #Same display and driver for PicoBoy. cross compatability?                                                                                                                                                                                       
    Display.fill(ST7789.color(100,100,100))
    Display.text("This is PicoWav!", 10, 100, ST7789.color(255,255,255))
    Display.show_screen()






