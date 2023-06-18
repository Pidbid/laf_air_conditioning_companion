from wifi import do_connect
from machine import Pin,RTC,WDT,I2C,SoftI2C
import time,json
import gc
from aht10 import AHT10
from mqtt import MQTTClient
import random
from irHelper import IRHelper

gc.enable()
devicesId = "wicos"
aht = AHT10(0x38, 6, 7)
clientId = str(random.random())[2:]
mqtt = MQTTClient(clientId,"broker.emqx.io",port=1883)
ir = IRHelper(3,10)


def msg_callback(topic,msg):
    print(topic,msg.decode('utf-8'))
    payload = json.loads(msg.decode('utf-8'))
    command = ""
    if topic.decode('utf-8') == "/wicos/devices/control":
        if payload["devices"] == "air":
            # 空调控制
            command = payload["command"]
            ir.send_cmd(command)
    

if __name__ == "__main__":
    wdt0 = WDT(id=0,timeout=15000)
    do_connect()
    mqtt.set_callback(msg_callback)
    mqtt.connect()
    mqtt.subscribe("/wicos/devices/control")
    count = 0
    while True:
        wdt0.feed()
        if count % 5 == 0:
            temp = aht.temperature()
            humi = aht.humidity()
            put_str = json.dumps({"devices_id":devicesId,"humi":humi,"temp":temp})
            mqtt.publish("/wicos/devices/publish",put_str)
        count += 1
        if mqtt.check_msg():
            mqtt.wait_msg()
        time.sleep(1)







