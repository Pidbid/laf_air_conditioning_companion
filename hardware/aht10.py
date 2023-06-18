"""
AHT10 i2c Temperature & Humidity sensor library for ESP32 Micropython\n
Based on aht10-python library from gejanssen (https://github.com/gejanssen/aht10-python/)\n
LouDFPV 19-12-2020\n
"""

import time
import machine

class AHT10:
    """
    AHT10 default i2c address is 0x38\n
    
    example:\n
    from aht10 import AHT10\n
    aht = AHT10(0x38, 21, 22) # i2c address, sclPin, sdaPin\n
    aht.printInfo() # print temperature and humidity to the console\n
    aht.temperature() # returns temperature as float\n
    aht.humidity() # returns humidity as float\n
    """
    _CONFIG = (0xE1, 0x08, 0x00) 
    _MEASURE_CMD = (0xAC, 0x33, 0x00)
    _READ_INFO = 6 # amount of bytes to read
    
    def __init__(self, addr, sclPin, sdaPin):
        self._addr = addr
        self._i2c = machine.SoftI2C(scl=machine.Pin(sclPin), sda=machine.Pin(sdaPin))
    
    def _read(self, data):
        self._data = self._i2c.readfrom(self._addr, data)
        return self._data
    
    def _write(self, data):
        self._i2c.writeto(self._addr, bytearray(data))
    
    def _enable(self):
        self._write(AHT10._CONFIG)
    
    def _measure(self):
        self._write(AHT10._MEASURE_CMD)
    
    def _readTemp(self):
        self._enable()
        self._measure()
        self._data = self._read(AHT10._READ_INFO)
        self._temp = ((self._data[3] & 0x0F) << 16) | (self._data[4] << 8) | self._data[5]
        self._ctemp = ((self._temp * 200) / 0x100000) - 50
        return self._ctemp
    
    def _readHum(self):
        self._enable()
        self._measure()
        self._data = self._read(AHT10._READ_INFO)
        self._hum = ((self._data[1] << 16) | (self._data[2] << 8) | self._data[3]) >> 4
        self._chum = (self._hum * 100 / 0x100000)
        return self._chum      
    
    def temperature(self):
        """
        returns temperature as float
        """
        temperature = self._readTemp()
        return temperature

    def humidity(self):
        """
        returns humidity as float
        """
        humidity = self._readHum()
        return humidity
        
    def printInfo(self):
        """
        prints temperature and humidity in console
        """
        temp = self._readTemp()
        hum = self._readHum()
        print(u'Temperature: {0:.2f}C'.format(temp))
        print(u'Humidity: {0:.2f}%'.format(hum))