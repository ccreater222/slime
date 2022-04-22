<template>
  <el-row :gutter="20">
    <el-col ref="col" :span="16">
      <div ref="echart" class="chart" :style="{height:height,width:width}" />
    </el-col>
    <el-col :span="8">
      <el-table :data="chartData" :max-height="height">
        <el-table-column prop="name" :label="keyword" />
        <el-table-column prop="value" label="总数" />
      </el-table>
    </el-col>
  </el-row>
</template>
<script>
const echarts = require('echarts/lib/echarts')
require('echarts/lib/component/title')
require('echarts/lib/component/tooltip')
require('echarts/lib/component/legend')
require('echarts/lib/chart/pie')
import { analyzeresource } from '@/api/resource'

export default {
  props: {
    chartDataPromise: {
      type: Promise,
      required: true
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '100%'
    },
    keyword: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      echarts: null,
      chartData: null
    }
  },
  mounted() {
    this.chartDataPromise.then(data => {
      return analyzeresource(data)
    }).then(data => {
      console.log(data)
      this.chartData = data.data
      this.setOptions(data.data)
    })
    this.$nextTick(() => {
      this.initChat()
    })
  },
  beforeDestroy() {
    if (!this.echarts) {
      return
    }
    this.echarts.dispose()
    this.echarts = null
  },
  methods: {
    refreshdata() {
      this.chartDataPromise.then(data => {
        return analyzeresource(data)
      }).then(data => {
        this.chartData = data.data
        this.setOptions(data.data)
      })
    },
    initChat() {
      this.echarts = echarts.init(this.$refs.echart, null, {
        height: this.height,
        width: this.width
      })
      this.setOptions(this.chartData)
    },
    setOptions(data) {
      if (!data) {
        return
      }
      data = data.slice(0, 10)
      var option
      option = {
        title: {
          text: this.keyword,
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            type: 'pie',
            radius: '50%',
            data: data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      this.echarts.setOption(option)
      this.resize()
    },
    resize() {
      this.echarts.resize({
        width: this.$refs.col.$el.offsetWidth,
        height: this.$refs.col.$el.offsetHeight
      })
    }
  }
}
</script>
