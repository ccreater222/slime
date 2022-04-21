<template>
  <div class="app-container">
    <el-divider><i class="el-icon-search" /></el-divider>
    <div class="filter-container">
      <el-row :gutter="20" justify="center">
        <el-col v-for="col in defaultFormThead" :key="col" :span="2">
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
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-plus" @click="handleCreate">
        添加
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-edit" @click="handleEdit">
        修改
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-delete" @click="handleDelete">
        删除
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-odometer" @click="handleTask">
        发布任务
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-s-data" @click="handleAnalyze">
        统计信息
      </el-button>
      <el-button v-waves class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-refresh-left" @click="handleReset">
        重置
      </el-button>
      <el-button v-waves class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-download" @click="handleDownload">
        导出
      </el-button>
      <el-upload accept=".json" class="filter-item" type="primary" style="margin-right: 10px; margin-left: 10px; " action="/api/create/resource" :show-file-list="false" :before-upload="handleImport">
        <el-button
          v-waves
          type="primary"
          icon="el-icon-upload"
        >
          导入
        </el-button>
      </el-upload>

    </div>
    <el-divider><i class="el-icon-s-management" /></el-divider>
    <div class="filter-container">
      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox v-for="item in defaultFormThead" :key="item" :label="item" :disabled="constcol.indexOf(item)!==-1">
          {{ item }}
        </el-checkbox>
      </el-checkbox-group>
    </div>
    <el-table :key="key" :data="tableData" fit highlight-current-row style="width: 100%" @select="handleSelect" @select-all="handleSelectAll" @sort-change="sortHandler">
      <el-table-column
        type="selection"
        width="55"
      />
      <el-table-column v-for="colume in formThead" :key="colume" :label="colume" sortable="custom">
        <template slot-scope="scope">
          <el-tag
            v-for="tag in (scope.row[colume] instanceof Array)?scope.row[colume]:[]"
            :key="tag+colume"
            type="primary"
            size="mini"
            disable-transitions
          >
            {{ tag }}
          </el-tag>
          {{ !(scope.row[colume] instanceof Array)?scope.row[colume]:"" }}
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="success"
            @click="handlePerEdit(scope.$index, scope.row)"
          >编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handlePerDelete(scope.$index, scope.row)"
          >删除</el-button>
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
    <el-dialog title="导出" :visible.sync="downloadDialogFormVisible">
      <el-form label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="数据格式">
          <el-radio-group v-model="downloadformat">
            <el-radio label="csv" />
            <el-radio label="txt" />
            <el-radio label="json" />
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="downloadDialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="downloadAction">
          确认
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="dataDialogFormVisible" :title="isupdate?'修改':'添加'">
      <el-form :model="temp" label-position="left" label-width="auto" style="margin-left:50px;">
        <el-form-item v-for="item in editablecol" :key="item" :label="item">
          <el-input v-model="temp[item]" placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dataDialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="isupdate?updateData():createData()">
          确认
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="analyzeDialogFormVisible" title="统计信息">
      <el-tabs tab-position="left" style="height: 500px;" @tab-click="analyzeTabClicked">
        <el-tab-pane label="IP RANGE">
          <analyze-template height="500px" :keyword="'IP RANGE'" :chart-data-promise="analyzedata('cidr',500)" />
        </el-tab-pane>
        <el-tab-pane label="Tags">
          <analyze-template height="500px" :keyword="'TAGS'" :chart-data-promise="analyzedata('tags', 500)" />
        </el-tab-pane>
        <el-tab-pane label="Services">
          <analyze-template height="500px" :keyword="'SERVICES'" :chart-data-promise="analyzedata('services',500)" />
        </el-tab-pane>
        <el-tab-pane label="Fingerprints">
          <analyze-template height="500px" :keyword="'FINGERPRINTS'" :chart-data-promise="analyzedata('fingerprints',500)" />
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
    <el-dialog :visible.sync="taskDialogFormVisible" title="发布任务">
      test
    </el-dialog>
  </div>
</template>

<script>
import { updateresource, getresource, createresource, deleteresource, analyzeresource } from '@/api/resource'
import waves from '@/directive/waves/index.js'
import AnalyzeTemplate from './components/AnalyzeTemplate.vue'
import { saveAs } from 'file-saver'
const deepcopy = require('deepcopy')

var defaultFormThead
export default {
  directives: {
    waves
  },
  components: {
    AnalyzeTemplate
  },
  data() {
    getresource({ page: 1 }).then(
      data => {
        defaultFormThead = data.data.columes
        this.$data.defaultFormThead = defaultFormThead
        this.$data.checkboxVal = defaultFormThead
        this.$data.formThead = defaultFormThead
        this.$data.formTheadOptions = defaultFormThead
        this.$data.tableData = data.data.columedatas
        this.$data.total = data.total
      }
    )

    return {
      tableData: [],
      key: 1,
      formTheadOptions: [],
      defaultFormThead: [],
      checkboxVal: [],
      formThead: [],
      listQuery: {},
      currentpage: 1,
      size: 20,
      total: 0,
      selected: [],
      selectall: false,
      constcol: ['name', 'id'],
      downloadDialogFormVisible: false,
      downloadformat: 'json',
      isupdate: false,
      dataDialogFormVisible: false,
      temp: {},
      disableEditCol: ['updated', 'created', 'id'],
      sort: '',
      desc: false,
      analyzeDialogFormVisible: false,
      taskDialogFormVisible: false
    }
  },
  computed: {
    editablecol: function() {
      var result = []
      this.$data.checkboxVal.forEach(v => {
        if (this.$data.disableEditCol.indexOf(v) === -1) {
          result.push(v)
        }
      })
      return result
    }
  },
  watch: {
    checkboxVal(valArr) {
      // TODO: unique value for smallest value
      this.callGetResource({}).then(data => {
        this.$data.tableData = data.data.columedatas
        this.formThead = this.formTheadOptions.filter(i => valArr.indexOf(i) >= 0)
        this.key = this.key + 1
      })
    }
  },
  methods: {
    handleTask: function() {
      this.taskDialogFormVisible = true
    },
    handleSizeChange: function(size) {
      this.$data.size = size
      this.callGetResource({}).then(data => {
        this.$data.tableData = data.data.columedatas
      })
    },
    handleCurrentChange: function(page) {
      this.$data.currentpage = page
      this.callGetResource({}).then(data => {
        this.$data.tableData = data.data.columedatas
      })
    },
    handleFilter: function(value) {
      this.refresh()
    },
    handleCreate: function() {
      this.$data.isupdate = false
      this.$data.temp = {}
      this.$data.dataDialogFormVisible = true
    },
    handleDownload: function(value) {
      this.$data.downloadDialogFormVisible = true
    },
    handleSelect: function(value) {
      this.$data.selected = value
      this.$data.selectall = false
    },
    handleSelectAll: function(value) {
      this.$data.selectall = value.length !== 0
    },
    handleReset: function() {
      this.$data.listQuery = {}
    },
    handleEdit: function() {
      this.$data.isupdate = true
      if (this.$data.selected.length !== 1) {
        this.$notify.error({
          title: '错误',
          message: '必须选中一条记录修改'
        })
        return
      }

      this.$data.temp = deepcopy(this.$data.selected[0])
      this.$data.dataDialogFormVisible = true
    },
    downloadAction: function() {
      let downloaddata = []
      if (this.$data.selected.length > 0 && this.$data.selectall === false) {
        downloaddata = this.$data.selected
        this.download(downloaddata)
        this.$data.downloadDialogFormVisible = false
      } else {
        this.callGetResource({})
          .then(data => {
            this.download(data.data.columedatas)
            this.$data.downloadDialogFormVisible = false
          })
      }
    },
    download: function(downloaddata) {
      if (downloaddata.length === 0) {
        return
      }
      var data = ''
      if (this.$data.downloadformat === 'json') {
        data = JSON.stringify(downloaddata)
      } else if (this.$data.downloadformat === 'txt') {
        downloaddata.forEach(v => {
          var keys = Object.keys(v)
          keys.forEach(k => {
            data += v[k] + ' '
          })
          data += '\n'
        })
      } else if (this.$data.downloadformat === 'csv') {
        downloaddata.push(Object.keys(downloaddata[0]))
        downloaddata.forEach(v => {
          var keys = Object.keys(v)
          keys.forEach(k => {
            data += v[k] + ','
          })
          data += '\n'
        })
      }
      if (data !== '') {
        var blob = new Blob([data], {
          type: 'text/plain'
        })
        saveAs(blob, `export.${this.$data.downloadformat}`)
      }
    },
    updateData: function() {
      updateresource({
        columes: this.$data.checkboxVal,
        page: this.$data.currentpage,
        size: this.$data.size,
        condition: this.$data.listQuery,
        selectall: this.$data.selectall,
        selected: this.$data.selected,
        data: this.$data.temp
      }).then(data => {
        if (data.success) {
          this.$notify({
            title: '成功',
            message: '修改成功',
            type: 'success'
          })
        } else {
          this.$notify({
            title: '失败',
            message: data.msg,
            type: 'error'
          })
        }

        this.$data.dataDialogFormVisible = false
      }).catch((e) => {
        this.$notify.error({
          title: '错误',
          message: '修改失败'
        })
      })
    },
    createData: function() {
      createresource(this.temp).then(data => {
        if (data.success) {
          this.$notify({
            title: '成功',
            message: '添加成功',
            type: 'success'
          })
        } else {
          this.$notify({
            title: '失败',
            message: data.msg,
            type: 'error'
          })
        }
        this.$data.dataDialogFormVisible = false
      }).catch(e => {
        this.$notify({
          title: '失败',
          message: e,
          type: 'error'
        })
      })
    },
    handleImport: function(file) {
      file.text().then(data => {
        data = JSON.parse(data)
        return createresource(data)
      }).then(data => {
        if (data.success) {
          this.$notify({
            title: '成功',
            message: '导入成功',
            type: 'success'
          })
          this.refresh()
        } else {
          this.$notify({
            title: '失败',
            message: '导入失败: ' + data.msg,
            type: 'error'
          })
        }
      })
        .catch(e => {
          this.$notify(
            {
              title: '失败',
              message: e,
              type: 'error'
            }
          )
        })
      return false
    },
    refresh: function() {
      this.callGetResource({}).then(data => {
        this.$data.tableData = data.data.columedatas
        // this.key = this.key + 1
      })
    },
    callGetResource: function(data) {
      var keymap = {
        columes: this.$data.checkboxVal,
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
      return getresource(keymap)
    },
    handleDelete: function() {
      this.$confirm('确认删除', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteresource({
          columes: this.$data.checkboxVal,
          page: this.$data.currentpage,
          size: this.$data.size,
          sort: this.$data.sort,
          desc: this.$data.desc,
          condition: this.$data.listQuery,
          selectall: this.$data.selectall,
          selected: this.$data.selected
        }).then(data => {
          this.$notify({
            type: 'success',
            message: '删除成功!',
            title: '提示'
          })
        })
      }).catch(() => {
        this.$notify({
          type: 'info',
          message: '已取消删除',
          title: '提示'
        })
      })
    },
    sortHandler: function(data) {
      this.$data.sort = data.column.label
      this.$data.desc = data.order === 'descending'
      this.refresh()
    },
    handlePerEdit: function(index, row) {
      this.$data.temp = row
      this.$data.isupdate = true
      this.$data.dataDialogFormVisible = true
    },
    handlePerDelete: function(index, row) {
      this.$confirm('确认删除', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteresource({
          columes: this.$data.checkboxVal,
          page: this.$data.currentpage,
          size: this.$data.size,
          sort: this.$data.sort,
          desc: this.$data.desc,
          condition: this.$data.listQuery,
          selectall: false,
          selected: [row]
        }).then(data => {
          this.$notify({
            type: 'success',
            message: '删除成功!',
            title: '提示'
          })
        })
      }).catch(() => {
        this.$notify({
          type: 'info',
          message: '已取消删除',
          title: '提示'
        })
      })
    },
    handleAnalyze: function() {
      this.$data.analyzeDialogFormVisible = true
    },
    analyzedata: function(target, limit) {
      var data = {
        columes: this.$data.checkboxVal,
        page: this.$data.currentpage,
        size: this.$data.size,
        sort: this.$data.sort,
        desc: this.$data.desc,
        condition: this.$data.listQuery,
        selectall: this.$data.selectall,
        selected: this.$data.selected,
        target: target,
        limit
      }
      return analyzeresource(data)
    },
    analyzeTabClicked: function(tab, event) {
      console.log('clicked')
      this.$nextTick(() => {
        tab.$children[0].resize()
      })
    }
  }
}
</script>

<style scoped>

</style>
