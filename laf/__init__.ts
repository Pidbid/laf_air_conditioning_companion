import cloud from '@lafjs/cloud'
import { connect } from "mqtt"
import dayjs from "dayjs"
// import { Queue, guid, mqttMessageHandler } from "@/commonFunctions"

const db = cloud.database()

const mqttQueue = new Queue()
const db_topic = db.collection("iot-mqtt-topic")

//mqtt 初始化
const clientId = guid(16)

let mqttConnect = false

export default async function (ctx: FunctionContext) {
    //MQTT 初始化
    const mqttclient = connect("mqtt://broker.emqx.io:1883", {
        clientId,
        clean: true,
        connectTimeout: 4000,
        // username: 'emqx',
        // password: 'public',
        reconnectPeriod: 1000,
    })
    const topicRes = await db_topic.where({}).get()
    const mqttTopicArray = topicRes.data.map(topic => topic.topic)
    console.log(mqttTopicArray)
    mqttclient.on('connect', () => {
        console.log("mqtt connected")
        mqttConnect = true
        //订阅
        mqttclient.subscribe(mqttTopicArray, () => {
            console.log(`suscribe topic ${mqttTopicArray}`)
        })
    })
    mqttclient.on("message", async (topic, payload) => {
        await mqttMessageHandler(topic, payload.toString())
    })
    mqttclient.on("error", (err) => {
        console.log(err)
    })
    // 共享
    cloud.shared.set("mqttConnect", mqttConnect)
    cloud.shared.set("mqttClient", mqttclient)
    cloud.shared.set("Queue", Queue)
}


//队列
function Queue() {
    let items = []
    this.enqueue = function (element) {
        items.push(element)
    }
    this.dequeue = function () {
        return items.shift()
    }
    this.front = function () {
        return items[0]
    }
    this.isEmpty = function () {
        return items.length == 0
    }
    this.length = function () {
        return items.length
    }
}


//uuid
function guid(len = 32, firstU = true, radix = null) {
    const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('')
    const uuid = []
    radix = radix || chars.length

    if (len) {
        // 如果指定uuid长度,只是取随机的字符,0|x为位运算,能去掉x的小数位,返回整数位
        for (let i = 0; i < len; i++) uuid[i] = chars[0 | Math.random() * radix]
    } else {
        let r
        // rfc4122标准要求返回的uuid中,某些位为固定的字符
        uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-'
        uuid[14] = '4'

        for (let i = 0; i < 36; i++) {
            if (!uuid[i]) {
                r = 0 | Math.random() * 16
                uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r]
            }
        }
    }
    // 移除第一个字符,并用u替代,因为第一个字符为数值时,该guuid不能用作id或者class
    if (firstU) {
        uuid.shift()
        return `u${uuid.join('')}`
    }
    return uuid.join('')
}


//mqtt 消息处理函数
async function mqttMessageHandler(topic: string, payload: any) {
    let payloadFormat
    try {
        payloadFormat = JSON.parse(payload)
    } catch {
        payloadFormat = payload.toString()
    }
    const db_mqtt_log = db.collection("iot-mqtt-log")
    const db_data = db.collection("iot-data")
    await db_mqtt_log.add({ type: "subscribe", topic, payload: payloadFormat, date: new Date().getTime() })
    if (topic == "/test/devices/publish") {
        await db_data.add({ date: new Date().getTime(), dateFormat: dayjs(new Date().getTime() + 8 * 60 * 60 * 1000).format("YY/MM/DD HH:mm:ss"), humi: payloadFormat.humi, temp: payloadFormat.temp, devices_id: payloadFormat.devices_id })
    }
}