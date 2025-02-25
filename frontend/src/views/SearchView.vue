<template>
  <div class="search-view">
    <search-bar
      @search="performSearch"
      @search-type-change="onSearchTypeChange"
    ></search-bar>

    <div class="search-results">
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="5" animated />
      </div>

      <div v-else-if="error" class="error-state">
        <el-result icon="error" title="搜索失败" :sub-title="error.message">
          <template #extra>
            <el-button type="primary" @click="retry">重试</el-button>
          </template>
        </el-result>
      </div>

      <div v-else>
        <!-- 关键词搜索结果 -->
        <div v-if="searchType === 'keyword'" class="keyword-results">
          <div class="results-header">
            <h2>搜索结果: "{{ searchQuery }}"</h2>
            <p>找到 {{ totalResults || 0 }} 条结果</p>
          </div>

          <div v-if="searchResults.length === 0" class="no-results">
            <el-empty description="没有找到匹配的结果"></el-empty>
          </div>

          <div v-else class="results-list">
            <material-card
              v-for="material in searchResults"
              :key="material.id"
              :material="material"
              @click="openMaterial(material.id)"
            ></material-card>

            <div class="pagination">
              <el-pagination
                background
                layout="prev, pager, next"
                :total="totalResults"
                :page-size="pageSize"
                :current-page.sync="currentPage"
                @current-change="handlePageChange"
              ></el-pagination>
            </div>
          </div>
        </div>

        <!-- 思维导图搜索结果 -->
        <div v-else class="mindmap-results">
          <div class="results-header">
            <h2>思维导图搜索结果</h2>
            <p>找到 {{ totalResults || 0 }} 个相关思维导图</p>
          </div>

          <div v-if="searchResults.length === 0" class="no-results">
            <el-empty description="没有找到匹配的思维导图"></el-empty>
          </div>

          <div v-else>
            <div class="related-tags" v-if="relatedTags.length > 0">
              <h3>相关标签：</h3>
              <div class="tag-cloud">
                <el-tag
                  v-for="tag in relatedTags"
                  :key="tag.id"
                  :color="tag.color"
                  effect="plain"
                  @click="addTagToSearch(tag.id)"
                  :disable-transitions="false"
                  :class="{ selected: selectedTagIds.includes(tag.id) }"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
            </div>

            <div class="mindmap-container">
              <mind-map
                :mapData="currentMindMapData"
                @node-click="handleNodeClick"
              ></mind-map>
            </div>

            <div class="mindmap-list">
              <h3>思维导图列表</h3>
              <el-tabs v-model="activeMindmap" @tab-click="handleMindMapChange">
                <el-tab-pane
                  v-for="(mindmap, index) in searchResults"
                  :key="mindmap.id"
                  :label="mindmap.title"
                  :name="index.toString()"
                >
                  <div class="mindmap-info">
                    <h4>{{ mindmap.title }}</h4>
                    <p>{{ mindmap.description }}</p>
                    <div class="tags">
                      <el-tag
                        v-for="tag in mindmap.tags"
                        :key="tag.id"
                        size="small"
                        :color="tag.color"
                      >
                        {{ tag.name }}
                      </el-tag>
                    </div>
                  </div>

                  <div
                    class="related-materials"
                    v-if="mindmap.materials && mindmap.materials.length > 0"
                  >
                    <h4>相关资料</h4>
                    <div class="materials-list">
                      <material-card
                        v-for="material in mindmap.materials"
                        :key="material.id"
                        :material="material"
                        @click="openMaterial(material.id)"
                      ></material-card>
                    </div>
                  </div>
                </el-tab-pane>
              </el-tabs>
            </div>

            <div class="pagination">
              <el-pagination
                background
                layout="prev, pager, next"
                :total="totalResults"
                :page-size="pageSize"
                :current-page.sync="currentPage"
                @current-change="handlePageChange"
              ></el-pagination>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";
import MaterialCard from "@/components/MaterialCard.vue";
import MindMap from "@/components/MindMap.vue";
import { searchByKeyword, searchByMindMap } from "@/services/search";

export default {
  name: "SearchView",
  components: {
    SearchBar,
    MaterialCard,
    MindMap,
  },
  data() {
    return {
      searchType: "keyword",
      searchQuery: "",
      selectedTagIds: [],
      searchResults: [],
      relatedTags: [],
      totalResults: 0,
      currentPage: 1,
      pageSize: 10,
      loading: false,
      error: null,
      activeMindmap: "0",
      currentMindMapData: null,
    };
  },
  created() {
    // 从URL查询参数初始化搜索状态
    const query = this.$route.query.q;
    const type = this.$route.query.type || "keyword";

    if (query) {
      this.searchType = type;
      if (type === "keyword") {
        this.searchQuery = query;
      } else {
        // 思维导图搜索，查询参数是标签ID列表
        this.selectedTagIds = query
          .split(",")
          .map((id) => parseInt(id))
          .filter((id) => !isNaN(id));
      }

      // 开始搜索
      this.performSearch();
    }
  },
  methods: {
    async performSearch() {
      this.loading = true;
      this.error = null;

      try {
        if (this.searchType === "keyword") {
          await this.searchByKeyword();
        } else {
          await this.searchByMindmap();
        }
      } catch (error) {
        console.error("搜索失败:", error);
        this.error = error;
      } finally {
        this.loading = false;
      }
    },

    async searchByKeyword() {
      if (!this.searchQuery.trim()) return;

      // 构建过滤器
      const filters = {};
      if (this.$route.query.fileType) {
        filters.file_type = this.$route.query.fileType;
      }

      if (this.$route.query.dateFrom && this.$route.query.dateTo) {
        filters.date_from = this.$route.query.dateFrom;
        filters.date_to = this.$route.query.dateTo;
      }

      const sortBy = this.$route.query.sortBy || "relevance";

      // 执行搜索
      const result = await searchByKeyword(
        this.searchQuery,
        filters,
        sortBy,
        this.currentPage,
        this.pageSize
      );

      this.searchResults = result.items;
      this.totalResults = result.total;
    },

    async searchByMindmap() {
      if (this.selectedTagIds.length === 0) return;

      // 构建过滤器
      const filters = {};
      if (this.$route.query.fileType) {
        filters.file_type = this.$route.query.fileType;
      }

      if (this.$route.query.dateFrom && this.$route.query.dateTo) {
        filters.date_from = this.$route.query.dateFrom;
        filters.date_to = this.$route.query.dateTo;
      }

      const sortBy = this.$route.query.sortBy || "relevance";

      // 执行思维导图搜索
      const result = await searchByMindMap(
        this.selectedTagIds,
        filters,
        sortBy,
        this.currentPage,
        this.pageSize
      );

      this.searchResults = result.items;
      this.totalResults = result.total;
      this.relatedTags = result.related_tags || [];

      // 设置当前激活的思维导图
      if (this.searchResults.length > 0) {
        this.activeMindmap = "0";
        this.setCurrentMindMapData(this.searchResults[0]);
      }
    },

    setCurrentMindMapData(mindmap) {
      // 将思维导图数据转换为MindMap组件所需的格式
      try {
        let data;
        if (typeof mindmap.data === "string") {
          data = JSON.parse(mindmap.data);
        } else {
          data = mindmap.data;
        }

        // 添加资料节点到思维导图数据
        if (mindmap.materials && mindmap.materials.length > 0) {
          this.addMaterialsToMindMapData(data, mindmap.materials);
        }

        this.currentMindMapData = data;
      } catch (error) {
        console.error("解析思维导图数据失败:", error);
        this.currentMindMapData = {
          name: mindmap.title,
          children: [],
        };
      }
    },

    addMaterialsToMindMapData(node, materials) {
      // 递归遍历思维导图节点，根据标签添加资料节点
      if (!node) return;

      // 如果节点有标签，查找匹配的资料
      if (node.tags) {
        const matchingMaterials = materials.filter(
          (material) =>
            material.tags &&
            material.tags.some((tag) =>
              node.tags.some((nodeTag) => nodeTag.id === tag.id)
            )
        );

        // 添加资料子节点
        if (matchingMaterials.length > 0) {
          if (!node.children) {
            node.children = [];
          }

          // 添加资料节点
          matchingMaterials.forEach((material) => {
            node.children.push({
              name: material.title,
              id: material.id,
              type: "material",
              tags: material.tags,
            });
          });
        }
      }

      // 递归处理子节点
      if (node.children && node.children.length > 0) {
        node.children.forEach((child) =>
          this.addMaterialsToMindMapData(child, materials)
        );
      }
    },

    handleMindMapChange(tab) {
      const index = parseInt(tab.name);
      if (!isNaN(index) && this.searchResults[index]) {
        this.setCurrentMindMapData(this.searchResults[index]);
      }
    },

    handleNodeClick(node) {
      if (node.type === "material" && node.id) {
        this.openMaterial(node.id);
      }
    },

    addTagToSearch(tagId) {
      // 添加或移除标签
      const index = this.selectedTagIds.indexOf(tagId);
      if (index === -1) {
        this.selectedTagIds.push(tagId);
      } else {
        this.selectedTagIds.splice(index, 1);
      }

      // 更新URL并重新搜索
      this.$router.push({
        path: "/search",
        query: {
          ...this.$route.query,
          q: this.selectedTagIds.join(","),
          type: "mindmap",
        },
      });

      this.performSearch();
    },

    openMaterial(materialId) {
      this.$router.push(`/material/${materialId}`);
    },

    handlePageChange(page) {
      this.currentPage = page;

      // 更新URL
      this.$router.push({
        path: "/search",
        query: {
          ...this.$route.query,
          page: page,
        },
      });

      this.performSearch();
    },

    onSearchTypeChange(type) {
      this.searchType = type;
    },

    retry() {
      this.performSearch();
    },
  },
};
</script>

<style scoped>
.search-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-results {
  margin-top: 30px;
}

.loading-state {
  padding: 20px;
}

.results-header {
  margin-bottom: 20px;
}

.results-header h2 {
  margin-bottom: 5px;
  color: #303133;
}

.results-header p {
  color: #909399;
}

.results-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.related-tags {
  margin-bottom: 20px;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-cloud .el-tag {
  cursor: pointer;
}

.tag-cloud .el-tag.selected {
  font-weight: bold;
  transform: scale(1.05);
}

.mindmap-container {
  height: 500px;
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  margin-bottom: 30px;
}

.mindmap-list {
  margin-top: 30px;
}

.mindmap-info {
  margin-bottom: 15px;
}

.mindmap-info h4 {
  margin-bottom: 5px;
}

.mindmap-info p {
  color: #606266;
  margin-bottom: 10px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.related-materials h4 {
  margin-bottom: 15px;
}

.materials-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 15px;
}
</style>
