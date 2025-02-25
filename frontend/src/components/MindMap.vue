<template>
  <div class="mindmap-container">
    <div class="toolbar">
      <div class="search-type">
        <span>搜索模式:</span>
        <el-radio-group v-model="searchType" @change="onSearchTypeChange">
          <el-radio label="keyword">关键词搜索</el-radio>
          <el-radio label="mindmap">思维导图搜索</el-radio>
        </el-radio-group>
      </div>
      <div class="controls">
        <el-button size="small" @click="zoomIn">
          <i class="el-icon-zoom-in"></i>
        </el-button>
        <el-button size="small" @click="zoomOut">
          <i class="el-icon-zoom-out"></i>
        </el-button>
        <el-button size="small" @click="resetView">
          <i class="el-icon-refresh"></i>
        </el-button>
      </div>
    </div>
    <div id="mindmap-chart" class="chart-container"></div>

    <!-- 资料预览抽屉 -->
    <el-drawer
      title="资料预览"
      :visible.sync="drawerVisible"
      direction="rtl"
      size="50%"
    >
      <div v-if="selectedMaterial" class="material-preview">
        <h2>{{ selectedMaterial.title }}</h2>
        <div class="tags">
          <el-tag
            v-for="tag in selectedMaterial.tags"
            :key="tag.id"
            :color="tag.color"
          >
            {{ tag.name }}
          </el-tag>
        </div>
        <p class="description">{{ selectedMaterial.description }}</p>
        <div
          class="preview-content"
          v-if="selectedMaterial.file_type === 'text'"
        >
          {{ selectedMaterial.content }}
        </div>
        <div class="file-preview" v-else>
          <el-button type="primary" @click="openFile(selectedMaterial.id)">
            打开文件
          </el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import * as echarts from "echarts";
import { getMindMapData, getMaterialById } from "@/services/mindmap";

export default {
  name: "MindMap",
  props: {
    mapId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      searchType: "mindmap",
      chart: null,
      mindmapData: null,
      selectedMaterial: null,
      drawerVisible: false,
      zoomLevel: 1,
    };
  },
  mounted() {
    this.initChart();
    this.loadMindMapData();
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById("mindmap-chart"));
      this.chart.on("click", this.handleNodeClick);

      // 处理窗口大小变化
      window.addEventListener("resize", () => {
        this.chart.resize();
      });
    },

    async loadMindMapData() {
      try {
        const data = await getMindMapData(this.mapId);
        this.mindmapData = data;
        this.renderMindMap(data);
      } catch (error) {
        console.error("加载思维导图数据失败:", error);
        this.$message.error("加载思维导图数据失败");
      }
    },

    renderMindMap(data) {
      // 使用树图布局
      const option = {
        tooltip: {
          trigger: "item",
          formatter: "{b}: {c}",
        },
        series: [
          {
            type: "tree",
            data: [data],
            top: "10%",
            left: "10%",
            bottom: "10%",
            right: "10%",
            symbolSize: 12,
            initialTreeDepth: 3,
            label: {
              position: "left",
              verticalAlign: "middle",
              align: "right",
              fontSize: 14,
              formatter: (params) => {
                // 显示节点名称和标签信息
                const name = params.data.name;
                const tags = params.data.tags || [];
                const tagText = tags.map((t) => `#${t.name}`).join(" ");
                return `{name|${name}}\n{tag|${tagText}}`;
              },
              rich: {
                name: {
                  fontSize: 14,
                  fontWeight: "bold",
                },
                tag: {
                  fontSize: 12,
                  color: "#888",
                },
              },
            },
            leaves: {
              label: {
                position: "right",
                verticalAlign: "middle",
                align: "left",
              },
            },
            itemStyle: {
              color: (params) => {
                // 根据搜索历史上色
                return params.data.searched ? "#ff7675" : "#3498db";
              },
            },
            expandAndCollapse: true,
            animationDuration: 550,
            animationDurationUpdate: 750,
          },
        ],
      };

      this.chart.setOption(option);
    },

    async handleNodeClick(params) {
      // 如果点击的是文件节点
      if (params.data.type === "material") {
        try {
          const material = await getMaterialById(params.data.id);
          this.selectedMaterial = material;
          this.drawerVisible = true;
        } catch (error) {
          console.error("获取资料信息失败:", error);
          this.$message.error("获取资料信息失败");
        }
      }
      // 如果点击的是标签节点，展开/折叠
      else if (params.data.type === "tag") {
        this.chart.dispatchAction({
          type: "treeExpandAndCollapse",
          seriesIndex: 0,
          dataIndex: params.dataIndex,
        });
      }
    },

    openFile(materialId) {
      // 打开文件预览页面
      this.$router.push(`/material/${materialId}`);
    },

    zoomIn() {
      this.zoomLevel *= 1.2;
      this.chart.setOption({
        series: [
          {
            zoom: this.zoomLevel,
          },
        ],
      });
    },

    zoomOut() {
      this.zoomLevel /= 1.2;
      this.chart.setOption({
        series: [
          {
            zoom: this.zoomLevel,
          },
        ],
      });
    },

    resetView() {
      this.zoomLevel = 1;
      this.chart.setOption({
        series: [
          {
            zoom: 1,
          },
        ],
      });

      // 重置视图位置
      this.chart.setOption({
        series: [
          {
            left: "10%",
            top: "10%",
            right: "10%",
            bottom: "10%",
          },
        ],
      });
    },

    onSearchTypeChange(value) {
      this.$emit("search-type-change", value);
    },
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
    }
    window.removeEventListener("resize", this.chart.resize);
  },
};
</script>

<style scoped>
.mindmap-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e6e9ed;
}

.chart-container {
  flex: 1;
  min-height: 500px;
}

.material-preview {
  padding: 20px;
}

.tags {
  margin: 10px 0;
}

.description {
  color: #666;
  margin-bottom: 20px;
}

.preview-content {
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
}

.file-preview {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
