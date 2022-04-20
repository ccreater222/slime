<template>
  <div class="app-container">
    搜索|选择
    操作
    <div class="filter-container">
      <el-input v-model="listQuery.title" placeholder="Title" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.importance" placeholder="字段一" clearable style="width: 90px" class="filter-item">
        <el-option v-for="item in defaultFormThead" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="listQuery.type" placeholder="字段二" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in defaultFormThead" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select>
      <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in defaultFormThead" :key="item.key" :label="item.label" :value="item.key" />
      </el-select>
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Search
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        Export
      </el-button>
    </div>
    <div class="action-container">
      <el-button type="primary">占位</el-button>
    </div>
    <div class="filter-container">
      <el-checkbox-group v-model="checkboxVal">
        <el-checkbox v-for="item in defaultFormThead" :key="item" :label="item">
          {{ item }}
        </el-checkbox>
      </el-checkbox-group>
    </div>
    <el-table :key="key" :data="tableData" border fit highlight-current-row style="width: 100%">
      <el-table-column prop="name" label="columeName" width="180" />
      <el-table-column v-for="colume in formThead" :key="colume" :label="colume">
        <template slot-scope="scope">
          {{ scope.row[colume] }}
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      :current-page="currentPage4"
      :page-sizes="[100, 200, 300, 400]"
      :page-size="100"
      layout="total, sizes, prev, pager, next, jumper"
      :total="400"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
const defaultFormThead = ['apple', 'banana', 'orange']
export default {
  data() {
    return {
      tableData: [
        {
          name: 'colume-1',
          apple: 'apple-1',
          banana: 'banana-10',
          orange: 'orange-10'
        },
        {
          name: 'colume-2',
          apple: 'apple-20',
          banana: 'banana-20',
          orange: 'orange-20'
        }
      ],
      key: 1,
      formTheadOptions: ['apple', 'banana', 'orange'],
      defaultFormThead: defaultFormThead,
      checkboxVal: defaultFormThead,
      formThead: defaultFormThead,
      listQuery: {}
    }
  },
  watch: {
    checkboxVal(valArr) {
      this.formThead = this.formTheadOptions.filter(i => valArr.indexOf(i) >= 0)
      this.key = this.key + 1
    }
  }
}
</script>

<style scoped>

</style>
