<template>
  <div class="search-bar">
    <div class="search-type-selector">
      <el-radio-group v-model="searchType" @change="onSearchTypeChange">
        <el-radio label="keyword">关键词搜索</el-radio>
        <el-radio label="mindmap">思维导图搜索</el-radio>
      </el-radio-group>
    </div>

    <!-- 关键词搜索输入框 -->
    <div v-if="searchType === 'keyword'" class="keyword-search">
      <el-input
        v-model="searchQuery"
        placeholder="请输入搜索关键词..."
        @keyup.enter.native="search"
        clearable
      >
        <template slot="append">
          <el-button icon="el-icon-search" @click="search"></el-button>
        </template>
      </el-input>

      <div
        v-if="showHistory && searchHistory.length > 0"
        class="search-history"
      >
        <div class="history-header">
          <h4>搜索历史</h4>
          <el-button type="text" size="mini" @click="clearHistory"
            >清空</el-button
          >
        </div>
        <div class="history-items">
          <div
            v-for="(item, index) in searchHistory"
            :key="index"
            class="history-item"
            @click="useHistoryItem(item.query)"
          >
            <span>{{ item.query }}</span>
            <small>{{ formatDate(item.created_at) }}</small>
          </div>
        </div>
      </div>
    </div>

    <!-- 思维导图搜索 - 标签选择器 -->
    <div v-else class="mindmap-search">
      <el-select
        v-model="selectedTags"
        multiple
        filterable
        placeholder="请选择标签进行搜索..."
        @change="search"
      >
        <el-option
          v-for="tag in availableTags"
          :key="tag.id"
          :label="tag.name"
          :value="tag.id"
        >
          <span :style="{ color: tag.color }">{{ tag.name }}</span>
        </el-option>
      </el-select>
    </div>

    <!-- 高级搜索选项 -->
    <div class="advanced-search">
      <el-collapse v-model="advancedSearchActive">
        <el-collapse-item title="高级搜索选项" name="1">
          <div class="filter-options">
            <div class="filter-section">
              <div class="filter-label">文件类型:</div>
              <el-select
                v-model="filters.fileType"
                placeholder="全部类型"
                clearable
              >
                <el-option label="文档" value="document"></el-option>
                <el-option label="图片" value="image"></el-option>
                <el-option label="视频" value="video"></el-option>
                <el-option label="音频" value="audio"></el-option>
                <el-option label="其他" value="other"></el-option>
              </el-select>
            </div>

            <div class="filter-section">
              <div class="filter-label">上传时间:</div>
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                :clearable="true"
              ></el-date-picker>
            </div>

            <div class="filter-section">
              <div class="filter-label">排序方式:</div>
              <el-radio-group v-model="sortBy">
                <el-radio label="relevance">相关性</el-radio>
                <el-radio label="newest">最新</el-radio>
                <el-radio label="popularity">热门</el-radio>
              </el-radio-group>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
import { getSearchHistory, clearSearchHistory } from "@/services/search";
import { getAllTags } from "@/services/mindmap";

export default {
  name: "SearchBar",
  data() {
    return {
      searchType: "keyword",
      searchQuery: "",
      selectedTags: [],
      availableTags: [],
      searchHistory: [],
      showHistory: false,
      advancedSearchActive: [],
      filters: {
        fileType: "",
      },
      dateRange: [],
      sortBy: "relevance",
    };
  },
  async mounted() {
    await this.loadSearchHistory();
    await this.loadTags();

    // 如果URL中有查询参数，初始化搜索状态
    const query = this.$route.query.q;
    const type = this.$route.query.type || "keyword";

    if (query) {
      this.searchType = type;

      if (type === "keyword") {
        this.searchQuery = query;
      } else {
        // 思维导图搜索，query可能是标签ID列表
        const tagIds = query.split(",").map((id) => parseInt(id));
        this.selectedTags = tagIds.filter((id) => !isNaN(id));
      }

      // 高级搜索参数
      if (this.$route.query.fileType) {
        this.filters.fileType = this.$route.query.fileType;
      }

      if (this.$route.query.dateFrom && this.$route.query.dateTo) {
        this.dateRange = [this.$route.query.dateFrom, this.$route.query.dateTo];
      }

      if (this.$route.query.sortBy) {
        this.sortBy = this.$route.query.sortBy;
      }
    }
  },
  methods: {
    async loadSearchHistory() {
      try {
        this.searchHistory = await getSearchHistory(10);
      } catch (error) {
        console.error("加载搜索历史失败:", error);
      }
    },

    async loadTags() {
      try {
        this.availableTags = await getAllTags();
      } catch (error) {
        console.error("加载标签失败:", error);
      }
    },

    async clearHistory() {
      try {
        await clearSearchHistory();
        this.searchHistory = [];
        this.showHistory = false;
      } catch (error) {
        console.error("清除搜索历史失败:", error);
        this.$message.error("清除搜索历史失败");
      }
    },

    useHistoryItem(query) {
      this.searchQuery = query;
      this.search();
    },

    onSearchTypeChange(value) {
      this.searchQuery = "";
      this.selectedTags = [];
      this.$emit("search-type-change", value);
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString();
    },

    search() {
      // 构建搜索参数
      const searchParams = {
        type: this.searchType,
      };

      if (this.searchType === "keyword") {
        if (!this.searchQuery.trim()) {
          this.$message.warning("请输入搜索关键词");
          return;
        }
        searchParams.q = this.searchQuery.trim();
      } else {
        if (this.selectedTags.length === 0) {
          this.$message.warning("请选择至少一个标签");
          return;
        }
        searchParams.q = this.selectedTags.join(",");
      }

      // 添加高级搜索参数
      if (this.filters.fileType) {
        searchParams.fileType = this.filters.fileType;
      }

      if (this.dateRange && this.dateRange.length === 2) {
        searchParams.dateFrom = this.dateRange[0];
        searchParams.dateTo = this.dateRange[1];
      }

      searchParams.sortBy = this.sortBy;

      // 导航到搜索结果页面
      this.$router.push({
        path: "/search",
        query: searchParams,
      });

      // 触发搜索事件
      this.$emit("search", searchParams);
    },
  },
};
</script>

<style scoped>
.search-bar {
  width: 100%;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-type-selector {
  margin-bottom: 15px;
}

.keyword-search,
.mindmap-search {
  position: relative;
  margin-bottom: 15px;
}

.keyword-search .el-input,
.mindmap-search .el-select {
  width: 100%;
}

.search-history {
  position: absolute;
  width: 100%;
  max-height: 300px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #e6e6e6;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid #f0f0f0;
}

.history-header h4 {
  margin: 0;
  font-size: 14px;
  color: #606266;
}

.history-items {
  padding: 5px 0;
}

.history-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 15px;
  cursor: pointer;
}

.history-item:hover {
  background-color: #f5f7fa;
}

.history-item small {
  color: #909399;
}

.advanced-search {
  margin-top: 15px;
}

.filter-options {
  padding: 10px;
}

.filter-section {
  margin-bottom: 15px;
}

.filter-label {
  margin-bottom: 5px;
  font-size: 14px;
  color: #606266;
}

.filter-section .el-select,
.filter-section .el-date-picker {
  width: 100%;
}
</style>
