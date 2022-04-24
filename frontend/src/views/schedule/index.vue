<template>
  <div class="app-container">
    <el-divider><i class="el-icon-search" /></el-divider>
    <div class="filter-container">
      <el-row :gutter="20" justify="center">
        <el-col v-for="col in defaultFormThead" :key="col" :span="2">
          <el-input v-model="listQuery[col]" :placeholder="col" prefix-icon="el-icon-search" class="filter-item" @input="handleFilter" />
        </el-col>
        <el-col :span="1">
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
            搜索
          </el-button>
        </el-col>
        <el-col :span="1">
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-refresh-left" @click="handleReset">
            重置
          </el-button>
        </el-col>
      </el-row>
    </div>
    <el-divider><i class="el-icon-s-management" /></el-divider>
    <el-table :key="key" :data="tableData" fit highlight-curconst @sort-change="sortHandler">
      <el-table-column type="expand">
        <template slot-scope="scope">
          <el-timeline>
            <el-timeline-item
              v-for="task in scope.row.task"
              :key="task"
              icon="el-icon-success"
              :color="scope.row.task.indexOf(task) === scope.row.task.length - 1 ? '#0bbd87':''"
              :type="scope.row.task.indexOf(task) < scope.row.task.length - 1 ? 'primary':''"
              timestamp=""
              size="large"
            >
              <router-link class="link" :to="{path: '/task/index',query: {taskid: task }}">{{ task }}</router-link>

            </el-timeline-item>
          </el-timeline>
        </template>
      </el-table-column>
      <el-table-column v-for="column in defaultFormThead" :key="column" :label="column" sortable="custom" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tag
            v-if="column === 'status'"
            type="primary"
            size="mini"
            disable-transitions
          >
            {{ scope.row[column] }}
          </el-tag>
          <template v-else-if="column === 'templatetask'">
            <router-link class="link" :to="{path: '/task/index',query: {taskid: scope.row[column] }}">{{ scope.row[column] }}</router-link>
          </template>
          <template v-else>
            {{ scope.row[column] }}
          </template>
        </template>
      </el-table-column>
      <el-table-column label="action">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="success"
            :disabled="scope.row.status==='pause'"
            @click="handleAction('start',scope.row.taskid)"
          >开始</el-button>
          <el-button
            size="mini"
            type="warning"
            :disabled="scope.row.status!=='pause'"
            @click="handleAction('pause',scope.row.taskid)"
          >暂停</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleAction('delete',scope.row.taskid)"
          >删除</el-button>
          <el-button
            size="mini"
            type="info"
            @click="handleAction('execute',scope.row.taskid)"
          >执行</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :current-page="currentpage"
      :page-sizes="[20,50,100]"
      :page-size="size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
import { getschedule, actionschedule } from '@/api/schedule'
import waves from '@/directive/waves/index.js'
export default {
  name: 'Schedule',
  directives: {
    waves
  },
  data() {
    getschedule({ page: 1, size: 20 }).then(
      data => {
        this.$data.total = data.total
        this.$data.tableData = data.data.columndatas
      }
    )

    return {
      tableData: [],
      key: 1,
      listQuery: {},
      currentpage: 1,
      size: 20,
      total: 0,
      sort: '',
      desc: false,
      defaultFormThead: ['id', 'name', 'cron', 'templatetask', 'nexttime', 'executecount', 'status']
    }
  },
  methods: {
    handleAction(action, taskid) {
      actionschedule(action, { taskid: taskid }).then(
        data => {
          if (data.success) {
            this.$notify({
              title: '提示',
              type: 'success',
              message: '计划任务已' + {
                'start': '开始',
                'pause': '暂停',
                'delete': '删除',
                'execute': '执行'
              }[action]
            })
          } else {
            this.$notify(
              {
                title: '操作失败',
                type: 'error',
                message: data.msg
              }
            )
          }
        }
      )
    },
    handleReset() {
      this.listQuery = {}
    },
    callGetSchedule(data) {
      console.log(this.$data)
      var keymap = {
        page: this.$data.currentpage,
        size: this.$data.size,
        sort: this.$data.sort,
        desc: this.$data.desc,
        condition: this.$data.listQuery
      }
      Object.keys(keymap).forEach(k => {
        if (data[k] !== '' && data[k] !== [] && data[k] !== {} && data[k] !== undefined) {
          keymap[k] = data[k]
        }
      })
      return getschedule(keymap)
    },
    sortHandler: function(data) {
      this.$data.sort = data.column.label
      this.$data.desc = data.order === 'descending'
      this.refresh()
    },
    handleSizeChange: function(size) {
      this.$data.size = size
      this.callGetSchedule({}).then(data => {
        this.$data.tableData = data.data.columndatas
      })
    },
    handleCurrentChange: function(page) {
      this.$data.currentpage = page
      this.callGetSchedule({}).then(data => {
        this.$data.tableData = data.data.columndatas
      })
    },
    refresh: function() {
      this.callGetSchedule({}).then(data => {
        this.$data.tableData = data.data.columndatas
        // this.key = this.key + 1
      })
    },
    handleFilter: function(value) {
      this.refresh()
    }
  }
}
</script>

