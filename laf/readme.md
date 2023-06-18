### 数据库

#### iot-mqtt-log
- 存放所有log数据
- 结构为
```
{
    type:string,// subscribe 或 publish
    topic:string,
    payload:object,
    date:timestamp
}
```

#### iot-mqtt-topic
- 所有订阅或被订阅的topic
- 结构为
```
{
    type:string // server 或 devices 分别表示那个设备订阅的
    topic:string
}
```

#### iot-data
- 所有数据存放
- 结构为
```
{
    date:timestamp,
    dateFormat:string, //格式化日期
    humi:float,//湿度
    temp:float //温度
}
```