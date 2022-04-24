<template>
  <el-form ref="form" :model="config" label-width="80px">
    <el-form-item v-for="key in Object.keys(config)" :key="key" :label="key">
      <el-input v-model="config[key]" @input="inputHandler" />
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
      default() {
        return {}
      }
    }
  },
  data() {
    this.plugininfo.config.forEach(k => {
      if (this.config[k] === undefined) {
        this.config[k] = ''
      }
    }
    )

    return {}
  },
  methods: {
    inputHandler(v) {
      this.$emit('datachanged', this.stagename, this.plugininfo.name, this.config)
    }
  }
}
</script>
