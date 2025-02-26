<template>
  <div class="mindmap-view">
    <AppHeader />
    
    <div class="content-container">
      <div class="page-header">
        <h1>我的思维导图</h1>
        <button class="btn btn-primary" @click="showCreateModal = true">
          创建新思维导图
        </button>
      </div>
      
      <div class="alert alert-info" v-if="loading">
        加载中...
      </div>
      
      <div class="alert alert-danger" v-if="error">
        {{ error }}
      </div>
      
      <div class="mindmap-grid" v-if="!loading && mindmaps.length > 0">
        <div 
          v-for="mindmap in mindmaps" 
          :key="mindmap.id" 
          class="mindmap-card"
          @click="viewMindMap(mindmap)"
        >
          <div class="mindmap-title">{{ mindmap.title }}</div>
          <div class="mindmap-desc">{{ mindmap.description || '无描述' }}</div>
          <div class="mindmap-date">创建于 {{ formatDate(mindmap.created_at) }}</div>
        </div>
      </div>
      
      <div class="empty-state" v-if="!loading && mindmaps.length === 0">
        <div class="empty-icon">📋</div>
        <h3>暂无思维导图</h3>
        <p>点击上方按钮创建您的第一个思维导图</p>
      </div>
    </div>
    
    <!-- 创建思维导图的模态框 -->
    <div class="modal" v-if="showCreateModal">
      <div class="modal-backdrop" @click="showCreateModal = false"></div>
      <div class="modal-content">
        <h2>创建新思维导图</h2>
        
        <form @submit.prevent="createMindMap">
          <div class="form-group">
            <label for="title">标题</label>
            <input 
              type="text" 
              id="title" 
              v-model="newMindMap.title" 
              class="form-control" 
              required 
              placeholder="请输入标题"
            />
          </div>
          
          <div class="form-group">
            <label for="description">描述</label>
            <textarea 
              id="description" 
              v-model="newMindMap.description" 
              class="form-control" 
              rows="3" 
              placeholder="请输入描述"
            ></textarea>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showCreateModal = false">
              取消
            </button>
            <button type="submit" class="btn btn-primary" :disabled="createLoading">
              {{ createLoading ? '创建中...' : '创建' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import api from '../services/api';

export default {
  name: 'MindMapView',
  components: {
    AppHeader
  },
  data() {
    return {
      mindmaps: [],
      loading: false,
      error: null,
      showCreateModal: false,
      createLoading: false,
      newMindMap: {
        title: '',
        description: '',
        data: {}
      }
    };
  },
  mounted() {
    this.fetchMindMaps();
  },
  methods: {
    async fetchMindMaps() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await api.get('/mindmaps/');
        this.mindmaps = response.data;
      } catch (error) {
        console.error('获取思维导图失败:', error);
        this.error = '获取思维导图失败，请稍后再试';
      } finally {
        this.loading = false;
      }
    },
    
    async createMindMap() {
      if (!this.newMindMap.title) return;
      
      this.createLoading = true;
      
      try {
        const response = await api.post('/mindmaps/', this.newMindMap);
        
        // 重置表单
        this.newMindMap = { title: '', description: '', data: {} };
        this.showCreateModal = false;
        
        // 刷新列表
        this.fetchMindMaps();
      } catch (error) {
        console.error('创建思维导图失败:', error);
        this.error = '创建思维导图失败，请稍后再试';
      } finally {
        this.createLoading = false;
      }
    },
    
    viewMindMap(mindmap) {
      // 跳转到思维导图详情页
      this.$router.push(`/mindmaps/${mindmap.id}`);
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.mindmap-view {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h1 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.btn {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #4a90e2;
  color: white;
}

.btn-primary:hover {
  background-color: #3a80d2;
}

.alert {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.alert-info {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.mindmap-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.mindmap-card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.mindmap-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.mindmap-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
}

.mindmap-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.mindmap-date {
  font-size: 12px;
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
}

.empty-state p {
  color: #666;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  width: 500px;
  max-width: 90%;
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  position: relative;
  z-index: 1001;
}

.modal-content h2 {
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #4a90e2;
  outline: none;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 30px;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
