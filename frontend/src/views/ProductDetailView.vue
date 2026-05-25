<template>
  <div class="product-detail">
    <div class="container">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="!product" class="no-product">商品不存在</div>
      <div v-else class="product-content">
        <div class="product-images">
          <img :src="product.image_url || 'https://via.placeholder.com/600'" :alt="product.name" class="main-image">
        </div>
        <div class="product-info">
          <h1 class="product-name">{{ product.name }}</h1>
          <div class="product-labels">
            <span v-for="label in product.green_labels" :key="label" class="green-label">{{ label }}</span>
          </div>
          <p class="product-price">¥{{ product.price.toFixed(2) }}</p>
          <div class="product-meta">
            <span class="sales">销量: {{ product.sales }}</span>
            <span class="rating">评分: {{ product.rating.toFixed(1) }}</span>
          </div>
          <div class="product-description">
            <h3>商品描述</h3>
            <p>{{ product.description }}</p>
          </div>
          <div class="product-actions">
            <button @click="addToCart" class="btn btn-primary">加入购物车</button>
            <button @click="toggleCollection" class="btn btn-secondary">
              {{ isCollected ? '取消收藏' : '收藏' }}
            </button>
            <button @click="recordBehavior('purchase')" class="btn btn-success">立即购买</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductDetailView',
  data() {
    return {
      product: null,
      loading: true,
      error: null,
      isCollected: false
    }
  },
  mounted() {
    this.getProductDetail()
    this.checkCollectionStatus()
  },
  methods: {
    async getProductDetail() {
      try {
        const productId = this.$route.params.id
        // 这里应该调用API获取商品详情，暂时使用模拟数据
        // 实际项目中应该调用后端API
        const response = await fetch(`/api/admin/products`)
        if (response.ok) {
          const products = await response.json()
          this.product = products.find(p => p.id == productId)
          if (!this.product) {
            this.error = '商品不存在'
          }
        } else {
          this.error = '获取商品详情失败'
        }
      } catch (error) {
        console.error('Error getting product detail:', error)
        this.error = '获取商品详情失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    async checkCollectionStatus() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) return
        
        const response = await fetch(`/api/user/collection?user_id=${user.id}`)
        if (response.ok) {
          const collections = await response.json()
          const productId = this.$route.params.id
          this.isCollected = collections.some(p => p.id == productId)
        }
      } catch (error) {
        console.error('Error checking collection status:', error)
      }
    },
    async toggleCollection() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          alert('请先登录')
          return
        }
        
        const productId = this.$route.params.id
        if (this.isCollected) {
          // 取消收藏
          const response = await fetch(`/api/user/collection/${productId}?user_id=${user.id}`, {
            method: 'DELETE'
          })
          if (response.ok) {
            this.isCollected = false
            alert('取消收藏成功')
          }
        } else {
          // 添加收藏
          const response = await fetch('/api/user/collection', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              user_id: user.id,
              product_id: productId
            })
          })
          if (response.ok) {
            this.isCollected = true
            alert('收藏成功')
          }
        }
      } catch (error) {
        console.error('Error toggling collection:', error)
        alert('操作失败，请稍后重试')
      }
    },
    async addToCart() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          alert('请先登录')
          return
        }
        
        const productId = this.$route.params.id
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
    async recordBehavior(behaviorType) {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) return
        
        const productId = this.$route.params.id
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
    }
  }
}
</script>

<style scoped>
.product-detail {
  padding: 2rem 0;
  min-height: 80vh;
}

.container {
  width: 95%;
  max-width: 1200px;
  margin: 0 auto;
}

.loading, .error, .no-product {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
}

.error {
  color: #f44336;
}

.product-content {
  display: flex;
  gap: 2rem;
  margin-top: 2rem;
}

.product-images {
  flex: 1;
  max-width: 500px;
}

.main-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.product-info {
  flex: 1;
  min-width: 300px;
}

.product-name {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #333;
}

.product-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.green-label {
  background-color: #4CAF50;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.product-price {
  font-size: 2rem;
  font-weight: bold;
  color: #f44336;
  margin-bottom: 1.5rem;
}

.product-meta {
  display: flex;
  gap: 2rem;
  font-size: 1rem;
  color: #666;
  margin-bottom: 2rem;
}

.product-description {
  margin-bottom: 2rem;
}

.product-description h3 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #333;
}

.product-description p {
  line-height: 1.6;
  color: #555;
}

.product-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  flex: 1;
  text-align: center;
}

.btn-primary {
  background-color: #2196F3;
  color: white;
}

.btn-primary:hover {
  background-color: #0b7dda;
}

.btn-secondary {
  background-color: #FFC107;
  color: #333;
}

.btn-secondary:hover {
  background-color: #ffb300;
}

.btn-success {
  background-color: #4CAF50;
  color: white;
}

.btn-success:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .product-content {
    flex-direction: column;
  }
  
  .product-images {
    max-width: 100%;
  }
  
  .product-actions {
    flex-direction: column;
  }
}
</style>