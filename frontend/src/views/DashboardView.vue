<template>
  <div class="dashboard-container">
    <h1>欢迎使用思维导图系统</h1>
    
    <div class="dashboard-stats">
      <div class="stat-card">
        <h3>我的思维导图</h3>
        <p class="stat-number">0</p>
      </div>
      
      <div class="stat-card">
        <h3>我的资料</h3>
        <p class="stat-number">0</p>
      </div>
    </div>
    
    <div class="quick-actions">
      <router-link to="/mindmaps" class="action-button">
        <i class="el-icon-plus"></i>
        创建思维导图
      </router-link>
      
      <router-link to="/materials" class="action-button">
        <i class="el-icon-upload"></i>
        上传资料
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  data() {
    return {
      // 后续可以添加仪表盘数据
    };
  }
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 30px;
  color: #333;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  color: #666;
  margin-bottom: 10px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #4a90e2;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 15px;
  background-color: #4a90e2;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #357abd;
}
</style>