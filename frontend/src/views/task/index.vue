<template>
  <div class="app-container">
    <el-divider><i class="el-icon-search" /></el-divider>
    <div class="filter-container">
      <el-row :gutter="20" justify="center">
        <el-col v-for="col in taskcolumn" :key="col" :span="2">
          <el-input v-model="listQuery[col]" :placeholder="col" prefix-icon="el-icon-search" class="filter-item" @input="handleFilter" />
        </el-col>
        <el-col :span="2">
          <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
            搜索
          </el-button>
        </el-col>

      </el-row>
    </div>
    <div class="filter-container">
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-video-play" @click="handleAction('start')">
        开始
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-video-pause" @click="handleAction('pause')">
        暂停
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-circle-close" @click="handleAction('stop')">
        停止
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-refresh-left" @click="handleAction('restart')">
        重启
      </el-button>
    </div>
    <el-divider><i class="el-icon-s-management" /></el-divider>

    <el-table :key="key" :data="tasklist" fit highlight-curconst @sort-change="sortHandler" @select="handleSelect" @select-all="handleSelectAll">
      <el-table-column type="expand">
        <template slot-scope="scope">
          <el-form :model="scope.row" label-position="left" label-width="auto">
            <el-form-item>
              <el-tabs type="card">
                <el-tab-pane v-for="stagename in Object.keys(scope.row.stageinfo)" :key="stagename" :label="stagename">
                  <el-collapse style="margin-left: 10px;margin-right: 10px;" accordion>
                    <el-collapse-item title="日志面板" name="Log">
                      <el-tabs tab-position="left">
                        <el-tab-pane v-for="plugin in Object.keys(scope.row.log[stagename])" :key="plugin" :label="plugin">
                          <el-input :value="scope.row.log[stagename][plugin]" type="textarea" autosize readonly />
                        </el-tab-pane>
                      </el-tabs>
                    </el-collapse-item>
                    <el-collapse-item title="配置面板" name="Config">
                      <el-tabs tab-position="left">
                        <el-tab-pane v-for="plugin in scope.row.stageinfo[stagename]" :key="plugin.name" :label="plugin.name">
                          <el-form :model="plugin.config" label-position="left" label-width="auto">
                            <el-form-item v-for="configname in Object.keys(plugin.config)" :key="configname" :label="configname">
                              <el-input v-model="plugin.config[configname]" readonly />
                            </el-form-item>
                          </el-form>
                        </el-tab-pane>
                      </el-tabs>
                    </el-collapse-item>
                  </el-collapse>
                </el-tab-pane>
              </el-tabs>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column
        type="selection"
        width="55"
      />
      <el-table-column label="taskid" :show-overflow-tooltip="true" prop="taskid" />
      <el-table-column
        label="status"
        column-key="status"
        sortable
        :filters="[{text: 'success', value: 'success'}, {text: 'failed', value: 'failed'}, {text: 'wait', value: 'wait'}, {text: 'execute', value: 'execute'}]"
        :filter-method="tagFilterHandler"
      >
        <template slot-scope="scope">
          <el-tag :type="tagstatus[scope.row.status]">
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="stage">
        <template slot-scope="scope">
          <el-tag v-for="stagename in Object.keys(scope.row.stageinfo)" :key="stagename" size="mini" style="margin-left: 10px;">
            {{ stagename }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="log" prop="log" show-overflow-tooltip>
        <template slot-scope="scope">
          {{ scope.row.log }}
        </template>
      </el-table-column>
      <el-table-column label="created" prop="created" />
      <el-table-column label="action">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="success"
            :disabled="scope.row.status!=='wait'"
            @click="handleAction('start',scope.row.taskid)"
          >开始</el-button>
          <el-button
            size="mini"
            type="warning"
            :disabled="scope.row.status!=='execute'"
            @click="handleAction('pause',scope.row.taskid)"
          >暂停</el-button>
          <el-button
            size="mini"
            type="danger"
            :disabled="scope.row.status!=='execute'"
            @click="handleAction('stop',scope.row.taskid)"
          >停止</el-button>
          <el-button
            size="mini"
            type="info"
            :disabled="scope.row.status==='wait'"
            @click="handleAction('restart',scope.row.taskid)"
          >重启</el-button>
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
// TODO: 将任务添加到计划任务
import { actiontask, gettask } from '@/api/task'
import waves from '@/directive/waves/index.js'
export default {
  name: 'TASK',
  directives: {
    waves
  },
  props: {
    taskid: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      key: 1,
      tasklist: [],
      taskcolumn: [],
      listQuery: {},
      currentpage: 1,
      size: 20,
      total: 0,
      tagstatus: {
        'done': 'success',
        'failed': 'danger',
        'execute': 'primary',
        'wait': 'warning'
      },
      selectall: false,
      selected: []
    }
  },
  mounted() {
    if (this.taskid !== '') {
      this.$data.listQuery['taskid'] = this.taskid
    }
    this.callGetTask({}).then(data => {
      this.$data.tasklist = data.data.tasklist
      this.$data.taskcolumn = data.data.taskcolumn
      this.$data.total = data.total
    })
  },
  methods: {
    handleAction(action) {
      var keymap = {
        page: this.$data.currentpage,
        size: this.$data.size,
        sort: this.$data.sort,
        desc: this.$data.desc,
        condition: this.$data.listQuery,
        selectall: this.$data.selectall,
        selected: this.$data.selected
      }
      if (arguments.length === 2) {
        keymap.selectall = false
        keymap.selected = [arguments[1]]
      }

      actiontask(action, keymap).then(
        data => {
          if (data.success) {
            this.$notify({
              title: '提示',
              type: 'success',
              message: '任务已' + {
                'start': '开始',
                'pause': '暂停',
                'restart': '重启',
                'stop': '停止'
              }[action]
            })
            this.refresh()
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
    refresh() {
      this.callGetTask({
        page: this.$data.page,
        size: this.$data.size
      }).then(data => {
        this.$data.tasklist = data.data.tasklist
        this.$data.taskcolumn = data.data.taskcolumn
        this.$data.total = data.total
      })
    },
    handleCurrentChange(page) {
      this.$data.currentpage = page
      this.callGetTask({}).then(
        data => {
          this.$data.tasklist = data.data.tasklist
        }
      )
    },
    handleSizeChange(size) {
      this.$data.size = size
      this.callGetTask({}).then(
        data => {
          this.$data.tasklist = data.data.tasklist
        }
      )
    },
    sortHandler(data) {
      console.log(data.column)
      this.$data.sort = data.column.label
      this.$data.desc = data.order === 'descending'
      this.callGetTask({}).then(
        data => {
          this.$data.tasklist = data.data.tasklist
        }
      )
    },
    handleSelect(value) {
      const selectedtaskid = []
      value.forEach(v => {
        selectedtaskid.push(v.taskid)
      })
      this.$data.selected = selectedtaskid
      this.$data.selectall = false
    },
    handleSelectAll(value) {
      this.$data.selectall = value.length !== 0
    },
    handleFilter() {
      this.callGetTask({}).then(
        data => {
          this.$data.tasklist = data.data.tasklist
          this.$data.taskcolumn = data.data.taskcolumn
          this.$data.total = data.data.total
        }
      )
    },
    tagFilterHandler(value, row, column) {
      if (row.status === value) {
        return true
      }
    },
    callGetTask(data) {
      var keymap = {
        page: this.$data.currentpage,
        size: this.$data.size,
        sort: this.$data.sort,
        desc: this.$data.desc,
        condition: this.$data.listQuery,
        selectall: this.$data.selectall,
        selected: this.$data.selected
      }
      Object.keys(keymap).forEach(k => {
        if (data[k] !== '' && data[k] !== [] && data[k] !== {} && data[k] !== undefined) {
          keymap[k] = data[k]
        }
      })
      return gettask(keymap)
    }
  }
}
</script>
