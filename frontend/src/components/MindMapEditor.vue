<template>
  <div class="mindmap-editor">
    <div class="editor-toolbar">
      <el-button-group>
        <el-button size="small" @click="importMindMap">
          <i class="el-icon-upload2"></i> 导入
        </el-button>
        <el-button size="small" @click="exportMindMap">
          <i class="el-icon-download"></i> 导出
        </el-button>
        <el-button size="small" @click="saveMindMap">
          <i class="el-icon-document-checked"></i> 保存
        </el-button>
      </el-button-group>
    </div>

    <div class="editor-container" ref="editorContainer"></div>

    <input
      type="file"
      ref="fileInput"
      style="display: none"
      accept=".mmap,.xmind"
      @change="handleFileImport"
    />
  </div>
</template>

<script>
import * as d3 from 'd3';
import { saveAs } from 'file-saver';

export default {
  name: 'MindMapEditor',
  props: {
    value: {
      type: Object,
      required: true
    },
    readOnly: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      editor: null,
      mindMapData: null
    };
  },
  mounted() {
    this.initEditor();
    if (this.value) {
      this.loadMindMapData(this.value);
    }
  },
  methods: {
    initEditor() {
      const width = this.$refs.editorContainer.clientWidth;
      const height = this.$refs.editorContainer.clientHeight;

      const svg = d3.select(this.$refs.editorContainer)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      this.editor = svg;
    },

    loadMindMapData(data) {
      this.mindMapData = data;
      this.renderMindMap();
    },

    renderMindMap() {
      if (!this.mindMapData) return;

      // 使用D3.js渲染思维导图
      const root = d3.hierarchy(this.mindMapData);
      const treeLayout = d3.tree().size([800, 600]);
      const nodes = treeLayout(root);

      // 清除现有内容
      this.editor.selectAll('*').remove();

      // 绘制连接线
      this.editor.selectAll('path')
        .data(nodes.links())
        .enter()
        .append('path')
        .attr('d', d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x))
        .attr('fill', 'none')
        .attr('stroke', '#ccc');

      // 绘制节点
      const node = this.editor.selectAll('g')
        .data(nodes.descendants())
        .enter()
        .append('g')
        .attr('transform', d => `translate(${d.y},${d.x})`);

      node.append('circle')
        .attr('r', 5)
        .attr('fill', '#fff')
        .attr('stroke', '#666');

      node.append('text')
        .attr('dy', '0.31em')
        .attr('x', d => d.children ? -6 : 6)
        .attr('text-anchor', d => d.children ? 'end' : 'start')
        .text(d => d.data.name);
    },

    importMindMap() {
      this.$refs.fileInput.click();
    },

    async handleFileImport(event) {
      const file = event.target.files[0];
      if (!file) return;

      try {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const content = e.target.result;
          // 解析.mmap或.xmind文件
          const data = await this.parseMindMapFile(content, file.name);
          this.loadMindMapData(data);
          this.$emit('input', data);
        };
        reader.readAsArrayBuffer(file);
      } catch (error) {
        this.$message.error('导入失败：' + error.message);
      }
    },

    async parseMindMapFile(content, filename) {
      // 根据文件扩展名选择解析方法
      const ext = filename.split('.').pop().toLowerCase();
      if (ext === 'mmap') {
        return this.parseMmapFile(content);
      } else if (ext === 'xmind') {
        return this.parseXmindFile(content);
      }
      throw new Error('不支持的文件格式');
    },

    async parseMmapFile(content) {
      // 实现.mmap文件解析逻辑
      // 这里需要根据.mmap文件格式规范实现具体的解析逻辑
      return {
        name: '根节点',
        children: []
      };
    },

    async parseXmindFile(content) {
      // 实现.xmind文件解析逻辑
      return {
        name: '根节点',
        children: []
      };
    },

    exportMindMap() {
      if (!this.mindMapData) return;

      try {
        // 将思维导图数据转换为.mmap格式
        const mmapContent = this.convertToMmapFormat(this.mindMapData);
        const blob = new Blob([mmapContent], { type: 'application/octet-stream' });
        saveAs(blob, 'mindmap.mmap');
      } catch (error) {
        this.$message.error('导出失败：' + error.message);
      }
    },

    convertToMmapFormat(data) {
      // 实现将数据转换为.mmap格式的逻辑
      // 这里需要根据.mmap文件格式规范实现具体的转换逻辑
      return JSON.stringify(data);
    },

    saveMindMap() {
      if (!this.mindMapData) return;
      this.$emit('save', this.mindMapData);
    }
  }
};
</script>

<style scoped>
.mindmap-editor {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-toolbar {
  padding: 8px;
  border-bottom: 1px solid #eee;
}

.editor-container {
  flex: 1;
  overflow: auto;
  background-color: #fff;
}
</style>