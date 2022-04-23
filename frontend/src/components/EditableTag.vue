<template>
  <div>
    <el-tag
      v-for="tag in dynamicTags"
      :key="tag"
      closable
      :disable-transitions="false"
      @close="handleClose(tag)"
    >
      {{ tag }}
    </el-tag>
    <el-input
      v-if="inputVisible"
      ref="saveTagInput"
      v-model="inputValue"
      class="input-new-tag"
      size="mini"
      @keyup.enter.native="handleInputConfirm"
      @blur="handleInputConfirm"
    />
    <el-button v-else class="button-new-tag" size="mini" @click="showInput">+ New {{ upperFirst(tagName) }}</el-button>
  </div>
</template>
<style>
  .el-tag + .el-tag {
    margin-left: 10px;
  }
  .button-new-tag {
    margin-left: 10px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
  }
  .input-new-tag {
    width: 90px;
    margin-left: 10px;
    vertical-align: bottom;
  }
</style>

<script>
export default {
  props: {
    dynamicTags: {
      type: Array,
      required: true
    },
    tagName: {
      type: String,
      default: 'Tag'
    }
  },
  data() {
    return {
      inputVisible: false,
      inputValue: ''
    }
  },
  methods: {
    upperFirst(word) {
      return word[0].toUpperCase() + word.slice(1)
    },
    updateTag() {
      this.$emit('updatetag', this.tagName, this.dynamicTags)
    },
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
      this.updateTag()
    },

    showInput() {
      this.inputVisible = true
      this.$nextTick(_ => {
        this.$refs.saveTagInput.$refs.input.focus()
      })
    },

    handleInputConfirm() {
      const inputValue = this.inputValue
      if (inputValue) {
        this.dynamicTags.push(inputValue)
        this.updateTag()
      }
      this.inputVisible = false
      this.inputValue = ''
    }
  }
}
</script>
