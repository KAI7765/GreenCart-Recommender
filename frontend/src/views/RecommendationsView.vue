<template>
  <div class="recommendations">
    <div class="container">
      <div class="recommendations-header">
        <h2>为您推荐的绿色产品</h2>
        <div class="filter-options">
          <label for="sort-select">排序方式:</label>
          <select id="sort-select" v-model="sortBy" @change="sortProducts">
            <option value="match">匹配度优先</option>
            <option value="price">价格优先</option>
            <option value="sales">销量优先</option>
            <option value="rating">评分优先</option>
          </select>
        </div>
      </div>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="products.length === 0" class="no-products">
        <p>暂无推荐商品，请尝试调整偏好设置</p>
      </div>
      <div v-else class="product-grid">
        <div v-for="product in products" :key="product.id" class="product-card">
          <div class="product-image-container">
            <img :src="product.image_url || 'https://via.placeholder.com/300'" :alt="product.name" class="product-image">
            <div class="product-badge" v-if="product.green_labels.length > 0">
              绿色产品
            </div>
          </div>
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <div class="product-labels">
              <span v-for="label in product.green_labels" :key="label" class="green-label">{{ label }}</span>
            </div>
            <p class="product-price">¥{{ product.price.toFixed(2) }}</p>
            <div class="product-meta">
              <span class="sales">销量: {{ product.sales }}</span>
              <span class="rating">评分: {{ product.rating.toFixed(1) }}</span>
            </div>
            <p class="product-description">{{ product.description.substring(0, 100) }}...</p>
            <div class="product-actions">
              <button @click="goToDetail(product.id)" class="btn btn-secondary">查看详情</button>
              <button @click="recordBehavior(product.id, 'purchase')" class="btn btn-primary">立即购买</button>
              <div class="feedback-buttons">
                <button @click="submitFeedback(product.id, 'not_interested')" class="btn btn-feedback">
                  <i class="icon">👎</i> 不感兴趣
                </button>
                <button @click="submitFeedback(product.id, 'price_too_high')" class="btn btn-feedback">
                  <i class="icon">💰</i> 价格过高
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecommendationsView',
  data() {
    return {
      products: [],
      loading: true,
      error: null,
      sortBy: 'match',
      originalProducts: []
    }
  },
  mounted() {
    console.log('RecommendationsView mounted')
    this.getRecommendations()
  },
  methods: {
    async getRecommendations() {
      console.log('getRecommendations called')
      try {
        const userData = localStorage.getItem('user')
        console.log('User data from localStorage:', userData)
        
        // 如果没有登录用户，则获取热门绿色商品（无需登录）
        if (!userData) {
          console.log('No user found in localStorage, fetching hot green products')
          await this.fetchHotGreenProducts()
          return
        }
        
        const user = JSON.parse(localStorage.getItem('user'))
        console.log('User:', user)
        if (!user) {
          console.log('No user found')
          // 解析失败，获取热门商品
          await this.fetchHotGreenProducts()
          return
        }
        
        console.log('Fetching recommendations for user:', user.id)
        console.log('Fetch URL:', `/api/recommend/${user.id}`)
        const response = await fetch(`/api/recommend/${user.id}`)
        console.log('Response status:', response.status)
        if (response.ok) {
          console.log('Response ok, parsing JSON')
          const data = await response.json()
          console.log('Recommendations:', data)
          console.log('Recommendations length:', data.length)
          this.products = data
          this.originalProducts = [...data]
        } else {
          console.log('Response not ok:', response.status)
          this.error = '获取推荐失败'
        }
      } catch (error) {
        console.error('Error getting recommendations:', error)
        this.error = '获取推荐失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    async fetchHotGreenProducts() {
      try {
        // 调用后端获取热门绿色商品
        const response = await fetch('/api/admin/products/hot')
        if (response.ok) {
          const data = await response.json()
          this.products = data
          this.originalProducts = [...this.products]
        } else {
          // 如果请求失败，返回空列表
          this.products = []
          this.originalProducts = []
        }
      } catch (error) {
        console.error('Error fetching hot products:', error)
        this.products = []
        this.originalProducts = []
      }
    },
    sortProducts() {
      switch (this.sortBy) {
        case 'price':
          this.products.sort((a, b) => a.price - b.price)
          break
        case 'sales':
          this.products.sort((a, b) => b.sales - a.sales)
          break
        case 'rating':
          this.products.sort((a, b) => b.rating - a.rating)
          break
        default:
          this.products = [...this.originalProducts]
      }
    },
    async recordBehavior(productId, behaviorType) {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          alert('请先登录后再进行操作')
          return
        }
        
        await fetch('/api/user/behavior', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: user.id,
            product_id: productId,
            behavior_type: behaviorType
          })
        })
      } catch (error) {
        console.error('Error recording behavior:', error)
      }
    },
    async submitFeedback(productId, feedbackType) {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          alert('请先登录后再进行操作')
          return
        }
        
        await fetch('/api/user/feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: user.id,
            product_id: productId,
            feedback_type: feedbackType
          })
        })
        
        // 重新获取推荐商品
        await this.getRecommendations()
      } catch (error) {
        console.error('Error submitting feedback:', error)
      }
    },
    goToDetail(productId) {
      const user = JSON.parse(localStorage.getItem('user'))
      if (!user) {
        alert('请先登录后再查看详情')
        return
      }
      // 记录浏览行为
      this.recordBehavior(productId, 'view')
      // 跳转到商品详情页面
      this.$router.push(`/product/${productId}`)
    }
  }
}
</script>

<style scoped>
.recommendations {
  padding: 2rem 0 !important;
  min-height: 80vh !important;
}

.container {
  width: 95% !important;
  max-width: 1400px !important;
  margin: 0 auto !important;
  display: block !important;
}

.recommendations-header {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  margin-bottom: 2rem !important;
  padding-bottom: 1rem !important;
  border-bottom: 1px solid #e9ecef !important;
}

.recommendations h2 {
  color: #4CAF50 !important;
  font-size: 1.8rem !important;
  margin: 0 !important;
  text-align: left !important;
}

.filter-options {
  display: flex !important;
  gap: 1rem !important;
  align-items: center !important;
  float: right !important;
}

.filter-options label {
  font-weight: bold !important;
  color: #333 !important;
}

.filter-options select {
  padding: 0.6rem 1rem !important;
  border: 1px solid #ddd !important;
  border-radius: 4px !important;
  font-size: 1rem !important;
  background-color: white !important;
}

.loading, .error {
  text-align: center !important;
  padding: 4rem !important;
  font-size: 1.2rem !important;
}

.error {
  color: #f44336 !important;
}

.no-products {
  text-align: center !important;
  padding: 4rem !important;
  font-size: 1.2rem !important;
  color: #666 !important;
}

.product-grid {
  display: grid !important;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)) !important;
  gap: 1.5rem !important;
  clear: both !important;
}

.product-card {
  background-color: #f8f9fa !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
  transition: transform 0.3s !important;
  width: 100% !important;
  margin: 0 !important;
  float: none !important;
}

.product-card:hover {
  transform: translateY(-5px) !important;
}

.product-image {
  width: 100% !important;
  height: 200px !important;
  object-fit: cover !important;
}

.product-info {
  padding: 1.5rem !important;
}

.product-name {
  margin-bottom: 1rem !important;
  font-size: 1.1rem !important;
}

.product-labels {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 0.5rem !important;
  margin-bottom: 1rem !important;
}

.green-label {
  background-color: #4CAF50 !important;
  color: white !important;
  padding: 0.2rem 0.5rem !important;
  border-radius: 4px !important;
  font-size: 0.8rem !important;
}

.product-price {
  font-size: 1.2rem !important;
  font-weight: bold !important;
  color: #f44336 !important;
  margin-bottom: 1rem !important;
}

.product-meta {
  display: flex !important;
  justify-content: space-between !important;
  font-size: 0.9rem !important;
  color: #666 !important;
  margin-bottom: 1rem !important;
}

.product-actions {
  display: flex !important;
  flex-direction: column !important;
  gap: 0.5rem !important;
}

.btn {
  padding: 0.6rem !important;
  border: none !important;
  border-radius: 4px !important;
  font-weight: bold !important;
  cursor: pointer !important;
  transition: background-color 0.3s !important;
}

.btn-primary {
  background-color: #4CAF50 !important;
  color: white !important;
}

.btn-primary:hover {
  background-color: #45a049 !important;
}

.btn-secondary {
  background-color: #2196F3 !important;
  color: white !important;
}

.btn-secondary:hover {
  background-color: #0b7dda !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recommendations-header {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 1rem !important;
  }
  
  .filter-options {
    width: 100% !important;
  }
  
  .filter-options select {
    flex: 1 !important;
  }
  
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)) !important;
    gap: 1rem !important;
  }
}

@media (max-width: 480px) {
  .recommendations {
    padding: 1rem 0 !important;
  }
  
  .recommendations h2 {
    font-size: 1.5rem !important;
  }
  
  .product-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>