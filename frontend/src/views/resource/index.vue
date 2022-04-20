<template>
  <div class="app-container">
    <el-divider><i class="el-icon-search" /></el-divider>
    <div class="filter-container">
      <el-row :gutter="20" justify="center">
        <el-col v-for="col in defaultFormThead" :key="col" :span="2">
          <el-input v-model="listQuery[col]" :placeholder="col" prefix-icon="el-icon-search" class="filter-item" @keyup.enter.native="handleFilter" />
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
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-delete" @click="handleCreate">
        删除
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-odometer" @click="handleCreate">
        发布任务
      </el-button>
      <el-button class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-s-data" @click="handleCreate">
        统计信息
      </el-button>
      <el-button v-waves class="filter-item" style="margin-right: 10px;" type="primary" icon="el-icon-refresh-left" @click="handleReset">
        重置
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        导出
      </el-button>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-upload" @click="handleImport">
        导入
      </el-button>

    </div>
    <el-divider><i class="el-icon-s-management" /></el-divider>
    <div class="filter-container">
      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox v-for="item in defaultFormThead" :key="item" :label="item" :disabled="constcol.indexOf(item)!==-1">
          {{ item }}
        </el-checkbox>
      </el-checkbox-group>
    </div>
    <el-table :key="key" :data="tableData" fit highlight-current-row style="width: 100%" @select="handleSelect" @select-all="handleSelectAll">
      <el-table-column
        type="selection"
        width="55"
      />
      <el-table-column v-for="colume in formThead" :key="colume" :label="colume">
        <template slot-scope="scope">
          {{ scope.row[colume] }}
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
  </div>
</template>

<script>
import { getresource } from '@/api/resource'
import waves from '@/directive/waves/index.js'
import { saveAs } from 'file-saver'
var defaultFormThead
export default {
  directives: {
    waves
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
      constcol: ['name'],
      downloadDialogFormVisible: false,
      downloadformat: 'json',
      isupdate: false,
      dataDialogFormVisible: false,
      temp: {},
      disableEditCol: ['updated', 'created']
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
      getresource({ size: this.$data.size, page: this.$data.page, columes: this.$data.columes }).then(data => {
        this.$data.tableData = data.data.columedatas
        this.formThead = this.formTheadOptions.filter(i => valArr.indexOf(i) >= 0)
        this.key = this.key + 1
      })
    }
  },
  methods: {
    handleSizeChange: function(size) {
      this.$data.size = size
      getresource({ size, page: this.$data.currentpage }).then(data => {
        this.$data.tableData = data.data.columedatas
      })
    },
    handleCurrentChange: function(page) {
      this.$data.currentpage = page
      getresource({ size: this.$data.size, page }).then(data => {
        this.$data.tableData = data.data.columedatas
      })
    },
    handleFilter: function(value) {
      return
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
      this.$data.temp = this.$data.selected[0]
      this.$data.dataDialogFormVisible = true
    },
    downloadAction: function() {
      let downloaddata = []
      if (this.$data.selected.length > 0 && this.$data.selectall === false) {
        downloaddata = this.$data.selected
        this.download(downloaddata)
        this.$data.downloadDialogFormVisible = false
      } else {
        getresource({ selectall: this.$data.selectall, condition: this.$data.listQuery })
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
      this.$data.dataDialogFormVisible = false
    },
    createData: function() {
      this.$data.dataDialogFormVisible = false
    },
    handleImport: function() {
      return
    }
  }
}
</script>

<style scoped>

</style>
