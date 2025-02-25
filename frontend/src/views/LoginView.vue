<template>
  <div class="login-container">
    <div class="login-card">
      <h2>思维导图系统</h2>
      <h3>用户登录</h3>
      
      <div class="alert alert-danger" v-if="error">{{ error }}</div>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            class="form-control" 
            required 
            placeholder="请输入邮箱"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            class="form-control" 
            required 
            placeholder="请输入密码"
          />
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <div class="login-footer">
        <p>还没有账号？ <router-link to="/register">立即注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: null
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;
      
      try {
        // 格式化请求数据为表单格式
        const formData = new FormData();
        formData.append('username', this.email);
        formData.append('password', this.password);
        
        const response = await api.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });
        
        const { access_token } = response.data;
        
        // 保存token到本地
        localStorage.setItem('token', access_token);
        
        // 获取用户信息
        await this.fetchUserInfo();
        
        // 跳转到主页
        this.$router.push('/dashboard');
      } catch (error) {
        console.error('登录失败:', error);
        this.error = error.response?.data?.detail || '登录失败，请检查邮箱和密码';
      } finally {
        this.loading = false;
      }
    },
    async fetchUserInfo() {
      try {
        const response = await api.get('/users/me');
        // 存储用户信息到本地
        localStorage.setItem('user', JSON.stringify(response.data));
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
  padding: 30px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 10px;
}

h3 {
  text-align: center;
  color: #555;
  margin-bottom: 30px;
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
  background-color: #3a80d2;
}

.btn:disabled {
  background-color: #aaaaaa;
  cursor: not-allowed;
}

.login-footer {
  margin-top: 25px;
  text-align: center;
  color: #777;
}

.login-footer a {
  color: #4a90e2;
  text-decoration: none;
}

.alert {
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style> 