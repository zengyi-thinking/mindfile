import axios from 'axios';

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000';

export const mindmapService = {
  // 获取所有思维导图
  async getMindmaps() {
    const response = await axios.get(`${API_URL}/api/mindmaps`);
    return response.data;
  },

  // 获取单个思维导图
  async getMindmap(id) {
    const response = await axios.get(`${API_URL}/api/mindmaps/${id}`);
    return response.data;
  },

  // 创建思维导图
  async createMindmap(data) {
    const response = await axios.post(`${API_URL}/api/mindmaps`, data);
    return response.data;
  },

  // 更新思维导图
  async updateMindmap(id, data) {
    const response = await axios.put(`${API_URL}/api/mindmaps/${id}`, data);
    return response.data;
  },

  // 删除思维导图
  async deleteMindmap(id) {
    await axios.delete(`${API_URL}/api/mindmaps/${id}`);
  },

  // 搜索思维导图
  async searchMindmaps(params) {
    const response = await axios.get(`${API_URL}/api/search/mindmap`, { params });
    return response.data;
  },

  // 导出思维导图
  async exportMindmap(id, format = 'mmap') {
    const response = await axios.get(`${API_URL}/api/mindmaps/${id}/export`, {
      params: { format },
      responseType: 'blob'
    });
    return response.data;
  },

  // 导入思维导图
  async importMindmap(file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_URL}/api/mindmaps/import`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  }
};