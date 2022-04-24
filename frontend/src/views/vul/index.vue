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
    <div class="filter-container">
      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox v-for="item in defaultFormThead" :key="item" :label="item" :disabled="constcol.indexOf(item)!==-1">
          {{ item }}
        </el-checkbox>
      </el-checkbox-group>
    </div>
    <el-table :key="key" :data="tableData" fit highlight-curconst @sort-change="sortHandler">
      <el-table-column type="expand">
        <template slot-scope="scope">
          <el-form label-position="left" label-width="auto">
            <el-form-item v-for="column in formThead" :key="column" style="margin-bottom: 0px;" :label="column">
              <el-input
                v-if="(typeof scope.row[column]) !== 'object'"
                type="textarea"
                autosize
                readonly
                :value="scope.row[column].toString()"
              />
              <el-tag
                v-for="tag in (scope.row[column] instanceof Array)?scope.row[column]:[]"
                :key="tag+column"
                type="primary"
                size="mini"
                disable-transitions
              >
                {{ tag }}
              </el-tag>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column v-for="column in formThead" :key="column" :label="column" sortable="custom" :show-overflow-tooltip="true">
        <template slot-scope="scope">
          <el-tag
            v-for="tag in (scope.row[column] instanceof Array)?scope.row[column]:[]"
            :key="tag+column"
            type="primary"
            size="mini"
            disable-transitions
          >
            {{ tag }}
          </el-tag>
          {{ !(scope.row[column] instanceof Array)?scope.row[column]:"" }}
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
import { getvul } from '@/api/vul'
import waves from '@/directive/waves/index.js'
export default {
  name: 'VUL',
  directives: {
    waves
  },
  data() {
    var defaultFormThead = ['ip', 'port', 'subdomain', 'topdomain', 'name', 'title', 'type', 'plugin', 'info', 'req', 'resp', 'tag', 'created']
    getvul({ page: 1, size: 20 }).then(
      data => {
        this.$data.tableData = data.data
        this.$data.total = data.total
      }
    )

    return {
      tableData: [],
      key: 1,
      formTheadOptions: defaultFormThead,
      defaultFormThead,
      checkboxVal: defaultFormThead,
      formThead: defaultFormThead,
      listQuery: {},
      currentpage: 1,
      size: 20,
      total: 0,
      constcol: ['name'],
      sort: '',
      desc: false
    }
  },
  watch: {
    checkboxVal(valArr) {
      this.callGetVul({}).then(data => {
        this.$data.tableData = data.data
        this.formThead = this.formTheadOptions.filter(i => valArr.indexOf(i) >= 0)
        this.key = this.key + 1
      })
    }
  },
  methods: {
    handleReset() {
      this.listQuery = {}
    },
    callGetVul(data) {
      var keymap = {
        columns: this.$data.checkboxVal,
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
      return getvul(keymap)
    },
    sortHandler: function(data) {
      this.$data.sort = data.column.label
      this.$data.desc = data.order === 'descending'
      this.refresh()
    },
    handleSizeChange: function(size) {
      this.$data.size = size
      this.callGetVul({}).then(data => {
        this.$data.tableData = data.data
      })
    },
    handleCurrentChange: function(page) {
      this.$data.currentpage = page
      this.callGetVul({}).then(data => {
        this.$data.tableData = data.data
      })
    },
    refresh: function() {
      this.callGetVul({}).then(data => {
        this.$data.tableData = data.data
        // this.key = this.key + 1
      })
    },
    handleFilter: function(value) {
      this.refresh()
    }
  }
}
</script>
