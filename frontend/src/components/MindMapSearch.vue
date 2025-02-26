<template>
  <div class="mindmap-search">
    <div class="search-controls">
      <el-input
        v-model="searchQuery"
        placeholder="输入关键词搜索..."
        @input="onSearch"
        clearable
      >
        <template #prefix>
          <i class="el-icon-search"></i>
        </template>
      </el-input>

      <div class="filter-section">
        <el-select v-model="selectedTags" multiple placeholder="选择标签" @change="onSearch">
          <el-option
            v-for="tag in availableTags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          >
            <span :style="{ color: tag.color }">{{ tag.name }}</span>
          </el-option>
        </el-select>

        <el-select v-model="fileType" placeholder="文件类型" @change="onSearch">
          <el-option label="全部" value=""></el-option>
          <el-option label="文本" value="text"></el-option>
          <el-option label="PDF" value="pdf"></el-option>
          <el-option label="图片" value="image"></el-option>
        </el-select>

        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          @change="onSearch"
        ></el-date-picker>
      </div>
    </div>

    <div class="mindmap-container">
      <div id="mindmap" ref="mindmapContainer"></div>
    </div>

    <div class="search-results" v-if="searchResults.length > 0">
      <h3>搜索结果</h3>
      <el-card v-for="result in searchResults" :key="result.id" class="result-card">
        <div class="result-title">{{ result.title }}</div>
        <div class="result-tags">
          <el-tag
            v-for="tag in result.tags"
            :key="tag.id"
            :color="tag.color"
            size="small"
          >
            {{ tag.name }}
          </el-tag>
        </div>
        <div class="result-description">{{ result.description }}</div>
        <div class="result-footer">
          <span>{{ formatDate(result.created_at) }}</span>
          <el-button type="text" @click="viewMaterial(result.id)">查看详情</el-button>
        </div>
      </el-card>
    </div>

    <div class="no-results" v-else-if="hasSearched">
      <el-empty description="未找到相关资料"></el-empty>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3';
import { searchByMindMap } from '@/services/search';

export default {
  name: 'MindMapSearch',
  data() {
    return {
      searchQuery: '',
      selectedTags: [],
      fileType: '',
      dateRange: [],
      availableTags: [],
      searchResults: [],
      hasSearched: false,
      mindmapData: null,
      svg: null,
      simulation: null
    };
  },
  mounted() {
    this.initMindMap();
    this.fetchTags();
  },
  methods: {
    async fetchTags() {
      try {
        // 从API获取可用标签列表
        const response = await this.$http.get('/api/tags');
        this.availableTags = response.data;
      } catch (error) {
        console.error('获取标签失败:', error);
      }
    },
    async onSearch() {
      this.hasSearched = true;
      try {
        const params = {
          query: this.searchQuery,
          tags: this.selectedTags,
          file_type: this.fileType,
          start_date: this.dateRange[0],
          end_date: this.dateRange[1]
        };

        const response = await searchByMindMap(params);
        this.searchResults = response.data.results;
        this.updateMindMap(response.data.mindmap);
      } catch (error) {
        console.error('搜索失败:', error);
      }
    },
    initMindMap() {
      const container = this.$refs.mindmapContainer;
      const width = container.clientWidth;
      const height = container.clientHeight;

      this.svg = d3.select('#mindmap')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      this.simulation = d3.forceSimulation()
        .force('link', d3.forceLink().id(d => d.id))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(width / 2, height / 2));
    },
    updateMindMap(data) {
      if (!data || !data.nodes || !data.links) return;

      const svg = this.svg;
      const simulation = this.simulation;

      // 清除现有内容
      svg.selectAll('*').remove();

      const link = svg.append('g')
        .selectAll('line')
        .data(data.links)
        .enter().append('line')
        .attr('stroke', '#999')
        .attr('stroke-opacity', 0.6);

      const node = svg.append('g')
        .selectAll('circle')
        .data(data.nodes)
        .enter().append('circle')
        .attr('r', 5)
        .attr('fill', d => d.color || '#69c0ff')
        .call(d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended));

      const text = svg.append('g')
        .selectAll('text')
        .data(data.nodes)
        .enter().append('text')
        .text(d => d.name)
        .attr('dx', 12)
        .attr('dy', '.35em');

      simulation
        .nodes(data.nodes)
        .on('tick', ticked);

      simulation.force('link')
        .links(data.links);

      function ticked() {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);

        node
          .attr('cx', d => d.x)
          .attr('cy', d => d.y);

        text
          .attr('x', d => d.x)
          .attr('y', d => d.y);
      }

      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }

      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }

      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }
    },
    viewMaterial(id) {
      this.$router.push(`/materials/${id}`);
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString('zh-CN');
    }
  }
};
</script>

<style scoped>
.mindmap-search {
  padding: 20px;
}

.search-controls {
  margin-bottom: 20px;
}

.filter-section {
  margin-top: 15px;
  display: flex;
  gap: 15px;
}

.mindmap-container {
  height: 500px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  margin-bottom: 20px;
  overflow: hidden;
}

#mindmap {
  width: 100%;
  height: 100%;
}

.search-results {
  margin-top: 20px;
}

.result-card {
  margin-bottom: 15px;
}

.result-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
}

.result-tags {
  margin-bottom: 10px;
}

.result-description {
  color: #666;
  margin-bottom: 10px;
}

.result-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 14px;
}

.no-results {
  text-align: center;
  padding: 40px;
}
</style>