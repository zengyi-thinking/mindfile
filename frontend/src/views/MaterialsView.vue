<template>
  <div class="materials-view">
    <AppHeader />
    
    <div class="content-container">
      <div class="page-header">
        <h1>我的资料</h1>
        <button class="btn btn-primary" @click="showCreateModal = true">
          上传新资料
        </button>
      </div>
      
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索资料..." 
          class="search-input"
          @input="searchMaterials"
        />
        
        <div class="filter-options">
          <select v-model="filter.fileType" @change="fetchMaterials">
            <option value="">所有类型</option>
            <option value="text">文本</option>
            <option value="pdf">PDF</option>
            <option value="image">图片</option>
            <option value="other">其他</option>
          </select>
          
          <select v-model="filter.sortBy" @change="fetchMaterials">
            <option value="newest">最新上传</option>
            <option value="popularity">最受欢迎</option>
            <option value="title">按标题</option>
          </select>
        </div>
      </div>
      
      <div class="alert alert-info" v-if="loading">
        加载中...
      </div>
      
      <div class="alert alert-danger" v-if="error">
        {{ error }}
      </div>
      
      <div class="materials-grid" v-if="!loading && materials.length > 0">
        <div 
          v-for="material in materials" 
          :key="material.id" 
          class="material-card"
          @click="viewMaterial(material)"
        >
          <div class="material-icon">
            <span v-if="material.file_type === 'pdf'">📄</span>
            <span v-else-if="material.file_type === 'image'">🖼️</span>
            <span v-else>📝</span>
          </div>
          <div class="material-info">
            <div class="material-title">{{ material.title }}</div>
            <div class="material-desc">{{ material.description || '无描述' }}</div>
            <div class="material-meta">
              <span class="material-date">{{ formatDate(material.created_at) }}</span>
              <span class="material-views">👁️ {{ material.view_count }}</span>
              <span class="material-likes">❤️ {{ material.like_count }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="empty-state" v-if="!loading && materials.length === 0">
        <div class="empty-icon">📚</div>
        <h3>暂无资料</h3>
        <p>点击上方按钮上传您的第一份资料</p>
      </div>
    </div>
    
    <!-- 上传新资料的模态框 -->
    <div class="modal" v-if="showCreateModal">
      <div class="modal-backdrop" @click="showCreateModal = false"></div>
      <div class="modal-content">
        <h2>上传新资料</h2>
        
        <form @submit.prevent="createMaterial">
          <div class="form-group">
            <label for="title">标题</label>
            <input 
              type="text" 
              id="title" 
              v-model="newMaterial.title" 
              class="form-control" 
              required 
              placeholder="请输入标题"
            />
          </div>
          
          <div class="form-group">
            <label for="description">描述</label>
            <textarea 
              id="description" 
              v-model="newMaterial.description" 
              class="form-control" 
              rows="3" 
              placeholder="请输入描述"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="content">内容</label>
            <textarea 
              id="content" 
              v-model="newMaterial.content" 
              class="form-control" 
              rows="5" 
              placeholder="请输入内容或上传文件"
            ></textarea>
          </div>
          
          <div class="form-group">
            <label for="file">上传文件 (可选)</label>
            <input 
              type="file" 
              id="file" 
              ref="fileInput"
              class="form-control" 
            />
          </div>
          
          <div class="form-group">
            <label>
              <input type="checkbox" v-model="newMaterial.is_public" />
              公开此资料
            </label>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showCreateModal = false">
              取消
            </button>
            <button type="submit" class="btn btn-primary" :disabled="createLoading">
              {{ createLoading ? '上传中...' : '上传' }}
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
  name: 'MaterialsView',
  components: {
    AppHeader
  },
  data() {
    return {
      materials: [],
      loading: false,
      error: null,
      searchQuery: '',
      filter: {
        fileType: '',
        sortBy: 'newest'
      },
      showCreateModal: false,
      createLoading: false,
      newMaterial: {
        title: '',
        description: '',
        content: '',
        is_public: false,
        file_type: 'text'
      }
    };
  },
  mounted() {
    this.fetchMaterials();
  },
  methods: {
    async fetchMaterials() {
      this.loading = true;
      this.error = null;
      
      try {
        const params = {
          file_type: this.filter.fileType,
          sort_by: this.filter.sortBy
        };
        
        const response = await api.get('/materials/', { params });
        this.materials = response.data;
      } catch (error) {
        console.error('获取资料失败:', error);
        this.error = '获取资料失败，请稍后再试';
      } finally {
        this.loading = false;
      }
    },
    
    searchMaterials() {
      // 简单的前端搜索
      clearTimeout(this.searchTimer);
      this.searchTimer = setTimeout(() => {
        this.fetchMaterials();
      }, 300);
    },
    
    async createMaterial() {
      if (!this.newMaterial.title) return;
      
      this.createLoading = true;
      
      try {
        // 检查是否有文件上传
        const fileInput = this.$refs.fileInput;
        const file = fileInput && fileInput.files.length > 0 ? fileInput.files[0] : null;
        
        let response;
        
        if (file) {
          // 创建FormData对象用于文件上传
          const formData = new FormData();
          formData.append('file', file);
          formData.append('title', this.newMaterial.title);
          formData.append('description', this.newMaterial.description || '');
          formData.append('is_public', this.newMaterial.is_public);
          
          // 确定文件类型
          if (file.type.includes('pdf')) {
            formData.append('file_type', 'pdf');
          } else if (file.type.includes('image')) {
            formData.append('file_type', 'image');
          } else {
            formData.append('file_type', 'other');
          }
          
          response = await api.post('/materials/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        } else {
          // 无文件上传，直接发送文本内容
          this.newMaterial.file_type = 'text';
          response = await api.post('/materials/', this.newMaterial);
        }
        
        // 重置表单
        this.newMaterial = { 
          title: '', 
          description: '', 
          content: '', 
          is_public: false,
          file_type: 'text'
        };
        if (fileInput) fileInput.value = '';
        this.showCreateModal = false;
        
        // 刷新列表
        this.fetchMaterials();
      } catch (error) {
        console.error('创建资料失败:', error);
        this.error = '创建资料失败，请稍后再试';
      } finally {
        this.createLoading = false;
      }
    },
    
    viewMaterial(material) {
      // 跳转到资料详情页
      this.$router.push(`/materials/${material.id}`);
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.materials-view {
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
  margin-bottom: 20px;
}

h1 {
  font-size: 24px;
  color: #333;
  margin: 0;
}

.search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.search-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.filter-options {
  display: flex;
  gap: 10px;
  margin-left: 10px;
}

.filter-options select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.materials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.material-card {
  display: flex;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.material-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.material-icon {
  font-size: 24px;
  margin-right: 15px;
}

.material-info {
  flex: 1;
}

.material-title {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
}

.material-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.material-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #999;
}

.btn, .alert, .empty-state, .modal, .modal-backdrop, .modal-content,
.form-group, label, .form-control, .modal-footer, .btn-secondary {
  /* 样式与之前的MindMapView组件相同，这里省略重复代码 */
}
</style> 