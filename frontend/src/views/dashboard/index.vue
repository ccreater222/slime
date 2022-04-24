<template>
  <div class="dashboard-editor-container">
    <el-card class="box-card">
      <panel-group v-if="prepared" :resource="countdata.resource" :service="countdata.service" :task="countdata.task" :vul="countdata.vul" />
    </el-card>

    <el-row :gutter="20" style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>折线图</span>
        </div>
        <compare-line-chart v-if="prepared" ref="comparelinechart" :data="comparedata" />
      </el-card>
    </el-row>

    <el-row :gutter="20" style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <el-col :span="12">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>漏洞信息</span>
          </div>
          <el-table :data="vulinfo">
            <el-table-column label="name" prop="name" />
            <el-table-column label="ip" prop="ip" />
            <el-table-column label="port" prop="port" />
            <el-table-column label="subdomain" prop="subdomain" />
            <el-table-column label="title" prop="title" />
            <el-table-column label="plugin" prop="plugin" />
            <el-table-column label="tag" show-overflow-tooltip>
              <template slot-scope="scope">
                <el-tag v-for="tag in scope.row.tag" :key="tag" size="mini" style="margin-left: 10px;">
                  {{ tag }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="info" prop="info" show-overflow-tooltip />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>任务信息</span>
          </div>
          <el-table :data="taskinfo">
            <el-table-column show-overflow-tooltip label="taskid">
              <template slot-scope="scope">
                <router-link class="link" :to="{path: '/task/index',query: {taskid: scope.row.taskid }}">{{ scope.row.taskid }}</router-link>
              </template>
            </el-table-column>
            <el-table-column label="stage">
              <template slot-scope="scope">
                <el-tag v-for="stagename in Object.keys(scope.row.stageinfo)" :key="stagename" size="mini" style="margin-left: 10px;">
                  {{ stagename }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column
              label="status"
              column-key="status"
            >
              <template slot-scope="scope">
                <el-tag :type="tagstatus[scope.row.status]">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="created" prop="created" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getdashboard } from '@/api/dashboard'
import { getvul } from '@/api/vul'
import { gettask } from '@/api/task'
import CompareLineChart from './components/CompareLineChart.vue'
import PanelGroup from './components/PanelGroup.vue'
export default {
  name: 'Dashboard',
  components: { PanelGroup, CompareLineChart },
  data() {
    getdashboard().then(data => {
      this.$data.comparedata = data.data.comparedata
      this.$data.countdata = data.data.countdata
      this.$data.prepared = true
    })
    gettask({
      'page': 1,
      'size': 10,
      'sort': '',
      'desc': true,
      'condition': {},
      'selectall': false,
      'selected': []
    }).then(data => {
      this.$data.taskinfo = data.data.tasklist
    })
    getvul({ page: 1, size: 10, sort: '' }).then(
      data => {
        this.$data.vulinfo = data.data
      }
    )
    return {
      countdata: {},
      comparedata: {
      },
      prepared: false,
      taskinfo: [
        {
          stageinfo: [1, 2, 3, 4],
          status: 'execute',
          created: '2022',
          taskid: '123123123'
        }
      ],
      vulinfo: [
        {}
      ],
      tagstatus: {
        'done': 'success',
        'failed': 'danger',
        'execute': 'primary',
        'wait': 'warning'
      }
    }
  }
}
</script>
