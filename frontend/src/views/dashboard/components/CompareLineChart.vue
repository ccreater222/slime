<template>
  <div :style="{height:height,width:width}" />
</template>
<script>
import * as echarts from 'echarts/core'
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'
import { LineChart } from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition
])
export default {
  props: {
    data: {
      type: Object,
      required: true
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '350px'
    }
  },
  mounted() {
    this.$nextTick(_ => {
      this.init()
    })
  },
  methods: {
    init() {
      var chartDom = this.$el
      var myChart = echarts.init(chartDom)
      var option
      var series = []
      var date = []
      var daylen = 0
      Object.keys(this.data).forEach(key => {
        daylen = this.data[key].length
        series.push({
          name: key,
          type: 'line',
          stack: key,
          smooth: true,
          data: this.data[key],
          emphasis: {
            focus: 'series'
          }
        })
      })
      var today = new Date()
      var olddest = new Date(today.getFullYear(), today.getMonth(), today.getDate() - daylen)
      var tempday = null
      for (var i = 0; i < daylen; i++) {
        tempday = new Date(olddest.getFullYear(), olddest.getMonth(), olddest.getDate() + i)
        date.push(tempday.toLocaleDateString())
      }

      option = {
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: Object.keys(this.data)
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            data: date
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series
      }

      option && myChart.setOption(option)
    }
  }
}
</script>
