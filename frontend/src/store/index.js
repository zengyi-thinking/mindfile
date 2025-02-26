import { createStore } from 'vuex'

export default createStore({
  state: {
    user: null,
    mindmaps: [],
    materials: [],
    searchResults: [],
    selectedTags: []
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setMindmaps(state, mindmaps) {
      state.mindmaps = mindmaps
    },
    setMaterials(state, materials) {
      state.materials = materials
    },
    setSearchResults(state, results) {
      state.searchResults = results
    },
    setSelectedTags(state, tags) {
      state.selectedTags = tags
    }
  },
  actions: {
    async searchByMindmap({ commit }, { tagIds, filters, sortBy, page, limit }) {
      try {
        const response = await fetch(`/api/search/mindmap?tag_ids=${tagIds.join(',')}&page=${page}&limit=${limit}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        const data = await response.json()
        commit('setSearchResults', data)
        return data
      } catch (error) {
        console.error('搜索失败:', error)
        throw error
      }
    },
    async uploadMaterial({ commit }, { file, tags, description }) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('tags', JSON.stringify(tags))
        formData.append('description', description)

        const response = await fetch('/api/materials/upload', {
          method: 'POST',
          body: formData
        })
        const data = await response.json()
        return data
      } catch (error) {
        console.error('上传失败:', error)
        throw error
      }
    }
  },
  getters: {
    isAuthenticated: state => !!state.user,
    currentUser: state => state.user,
    searchResultCount: state => state.searchResults.length
  }
})