import machine
import utime
import ujson


class IRHelper:
    def __init__(self, rx_gpio, tx_gpio):
        self.rx_pin = machine.Pin(rx_gpio, machine.Pin.IN, machine.Pin.PULL_UP)
        self.tx_pin = machine.Pin(tx_gpio, machine.Pin.OUT)

        self.rx_pin.irq(
            trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING,
            handler=self.__logHandler)

        self.logList = []
        self.index = 0
        self.start = 0

        self.cmd_file_path = "/buttomCMD.txt"

    def _read_cmd(self):
        try:
            with open(self.cmd_file_path, 'r') as f:
                data = f.read() or "{}"
                json_data = ujson.loads(data)
        except:
            return {}
        return json_data

    def __logHandler(self, source):
        thisComeInTime = utime.ticks_us()
        if self.start == 0:
            self.start = thisComeInTime
            self.index = 0
            return

        self.logList.append(utime.ticks_diff(thisComeInTime, self.start))
        self.start = thisComeInTime
        self.index += 1

    def _irSendCMD(self, pwmObject, ctrlList, duty=360):
        pwmObject.deinit()
        pwmObject.init()
        pwmObject.freq(38000)
        pwmObject.duty(0)
        utime.sleep_ms(100)
        ctrlListLen = len(ctrlList)

        for i in range(ctrlListLen):
            if i % 2 == 0:
                pwmObject.duty(duty)
            else:
                pwmObject.duty(0)
            utime.sleep_us(ctrlList[i])
        pwmObject.duty(0)

    def select_cmd(self, key_name):
        json_data = self._read_cmd()
        return json_data[key_name]

    def record_cmd(self):
        print('Wait for infrared signal...')
        while True:
            utime.sleep_ms(200)

            if utime.ticks_diff(
                    utime.ticks_us(),
                    self.start) > 800000 and self.index > 0:
                thisIRcodeList = [item for item in self.logList]
                print(thisIRcodeList, "\n")
                tmpDict = self._read_cmd()
                cmd_key = input("set cmd key:")
                tmpDict[cmd_key] = thisIRcodeList
                jsDump = ujson.dumps(tmpDict)
                with open(self.cmd_file_path, "w+", encoding="utf-8") as out:
                    out.write(jsDump)
                print("log ok %s; \n" % cmd_key)

                # reset
                print("endir")
                self.logList = []
                self.index = 0
                self.start = 0
                return

    def send_cmd(self, key_name):
        ctrlList = self.select_cmd(key_name)
        irLedPwmObject = machine.PWM(self.tx_pin, freq=38000, duty=0)
        self._irSendCMD(irLedPwmObject, ctrlList)
        print(f"send finish {key_name}")

