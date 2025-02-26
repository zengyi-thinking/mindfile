<template>
  <header class="app-header">
    <div class="logo">
      <router-link to="/dashboard">思维导图系统</router-link>
    </div>
    
    <nav class="main-nav">
      <router-link to="/dashboard" class="nav-item">首页</router-link>
      <router-link to="/mindmaps" class="nav-item">思维导图</router-link>
      <router-link to="/materials" class="nav-item">资料管理</router-link>
    </nav>
    
    <div class="user-menu" @click="toggleDropdown" v-if="user">
      <div class="avatar">{{ userInitials }}</div>
      <span class="username">{{ user.username }}</span>
      <span class="dropdown-icon">▼</span>
      
      <div class="dropdown-menu" v-if="showDropdown">
        <router-link to="/settings" class="dropdown-item">用户设置</router-link>
        <div class="dropdown-divider"></div>
        <a href="#" @click.prevent="logout" class="dropdown-item">退出登录</a>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader',
  data() {
    return {
      showDropdown: false,
      user: null
    };
  },
  computed: {
    userInitials() {
      if (!this.user || !this.user.username) return '?';
      return this.user.username.charAt(0).toUpperCase();
    }
  },
  mounted() {
    // 从localStorage获取用户信息
    const userStr = localStorage.getItem('user');
    if (userStr) {
      try {
        this.user = JSON.parse(userStr);
      } catch (e) {
        console.error('解析用户信息失败', e);
      }
    }
    
    // 点击其他地方时关闭下拉菜单
    document.addEventListener('click', this.closeDropdown);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.closeDropdown);
  },
  methods: {
    toggleDropdown(event) {
      event.stopPropagation();
      this.showDropdown = !this.showDropdown;
    },
    closeDropdown(event) {
      if (!event.target.closest('.user-menu')) {
        this.showDropdown = false;
      }
    },
    logout() {
      // 清除token和用户信息
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // 跳转到登录页
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.logo a {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  text-decoration: none;
}

.main-nav {
  display: flex;
  gap: 20px;
}

.nav-item {
  color: #555;
  text-decoration: none;
  padding: 5px 0;
  transition: color 0.3s;
}

.nav-item:hover, .nav-item.router-link-active {
  color: #4a90e2;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  position: relative;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #4a90e2;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
}

.username {
  font-weight: 500;
  color: #333;
}

.dropdown-icon {
  font-size: 10px;
  color: #777;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  width: 200px;
  margin-top: 10px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.dropdown-item {
  display: block;
  padding: 12px 20px;
  color: #333;
  text-decoration: none;
  transition: background-color 0.3s;
}

.dropdown-item:hover {
  background-color: #f5f7fa;
}

.dropdown-divider {
  height: 1px;
  background-color: #eee;
  margin: 5px 0;
}
</style> 