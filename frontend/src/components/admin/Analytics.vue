<template>
  <div class="analytics">
    <h3>推荐系统数据分析</h3>
    <div class="analytics-grid">
      <div class="analytics-card">
        <h4>推荐效果分析</h4>
        <div class="chart-container">
          <canvas ref="recommendationChart"></canvas>
        </div>
      </div>
      <div class="analytics-card">
        <h4>用户群体分布</h4>
        <div class="chart-container">
          <canvas ref="userGroupChart"></canvas>
        </div>
      </div>
      <div class="analytics-card">
        <h4>商品类别分布</h4>
        <div class="chart-container">
          <canvas ref="categoryChart"></canvas>
        </div>
      </div>
      <div class="analytics-card">
        <h4>用户反馈分析</h4>
        <div class="chart-container">
          <canvas ref="feedbackChart"></canvas>
        </div>
      </div>
    </div>
    <div class="analytics-summary">
      <h4>系统概览</h4>
      <div class="summary-grid">
        <div class="summary-item">
          <span class="summary-label">总用户数</span>
          <span class="summary-value">{{ summary.totalUsers }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">总商品数</span>
          <span class="summary-value">{{ summary.totalProducts }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">推荐次数</span>
          <span class="summary-value">{{ summary.recommendationCount }}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">用户反馈数</span>
          <span class="summary-value">{{ summary.feedbackCount }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'

export default {
  name: 'Analytics',
  data() {
    return {
      summary: {
        totalUsers: 0,
        totalProducts: 0,
        recommendationCount: 0,
        feedbackCount: 0
      },
      charts: {}
    }
  },
  mounted() {
    this.loadSummary()
    this.initCharts()
  },
  beforeUnmount() {
    // 清理图表实例
    Object.values(this.charts).forEach(chart => chart.destroy())
  },
  methods: {
    async loadSummary() {
      try {
        // 从API获取数据
        const response = await fetch('/api/admin/analytics')
        if (response.ok) {
          const data = await response.json()
          this.summary = data
        } else {
          // 模拟数据
          this.summary = {
            totalUsers: 120,
            totalProducts: 250,
            recommendationCount: 500,
            feedbackCount: 80
          }
        }
      } catch (error) {
        console.error('Error loading summary:', error)
        // 模拟数据
        this.summary = {
          totalUsers: 120,
          totalProducts: 250,
          recommendationCount: 500,
          feedbackCount: 80
        }
      }
    },
    initCharts() {
      // 初始化所有图表
      this.initRecommendationChart()
      this.initUserGroupChart()
      this.initCategoryChart()
      this.initFeedbackChart()
    },
    initRecommendationChart() {
      // 推荐效果图表
      const ctx = this.$refs.recommendationChart
      if (ctx) {
        this.charts.recommendation = new Chart(ctx, {
          type: 'line',
          data: {
            labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
            datasets: [{
              label: '推荐次数',
              data: [65, 78, 90, 85, 105, 110],
              borderColor: '#4CAF50',
              backgroundColor: 'rgba(76, 175, 80, 0.1)',
              tension: 0.3,
              fill: true
            }, {
              label: '点击次数',
              data: [45, 60, 75, 70, 90, 95],
              borderColor: '#2196F3',
              backgroundColor: 'rgba(33, 150, 243, 0.1)',
              tension: 0.3,
              fill: true
            }, {
              label: '购买次数',
              data: [20, 30, 40, 35, 50, 55],
              borderColor: '#FF9800',
              backgroundColor: 'rgba(255, 152, 0, 0.1)',
              tension: 0.3,
              fill: true
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: '推荐效果趋势'
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
      }
    },
    initUserGroupChart() {
      // 用户群体分布图表
      const ctx = this.$refs.userGroupChart
      if (ctx) {
        this.charts.userGroup = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['主动绿色群体', '潜在绿色群体', '性价比绿色群体', '未分类'],
            datasets: [{
              data: [35, 25, 30, 10],
              backgroundColor: [
                '#4CAF50',
                '#2196F3',
                '#FF9800',
                '#9E9E9E'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
              },
              title: {
                display: true,
                text: '用户群体分布'
              }
            }
          }
        })
      }
    },
    initCategoryChart() {
      // 商品类别分布图表
      const ctx = this.$refs.categoryChart
      if (ctx) {
        this.charts.category = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['食品', '日用品', '家居用品', '母婴用品', '家电', '服装', '美妆', '运动用品'],
            datasets: [{
              label: '绿色商品数量',
              data: [35, 45, 30, 25, 20, 15, 10, 8],
              backgroundColor: '#4CAF50'
            }, {
              label: '普通商品数量',
              data: [65, 55, 70, 75, 80, 85, 90, 92],
              backgroundColor: '#9E9E9E'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: '商品类别分布'
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
      }
    },
    initFeedbackChart() {
      // 用户反馈分析图表
      const ctx = this.$refs.feedbackChart
      if (ctx) {
        this.charts.feedback = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['不感兴趣', '价格过高', '质量问题', '其他'],
            datasets: [{
              data: [40, 30, 20, 10],
              backgroundColor: [
                '#F44336',
                '#FF9800',
                '#9C27B0',
                '#9E9E9E'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
              },
              title: {
                display: true,
                text: '用户反馈分析'
              }
            }
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.analytics {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.analytics h3 {
  margin-bottom: 2rem;
  color: #4CAF50;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(45%, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.analytics-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.analytics-card h4 {
  margin-bottom: 1rem;
  color: #333;
}

.chart-container {
  height: 300px;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.analytics-summary {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.analytics-summary h4 {
  margin-bottom: 1rem;
  color: #333;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.summary-item {
  text-align: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.summary-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.summary-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #4CAF50;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .analytics-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .chart-container {
    height: 250px;
  }
}

@media (max-width: 480px) {
  .analytics {
    padding: 1rem;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 200px;
  }
}
</style>