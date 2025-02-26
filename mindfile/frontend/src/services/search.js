import api from './api';

/**
 * 执行关键词搜索
 * @param {string} query - 搜索关键词
 * @param {Object} filters - 搜索过滤器
 * @param {string} sortBy - 排序方式
 * @param {number} page - 页码
 * @param {number} limit - 每页数量
 * @returns {Promise} - 搜索结果
 */
export async function searchByKeyword(query, filters = {}, sortBy = 'relevance', page = 1, limit = 10) {
  try {
    const response = await api.get('/api/search/keyword', {
      params: {
        query,
        ...filters,
        sort_by: sortBy,
        page,
        limit
      }
    });
    return response.data;
  } catch (error) {
    console.error('关键词搜索失败:', error);
    throw error;
  }
}

/**
 * 执行思维导图搜索
 * @param {Array} tagIds - 标签ID数组
 * @param {Object} filters - 搜索过滤器
 * @param {string} sortBy - 排序方式
 * @param {number} page - 页码
 * @param {number} limit - 每页数量
 * @returns {Promise} - 搜索结果
 */
export async function searchByMindMap(tagIds, filters = {}, sortBy = 'relevance', page = 1, limit = 10) {
  try {
    const response = await api.get('/api/search/mindmap', {
      params: {
        tag_ids: tagIds.join(','),
        ...filters,
        sort_by: sortBy,
        page,
        limit
      }
    });
    return response.data;
  } catch (error) {
    console.error('思维导图搜索失败:', error);
    throw error;
  }
}

/**
 * 获取用户搜索历史
 * @param {number} limit - 限制数量
 * @returns {Promise} - 搜索历史
 */
export async function getSearchHistory(limit = 10) {
  try {
    const response = await api.get('/api/search/history', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('获取搜索历史失败:', error);
    throw error;
  }
}

/**
 * 清除搜索历史
 * @returns {Promise}
 */
export async function clearSearchHistory() {
  try {
    const response = await api.delete('/api/search/history');
    return response.data;
  } catch (error) {
    console.error('清除搜索历史失败:', error);
    throw error;
  }
}

/**
 * 根据标签获取相关资料
 * @param {Array} tagIds - 标签ID数组
 * @param {number} page - 页码
 * @param {number} limit - 每页数量
 * @returns {Promise} - 资料列表
 */
export async function getMaterialsByTags(tagIds, page = 1, limit = 10) {
  try {
    const response = await api.get('/api/materials/by-tags', {
      params: {
        tag_ids: tagIds.join(','),
        page,
        limit
      }
    });
    return response.data;
  } catch (error) {
    console.error('根据标签获取资料失败:', error);
    throw error;
  }
} 