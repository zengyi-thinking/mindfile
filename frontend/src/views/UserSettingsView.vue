<template>
  <div class="settings-container">
    <h1>用户设置</h1>
    
    <div class="settings-card">
      <form @submit.prevent="saveSettings">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="settings.username" 
            class="form-control" 
            required
          />
        </div>
        
        <div class="form-group">
          <label for="email">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="settings.email" 
            class="form-control" 
            required
          />
        </div>
        
        <div class="form-group">
          <label for="newPassword">新密码 (可选)</label>
          <input 
            type="password" 
            id="newPassword" 
            v-model="settings.newPassword" 
            class="form-control" 
            minlength="6"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">确认新密码</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="settings.confirmPassword" 
            class="form-control" 
            :disabled="!settings.newPassword"
          />
        </div>
        
        <div class="alert alert-success" v-if="successMessage">
          {{ successMessage }}
        </div>
        
        <div class="alert alert-danger" v-if="error">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
          {{ loading ? '保存中...' : '保存设置' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'UserSettingsView',
  data() {
    return {
      settings: {
        username: '',
        email: '',
        newPassword: '',
        confirmPassword: ''
      },
      loading: false,
      error: null,
      successMessage: null
    };
  },
  computed: {
    isFormValid() {
      if (!this.settings.username || !this.settings.email) return false;
      if (this.settings.newPassword) {
        return this.settings.newPassword === this.settings.confirmPassword;
      }
      return true;
    }
  },
  created() {
    this.loadUserSettings();
  },
  methods: {
    async loadUserSettings() {
      try {
        const response = await api.get('/users/me');
        const { username, email } = response.data;
        this.settings.username = username;
        this.settings.email = email;
      } catch (error) {
        console.error('加载用户设置失败:', error);
        this.error = '加载用户设置失败';
      }
    },
    async saveSettings() {
      if (!this.isFormValid) return;
      
      this.loading = true;
      this.error = null;
      this.successMessage = null;
      
      try {
        const updateData = {
          username: this.settings.username,
          email: this.settings.email
        };
        
        if (this.settings.newPassword) {
          updateData.password = this.settings.newPassword;
        }
        
        await api.put('/users/me', updateData);
        
        this.successMessage = '设置已更新';
        this.settings.newPassword = '';
        this.settings.confirmPassword = '';
        
        // 更新本地存储的用户信息
        const userInfo = JSON.parse(localStorage.getItem('user'));
        userInfo.username = this.settings.username;
        userInfo.email = this.settings.email;
        localStorage.setItem('user', JSON.stringify(userInfo));
      } catch (error) {
        console.error('保存设置失败:', error);
        this.error = error.response?.data?.detail || '保存设置失败';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.settings-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 30px;
  color: #333;
}

.settings-card {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
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

.form-control:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #4a90e2;
  color: white;
}

.btn-primary:hover {
  background-color: #357abd;
}

.btn:disabled {
  background-color: #aaaaaa;
  cursor: not-allowed;
}

.alert {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>