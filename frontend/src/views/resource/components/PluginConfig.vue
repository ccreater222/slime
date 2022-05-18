<template>
  <el-form ref="form" :model="config" label-width="80px">
    <el-form-item v-for="key in plugininfo.config" :key="key">
      <el-row>
        <el-col :span="4">
          <div style="text-overflow: ellipsis;" :content="key"> {{ key }} </div>
        </el-col>
        <el-col :span="20">
          <el-input v-model="config[key]" @input="inputHandler" />
        </el-col>
      </el-row>
    </el-form-item>
  </el-form>
</template>
<script>
export default {
  props: {
    plugininfo: {
      type: Object,
      required: true
    },
    stagename: {
      type: String,
      required: true
    },
    config: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  data() {
    var config = {}
    this.plugininfo.config.forEach(k => {
      if (config[k] === undefined) { config[k] = '' }
    })
    return {
    }
  },
  methods: {
    inputHandler(v) {
      this.$emit('datachanged', this.stagename, this.plugininfo.name, this.config)
    }
  }
}
</script>
