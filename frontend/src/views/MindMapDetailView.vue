<template>
  <div class="mindmap-detail">
    <AppHeader />
    
    <div class="content-container">
      <div class="page-header">
        <div class="title-section">
          <h1>{{ mindmap.title }}</h1>
          <p class="description">{{ mindmap.description }}</p>
        </div>
        
        <div class="actions">
          <el-button-group>
            <el-button 
              type="primary" 
              :disabled="!isEdited"
              @click="saveMindMap"
            >
              保存更改
            </el-button>
            <el-button @click="$router.push('/mindmaps')">
              返回列表
            </el-button>
          </el-button-group>
        </div>
      </div>
      
      <div class="editor-container">
        <mind-map-editor
          v-if="mindmap.data"
          v-model="mindmap.data"
          @save="handleSave"
          @change="handleChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import MindMapEditor from '../components/MindMapEditor.vue';
import api from '../services/api';

export default {
  name: 'MindMapDetailView',
  components: {
    AppHeader,
    MindMapEditor
  },
  data() {
    return {
      mindmap: {
        title: '',
        description: '',
        data: null
      },
      isEdited: false,
      loading: false,
      error: null
    };
  },
  created() {
    this.fetchMindMap();
  },
  methods: {
    async fetchMindMap() {
      const id = this.$route.params.id;
      
      // 如果没有 ID，说明是创建新思维导图
      if (!id) {
        this.mindmap = {
          title: '新建思维导图',
          description: '',
          data: {
            id: 'root',
            name: '中心主题',
            children: []
          }
        };
        return;
      }
      
      this.loading = true;
      try {
        const response = await api.get(`/mindmaps/${id}`);
        this.mindmap = response.data;
        // 确保data是对象格式
        if (typeof this.mindmap.data === 'string') {
          this.mindmap.data = JSON.parse(this.mindmap.data);
        }
      } catch (error) {
        console.error('获取思维导图失败:', error);
        this.error = '获取思维导图失败，请稍后再试';
      } finally {
        this.loading = false;
      }
    },
    
    handleChange() {
      this.isEdited = true;
    },
    
    async handleSave(data) {
      const id = this.$route.params.id;
      
      try {
        if (id) {
          // 更新已有思维导图
          await api.put(`/mindmaps/${id}`, {
            data: JSON.stringify(data)
          });
        } else {
          // 创建新思维导图
          const response = await api.post('/mindmaps/', {
            title: this.mindmap.title,
            description: this.mindmap.description,
            data: JSON.stringify(data)
          });
          // 创建成功后跳转到编辑页面
          this.$router.replace(`/mindmaps/${response.data.id}`);
        }
        this.isEdited = false;
        this.$message.success('保存成功');
      } catch (error) {
        console.error('保存失败:', error);
        this.$message.error('保存失败，请稍后再试');
      }
    },
    
    async saveMindMap() {
      if (!this.isEdited) return;
      await this.handleSave(this.mindmap.data);
    }
  }
};
</script>

<style scoped>
.mindmap-detail {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.title-section h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.description {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.editor-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  height: calc(100vh - 200px);
  overflow: hidden;
}
</style>