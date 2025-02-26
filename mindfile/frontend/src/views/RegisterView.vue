<template>
  <div class="register-container">
    <div class="register-card">
      <h2>思维导图系统</h2>
      <h3>用户注册</h3>
      
      <div class="alert alert-danger" v-if="error">{{ error }}</div>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            class="form-control" 
            required 
            placeholder="请输入用户名"
          />
        </div>
        
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
            placeholder="请输入密码 (至少6位)"
            minlength="6"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input 
            type="password" 
            id="confirmPassword" 
            v-model="confirmPassword" 
            class="form-control" 
            required 
            placeholder="请再次输入密码"
          />
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      
      <div class="register-footer">
        <p>已有账号？ <router-link to="/login">登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false,
      error: null
    };
  },
  computed: {
    isFormValid() {
      return this.username && 
        this.email && 
        this.password && 
        this.password === this.confirmPassword &&
        this.password.length >= 6;
    }
  },
  methods: {
    async handleRegister() {
      if (!this.isFormValid) {
        if (this.password !== this.confirmPassword) {
          this.error = '两次输入的密码不一致';
        }
        return;
      }
      
      this.loading = true;
      this.error = null;
      
      try {
        const response = await api.post('/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        
        // 注册成功，重定向到登录页
        this.$router.push('/login');
      } catch (error) {
        console.error('注册失败:', error);
        this.error = error.response?.data?.detail || '注册失败，请稍后再试';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.register-card {
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

.register-footer {
  margin-top: 25px;
  text-align: center;
  color: #777;
}

.register-footer a {
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