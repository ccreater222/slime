<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { getresource } from '@/api/resource'
getresource({
  'colume': [], // 空的话代表所有字段
  'page': 1,
  'size': 10,
  'sort': '', // 空为不排序
  'desc': true,
  'condition': {

  }
})
export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
