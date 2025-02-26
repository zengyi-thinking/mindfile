<template>
  <div class="mindmap-editor">
    <AppHeader />
    
    <div class="editor-container">
      <div class="toolbar">
        <button class="btn" @click="addNode"><i class="fas fa-plus"></i> 添加节点</button>
        <button class="btn" @click="deleteNode"><i class="fas fa-trash"></i> 删除节点</button>
        <button class="btn" @click="saveMindmap"><i class="fas fa-save"></i> 保存</button>
        <button class="btn" @click="exportMindmap"><i class="fas fa-download"></i> 导出</button>
      </div>
      
      <div class="mindmap-canvas" ref="canvas">
        <!-- 思维导图渲染区域 -->
      </div>
      
      <div class="properties-panel" v-if="selectedNode">
        <h3>节点属性</h3>
        <div class="form-group">
          <label>标题</label>
          <input type="text" v-model="selectedNode.title" @input="updateNode">
        </div>
        <div class="form-group">
          <label>描述</label>
          <textarea v-model="selectedNode.description" @input="updateNode"></textarea>
        </div>
        <div class="form-group">
          <label>标签</label>
          <select multiple v-model="selectedNode.tags" @change="updateNode">
            <option v-for="tag in tags" :key="tag.id" :value="tag.id">
              {{ tag.name }}
            </option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { mindmapService } from '@/services/mindmap';
import AppHeader from '@/components/AppHeader.vue';

export default {
  name: 'MindMapEditor',
  components: { AppHeader },
  
  setup() {
    const route = useRoute();
    const router = useRouter();
    const canvas = ref(null);
    const mindmapData = reactive({
      nodes: [],
      edges: []
    });
    const selectedNode = ref(null);
    const tags = ref([]);
    
    // 初始化思维导图
    const initMindmap = async () => {
      if (route.params.id) {
        try {
          const data = await mindmapService.getMindmap(route.params.id);
          mindmapData.nodes = data.nodes;
          mindmapData.edges = data.edges;
          renderMindmap();
        } catch (error) {
          console.error('加载思维导图失败:', error);
        }
      }
    };
    
    // 渲染思维导图
    const renderMindmap = () => {
      // TODO: 使用可视化库渲染思维导图
      // 例如：使用 G6、D3.js 等库实现
    };
    
    // 添加节点
    const addNode = () => {
      const newNode = {
        id: Date.now().toString(),
        title: '新节点',
        description: '',
        tags: []
      };
      mindmapData.nodes.push(newNode);
      renderMindmap();
    };
    
    // 删除节点
    const deleteNode = () => {
      if (selectedNode.value) {
        const index = mindmapData.nodes.findIndex(n => n.id === selectedNode.value.id);
        if (index > -1) {
          mindmapData.nodes.splice(index, 1);
          // 同时删除相关的边
          mindmapData.edges = mindmapData.edges.filter(
            e => e.source !== selectedNode.value.id && e.target !== selectedNode.value.id
          );
          selectedNode.value = null;
          renderMindmap();
        }
      }
    };
    
    // 更新节点
    const updateNode = () => {
      if (selectedNode.value) {
        const index = mindmapData.nodes.findIndex(n => n.id === selectedNode.value.id);
        if (index > -1) {
          mindmapData.nodes[index] = { ...selectedNode.value };
          renderMindmap();
        }
      }
    };
    
    // 保存思维导图
    const saveMindmap = async () => {
      try {
        const data = {
          nodes: mindmapData.nodes,
          edges: mindmapData.edges
        };
        if (route.params.id) {
          await mindmapService.updateMindmap(route.params.id, data);
        } else {
          await mindmapService.createMindmap(data);
        }
        router.push('/mindmaps');
      } catch (error) {
        console.error('保存思维导图失败:', error);
      }
    };
    
    // 导出思维导图
    const exportMindmap = async () => {
      try {
        const blob = await mindmapService.exportMindmap(route.params.id);
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mindmap-${route.params.id}.mmap`;
        a.click();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('导出思维导图失败:', error);
      }
    };
    
    onMounted(() => {
      initMindmap();
    });
    
    return {
      canvas,
      selectedNode,
      tags,
      addNode,
      deleteNode,
      updateNode,
      saveMindmap,
      exportMindmap
    };
  }
};
</script>

<style scoped>
.mindmap-editor {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.editor-container {
  flex: 1;
  display: flex;
  padding: 20px;
}

.toolbar {
  position: fixed;
  top: 80px;
  left: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mindmap-canvas {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin: 0 20px;
}

.properties-panel {
  width: 300px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 4px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn {
  padding: 8px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.btn:hover {
  background: #45a049;
}
</style>