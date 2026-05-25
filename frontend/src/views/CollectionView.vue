<template>
  <div class="collection">
    <div class="container">
      <h2>我的收藏</h2>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="collections.length === 0" class="no-collections">
        <p>暂无收藏商品</p>
      </div>
      <div v-else class="product-grid">
        <div v-for="product in collections" :key="product.id" class="product-card">
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
              <button @click="removeFromCollection(product.id)" class="btn btn-danger">取消收藏</button>
              <button @click="addToCart(product.id)" class="btn btn-primary">加入购物车</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CollectionView',
  data() {
    return {
      collections: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.getCollections()
  },
  methods: {
    async getCollections() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          this.error = '请先登录'
          this.loading = false
          return
        }
        
        const response = await fetch(`/api/user/collection?user_id=${user.id}`)
        if (response.ok) {
          this.collections = await response.json()
        } else {
          this.error = '获取收藏列表失败'
        }
      } catch (error) {
        console.error('Error getting collections:', error)
        this.error = '获取收藏列表失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    async removeFromCollection(productId) {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) return
        
        const response = await fetch(`/api/user/collection/${productId}?user_id=${user.id}`, {
          method: 'DELETE'
        })
        if (response.ok) {
          // 从列表中移除
          this.collections = this.collections.filter(p => p.id !== productId)
          alert('取消收藏成功')
        }
      } catch (error) {
        console.error('Error removing from collection:', error)
        alert('取消收藏失败，请稍后重试')
      }
    },
    async addToCart(productId) {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          alert('请先登录')
          return
        }
        
        const response = await fetch('/api/user/cart', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: user.id,
            product_id: productId,
            quantity: 1
          })
        })
        if (response.ok) {
          alert('加入购物车成功')
        }
      } catch (error) {
        console.error('Error adding to cart:', error)
        alert('加入购物车失败，请稍后重试')
      }
    },
    goToDetail(productId) {
      this.$router.push(`/product/${productId}`)
    }
  }
}
</script>

<style scoped>
.collection {
  padding: 2rem 0 !important;
  min-height: 80vh !important;
}

.container {
  width: 95% !important;
  max-width: 1400px !important;
  margin: 0 auto !important;
  display: block !important;
}

.collection h2 {
  color: #4CAF50 !important;
  font-size: 1.8rem !important;
  margin-bottom: 2rem !important;
  text-align: left !important;
  padding-bottom: 1rem !important;
  border-bottom: 1px solid #e9ecef !important;
}

.loading, .error, .no-collections {
  text-align: center !important;
  padding: 4rem !important;
  font-size: 1.2rem !important;
}

.error {
  color: #f44336 !important;
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

.btn-danger {
  background-color: #f44336 !important;
  color: white !important;
}

.btn-danger:hover {
  background-color: #d32f2f !important;
}

@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)) !important;
    gap: 1rem !important;
  }
}

@media (max-width: 480px) {
  .collection {
    padding: 1rem 0 !important;
  }
  
  .collection h2 {
    font-size: 1.5rem !important;
  }
  
  .product-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>