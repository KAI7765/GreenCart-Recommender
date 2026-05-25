<template>
  <div class="cart">
    <div class="container">
      <h2>我的购物车</h2>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="cartItems.length === 0" class="no-items">
        <p>购物车为空</p>
      </div>
      <div v-else class="cart-content">
        <div class="cart-items">
          <div v-for="item in cartItems" :key="item.id" class="cart-item">
            <div class="item-checkbox">
              <input type="checkbox" v-model="item.checked" @change="updateSelectedItems">
            </div>
            <div class="item-image">
              <img :src="item.image_url || 'https://via.placeholder.com/100'" :alt="item.name">
            </div>
            <div class="item-info">
              <h3>{{ item.name }}</h3>
              <div class="item-labels">
                <span v-for="label in item.green_labels" :key="label" class="green-label">{{ label }}</span>
              </div>
              <p class="item-price">¥{{ item.price.toFixed(2) }}</p>
            </div>
            <div class="item-quantity">
              <button @click="updateQuantity(item.id, item.quantity - 1)" class="quantity-btn" :disabled="item.quantity <= 1">-</button>
              <span class="quantity">{{ item.quantity }}</span>
              <button @click="updateQuantity(item.id, item.quantity + 1)" class="quantity-btn">+</button>
            </div>
            <div class="item-subtotal">
              ¥{{ item.subtotal.toFixed(2) }}
            </div>
            <div class="item-actions">
              <button @click="removeFromCart(item.id)" class="btn btn-danger">删除</button>
            </div>
          </div>
        </div>
        <div class="cart-summary">
          <h3>购物车总计</h3>
          <div class="summary-item">
            <span>已选商品:</span>
            <span>{{ selectedItemsCount }}</span>
          </div>
          <div class="summary-item">
            <span>总金额:</span>
            <span class="total-price">¥{{ selectedTotalAmount.toFixed(2) }}</span>
          </div>
          <button class="btn btn-primary btn-checkout" :disabled="selectedItemsCount === 0">立即结算</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CartView',
  data() {
    return {
      cartItems: [],
      totalAmount: 0,
      loading: true,
      error: null
    }
  },
  computed: {
    totalItems() {
      return this.cartItems.reduce((total, item) => total + item.quantity, 0)
    },
    selectedItemsCount() {
      return this.cartItems
        .filter(item => item.checked)
        .reduce((total, item) => total + item.quantity, 0)
    },
    selectedTotalAmount() {
      return this.cartItems
        .filter(item => item.checked)
        .reduce((total, item) => total + item.subtotal, 0)
    }
  },
  mounted() {
    this.getCart()
  },
  methods: {
    async getCart() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          this.error = '请先登录'
          this.loading = false
          return
        }
        
        const response = await fetch(`/api/user/cart?user_id=${user.id}`)
        if (response.ok) {
          const data = await response.json()
          // 为每个商品添加checked属性
          this.cartItems = data.items.map(item => ({
            ...item,
            checked: false
          }))
          this.totalAmount = data.total
        } else {
          this.error = '获取购物车失败'
        }
      } catch (error) {
        console.error('Error getting cart:', error)
        this.error = '获取购物车失败，请稍后重试'
      } finally {
        this.loading = false
      }
    },
    updateSelectedItems() {
      // 当选中状态改变时，自动更新计算属性
    },
    async updateQuantity(productId, quantity) {
      if (quantity <= 0) return
      
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) return
        
        const response = await fetch(`/api/user/cart/${productId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: user.id,
            quantity: quantity
          })
        })
        if (response.ok) {
          // 重新获取购物车
          this.getCart()
        }
      } catch (error) {
        console.error('Error updating quantity:', error)
        alert('更新数量失败，请稍后重试')
      }
    },
    async removeFromCart(productId) {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) return
        
        const response = await fetch(`/api/user/cart/${productId}?user_id=${user.id}`, {
          method: 'DELETE'
        })
        if (response.ok) {
          // 重新获取购物车
          this.getCart()
        }
      } catch (error) {
        console.error('Error removing from cart:', error)
        alert('删除失败，请稍后重试')
      }
    }
  }
}
</script>

<style scoped>
.cart {
  padding: 2rem 0;
  min-height: 80vh;
}

.container {
  width: 95%;
  max-width: 1200px;
  margin: 0 auto;
}

.cart h2 {
  color: #4CAF50;
  font-size: 1.8rem;
  margin-bottom: 2rem;
  text-align: left;
}

.loading, .error, .no-items {
  text-align: center;
  padding: 4rem;
  font-size: 1.2rem;
}

.error {
  color: #f44336;
}

.cart-content {
  display: flex;
  gap: 2rem;
}

.cart-items {
  flex: 1;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-checkbox {
  flex: 0 0 40px;
  margin-right: 1rem;
  display: flex;
  align-items: center;
}

.item-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.item-image {
  flex: 0 0 100px;
  margin-right: 1.5rem;
}

.item-image img {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}

.item-info {
  flex: 1;
}

.item-info h3 {
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.item-labels {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-bottom: 0.5rem;
}

.green-label {
  background-color: #4CAF50;
  color: white;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  font-size: 0.7rem;
}

.item-price {
  font-weight: bold;
  color: #f44336;
  margin: 0;
}

.item-quantity {
  flex: 0 0 120px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.quantity-btn {
  width: 30px;
  height: 30px;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quantity-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.quantity {
  font-weight: bold;
  min-width: 30px;
  text-align: center;
}

.item-subtotal {
  flex: 0 0 100px;
  font-weight: bold;
  text-align: right;
}

.item-actions {
  flex: 0 0 80px;
  margin-left: 1rem;
}

.cart-summary {
  flex: 0 0 300px;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  height: fit-content;
}

.cart-summary h3 {
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e9ecef;
}

.total-price {
  font-weight: bold;
  font-size: 1.2rem;
  color: #f44336;
}

.btn {
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-danger {
  background-color: #f44336;
  color: white;
  width: 100%;
}

.btn-danger:hover {
  background-color: #d32f2f;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
  width: 100%;
  padding: 0.8rem;
  font-size: 1.1rem;
  margin-top: 1.5rem;
}

.btn-primary:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .cart-content {
    flex-direction: column;
  }
  
  .cart-summary {
    flex: 1;
  }
  
  .cart-item {
    flex-wrap: wrap;
  }
  
  .item-actions {
    margin-left: 0;
    margin-top: 1rem;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .cart {
    padding: 1rem 0;
  }
  
  .cart h2 {
    font-size: 1.5rem;
  }
  
  .cart-items {
    padding: 1rem;
  }
  
  .cart-item {
    padding: 0.5rem;
  }
}
</style>