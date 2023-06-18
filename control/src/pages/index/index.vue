<template>
	<tm-app>
		<tm-navbar title="Wicos 的空调伴侣" hideHome>
			<template v-slot:right>
				<tm-icon _class="mr-n10" name="tmicon-redo" @click="page_reload"></tm-icon>
			</template>
		</tm-navbar>
		<tm-sheet :round="5">
			<view class="flex flex-row">
				<view class="flex-1 flex-col flex-center">
					<tm-icon name="/static/wendu.png" :fontSize="65"></tm-icon>
					<tm-text class="mt-15" :label="htInfo.temp.toFixed(2) + ' ℃'" :fontSize="35"></tm-text>
				</view>
				<view class="flex-1 flex-col flex-center">
					<tm-icon name="/static/shidu.png" :fontSize="65"></tm-icon>
					<tm-text class="mt-15" :label="htInfo.humi.toFixed(2) + ' ％'" :fontSize="35"></tm-text>
				</view>
			</view>
		</tm-sheet>
		<view class="flex flex-row flex-center">
			<tm-text label="更新日期" :fontSize="25" color="grey"></tm-text>
			<tm-text class="ml-15" :label="htInfo.dateFormat" :fontSize="25" color="grey"></tm-text>
		</view>
		<tm-sheet :round="5" _class="flex flex-col flex-center">
			<tm-grid :col="1" :width="686">
				<tm-grid-item :height="200">
					<tm-icon name="tmicon-angle-up" :fontSize="90" color="grey"></tm-icon>
				</tm-grid-item>
			</tm-grid>
			<tm-grid :col="2" :width="686">
				<tm-grid-item :height="200">
					<tm-icon v-if="airConditionerState.zhileng" name="/static/zhileng_open.png" :fontSize="110"></tm-icon>
					<tm-icon v-else name="/static/zhileng_close.png" :fontSize="110"></tm-icon>
				</tm-grid-item>
				<tm-grid-item :height="200">
					<tm-icon v-if="airConditionerState.zhire" name="/static/zhire_open.png" :fontSize="110"></tm-icon>
					<tm-icon v-else name="/static/zhire_close.png" :fontSize="110"></tm-icon>
				</tm-grid-item>
			</tm-grid>
			<tm-grid :col="1" :width="686">
				<tm-grid-item :height="200">
					<tm-icon name="tmicon-angle-down" :fontSize="90" color="grey"></tm-icon>
				</tm-grid-item>
			</tm-grid>
			<tm-grid :col="1" :width="686">
				<tm-grid-item :height="200">
					<tm-icon v-if="airConditionerState.open" name="/static/open.png" :fontSize="90" color="grey"></tm-icon>
					<tm-icon v-else name="/static/close.png" :fontSize="90" color="grey"></tm-icon>
				</tm-grid-item>
			</tm-grid>
		</tm-sheet>
		<tm-sheet :round="5" :padding="[5, 5]" :height="700">
			<tm-cell title="温湿度折线" rightIcon="" showAvatar>
				<template v-slot:avatar>
					<tm-icon name="tmicon-menu" color="primary"></tm-icon>
				</template>
			</tm-cell>
			<tm-chart ref="chart" :onOnInit="chart_init" :width="636" :height="650"></tm-chart>
		</tm-sheet>
	</tm-app>
</template>

<script lang="ts" setup>
import {
	ref,
	getCurrentInstance,
	computed,
	inject
} from "vue"
import {
	onShow,
	onLoad,
	onInit
} from "@dcloudio/uni-app";
import tmChart from "@/tmui/components/tm-chart/tm-chart.vue"
import { onMounted } from "vue";
import { ECharts } from "echarts";

interface HTINFO {
	humi: number
	temp: number
	date: number
}

const LafServerUrl = "" //你的APP地址
let mychart = ref<InstanceType<typeof tmChart>>(null)
const airConditionerState = ref({
	zhileng: false,
	zhire: false,
	open: false
})
const htInfo = ref({ humi: 0, temp: 0, date: 0, dateFormat: "" })
const chartData = ref({
	xAxis: [
		{
			type: 'category',
			name: "时间",
			date: [1, 2, 3, 4]
		}
	],
	yAxis: [
		{
			type: 'value',
			name: "温度/℃"
		},
		{
			type: 'value',
			name: "湿度/%"
		}
	],
	series: [
		{
			data: [],
			type: 'line',
			label: {
				show: true,
				position: 'top',
			}
		},
		{
			data: [],
			type: 'line',
			label: {
				show: true,
				position: 'top',
			}
		}
	]
})

onMounted(async () => {
	await data_init()
})

const data_init = async () => {
	const htData = await uni.$tm.fetch.get(LafServerUrl + "ht-info")
	const {code,data} = htData.data
	if(code == 0) htInfo.value = data
}

const chart_init = (chart: ECharts) => {
	chart.setOption(chartData.value)
}

const page_reload = () => {
	// #ifdef APP-PLUS
	uni.redirectTo({
		url: "../index/index"
	})
	// #endif
	// #ifdef H5
	window.location = ""
	// #endif

}
</script>
