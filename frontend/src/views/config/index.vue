<template>
  <div class="app-container">
    <el-card v-for="type in configtype" :key="type" style="margin-bottom: 20px;">
      <div slot="header" class="clearfix">
        <span>{{ type }}配置</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="saveConfig(type)">保存</el-button>
      </div>
      <div>
        <el-collapse accordion>
          <template v-if="type !== 'global'">
            <el-collapse-item v-for="plugin in plugins[type]" :key="plugin.name" :name="plugin.name">
              <template slot="title">
                {{ plugin.name }}
              </template>
              <plugin-config :plugininfo="plugin" :config="getpluginconfig(type, plugin.name)" :stagename="type" @datachanged="pluginConfigUpdate" />
            </el-collapse-item>
          </template>
          <template v-else>
            <el-form ref="form" :model="globalconfig" label-width="80px">
              <el-form-item v-for="key in Object.keys(globalconfig)" :key="key" :label="key">
                <el-input v-model="globalconfig[key]" />
              </el-form-item>
            </el-form>
          </template>
        </el-collapse>
      </div>
    </el-card>
  </div>
</template>
<script>
import { saveconfig, getconfig } from '@/api/config'
import PluginConfig from '@/views/resource/components/PluginConfig.vue'
import { getplugins } from '@/api/plugins'
export default {
  name: 'Config',
  components: {
    PluginConfig
  },
  data() {
    getconfig({ taskid: 'global' }).then(
      data => {
        this.$data.pluginsconfig = data.data.plugins
        this.$data.globalconfig = data.data.global
      }
    ).then(() => {
      getplugins().then(data => {
        this.$data.stage = data.data.stage
        this.$data.stage['global']
        this.$data.plugins = data.data.plugins
        Object.keys(this.$data.stage).forEach(k => {
          this.$data.selectedplugins[k] = []
          this.$data.plugins[k] = this.$data.plugins[k].filter((v) => { if (v['name'] === 'skip') return false; else return true })
        })
      })
    })

    return {
      stage: {},
      plugins: {},
      pluginsconfig: {},
      globalconfig: {},
      selectedplugins: {},
      configtype: ['global', 'info_collect', 'topdomain_collect', 'subdomain_collect', 'ip_info', 'port_detect', 'service_detect', 'fingerprint_detect', 'poc_scan', 'final_step']
    }
  },
  methods: {
    getpluginconfig(stage, plugin) {
      if (stage === 'global') {
        return {}
      } else {
        for (var item of this.pluginsconfig[stage]) {
          if (item.name === plugin) {
            return item.config
          }
        }
      }
      return {}
    },
    pluginConfigUpdate(stagename, plugin, config) {
      this.pluginsconfig[stagename][plugin] = config
    },
    saveConfig(configtype) {
      let promise = null
      if (configtype === 'global') {
        promise = saveconfig({ type: configtype, taskid: 'global', config: this.$data.globalconfig })
      } else {
        promise = saveconfig({ type: configtype, taskid: 'global', config: this.$data.pluginsconfig[configtype] })
      }
      promise.then(
        data => {
          if (data.success) {
            this.$notify.success({
              title: '提示',
              message: '保存成功'
            }
            )
          } else {
            this.$notify.error({
              title: '保存失败',
              message: data.msg
            }
            )
          }
        }
      )
    }
  }
}
</script>
