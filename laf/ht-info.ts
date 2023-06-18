import cloud from '@lafjs/cloud'

const db = cloud.database()
const db_data = db.collection("iot-data")

export default async function (ctx: FunctionContext) {
  const htRes = await db_data.aggregate([
    {
      $sort: {
        date: -1
      }
    },
    {
      $limit: 1
    }
  ]).end()
  return { code: 0, msg: "success", data: htRes.data[0] }
}