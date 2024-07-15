from machine import Pin, SPI

class MCP4241:

    def __init__(self, spi, cs_pin):
        self.spi = spi
        self.cs = Pin(cs_pin, Pin.OUT)
        self.cs.value(1)  
        self.init_device()


    def spi_write(self, data):
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def spi_read(self, num_bytes):
        self.cs.value(0)  
        data = self.spi.read(num_bytes)
        self.cs.value(1) 
        return data

    def init_device(self):
        tcon_value = 0b11111111 
        self.spi_write(bytearray([(self.TCON_CMD << 4), tcon_value]))

    def write_pot(self, channel, value):

        if channel not in [0, 1] or not 0 <= value <= 255:
            raise ValueError("Invalid channel or value")
        

        if channel==1:
            command=0b00010000
        else:
            command=0b00000000
        data = bytes(bytearray([command, value]))
        print(data)
        self.spi_write(data)

    def read_pot(self, channel):
        if channel not in [0, 1]:
            raise ValueError("Invalid channel")
        
        if channel==1:
            command=0b00011100
        else:
            command=0b00001100
        self.spi_write(bytearray([command, 0x00]))
        data = self.spi_read(1)
        print(f"Read from channel {channel}: {data[0]}")
        return data[0]