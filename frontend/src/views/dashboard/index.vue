<template>
  <div class="dashboard-editor-container">
    <panel-group :resource="100" :service="100" :task="5" :vul="100" />
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <compare-line-chart ref="comparelinechart" :data="comparedata" />
    </el-row>
    <el-row gutter="20" style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-col :span="12" >
        <el-table>
        </el-table>
      </el-col>
      <el-col :span="12">
        <el-table :data="taskinfo" >
          <el-table-column prop="stage" />
          <el-table-column prop="status" />
          <el-table-column prop="created" />
          <el-table-column prop="taskid" />
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import CompareLineChart from './components/CompareLineChart.vue'
import PanelGroup from './components/PanelGroup.vue'
export default {
  name: 'Dashboard',
  components: { PanelGroup, CompareLineChart },
  data() {
    return {
      comparedata: {
        resource: [100, 200, 200, 200, 200, 250, 250],
        vul: [0, 1, 10, 50, 51, 52, 60],
        task: [0, 10, 30, 40, 40, 40, 50]
      },
      taskinfo: [
        {
          stage: [1,2,3,4],
          status: 'execute',
          created: '2022',
          taskid: '123123123'
        }
      ],
      vulinfo: []
    }
  },
  computed() {}
}
</script>
