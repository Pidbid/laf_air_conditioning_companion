import cloud from '@lafjs/cloud'

const mqttClient = cloud.shared.get("mqttClient")
const mqttConnect = cloud.shared.get("mqttConnect")

export default async function (ctx: FunctionContext) {
  const { topic = "/test/devices/control", content, qos = 0, retain = false } = ctx.body
  if (!content) return
  let publishContent = ""
  if (!mqttConnect) {
    await cloud.invoke("__init__")
  }
  try {
    publishContent = JSON.stringify(content)
  } catch (err) {
    publishContent = content.toString()
  }
  mqttClient.publish(topic, publishContent, { qos, retain })
}