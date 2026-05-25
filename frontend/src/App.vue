<template>
  <div class="app">
    <nav class="navbar">
      <div class="container">
        <h1 class="logo">绿色产品推荐系统</h1>
        <div class="nav-links" :class="{ 'active': mobileMenuActive }">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/recommendations" class="nav-link">推荐商品</router-link>
          <router-link to="/collection" class="nav-link" v-if="isLoggedIn">我的收藏</router-link>
          <router-link to="/cart" class="nav-link" v-if="isLoggedIn">购物车</router-link>
          <router-link to="/preferences" class="nav-link" v-if="isLoggedIn">偏好设置</router-link>
          <router-link to="/profile" class="nav-link" v-if="isLoggedIn">个人中心</router-link>
          <router-link to="/login" class="nav-link" v-if="!isLoggedIn">登录</router-link>
          <router-link to="/register" class="nav-link" v-if="!isLoggedIn">注册</router-link>
          <router-link to="/admin" class="nav-link" v-if="isAdmin">管理后台</router-link>
          <button @click="logout" class="nav-link logout-btn" v-if="isLoggedIn">退出</button>
        </div>
        <button class="mobile-menu-btn" @click="toggleMobileMenu">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>绿色产品推荐系统</h3>
            <p>致力于为您推荐符合环保理念的绿色产品</p>
          </div>
          <div class="footer-section">
            <h4>快速链接</h4>
            <ul>
              <li><router-link to="/">首页</router-link></li>
              <li><router-link to="/recommendations">推荐商品</router-link></li>
              <li><router-link to="/preferences">偏好设置</router-link></li>
            </ul>
          </div>
          <div class="footer-section">
            <h4>联系我们</h4>
            <p>邮箱: contact@greenproduct.com</p>
            <p>电话: 123-456-7890</p>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© 2026 绿色产品推荐系统</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
      mobileMenuActive: false
    }
  },
  mounted() {
    this.checkLoginStatus()
    window.addEventListener('resize', this.handleResize)
  },
  watch: {
    '$route'() {
      // 当路由变化时，重新检查登录状态
      this.checkLoginStatus()
    }
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    checkLoginStatus() {
      const user = localStorage.getItem('user')
      if (user) {
        const userData = JSON.parse(user)
        this.isLoggedIn = true
        this.isAdmin = userData.role === 'admin'
      }
    },
    logout() {
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      this.isLoggedIn = false
      this.isAdmin = false
      this.mobileMenuActive = false
      this.$router.push('/')
    },
    toggleMobileMenu() {
      this.mobileMenuActive = !this.mobileMenuActive
    },
    handleResize() {
      if (window.innerWidth > 768) {
        this.mobileMenuActive = false
      }
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #4CAF50;
  color: white;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  display: inline-block;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.logout-btn {
  background-color: #4CAF50;
  border: 1px solid white;
  color: white;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #45a049;
}

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 20px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.mobile-menu-btn span {
  display: block;
  width: 100%;
  height: 2px;
  background-color: white;
  transition: all 0.3s ease;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

.footer {
  background-color: #f8f9fa;
  padding: 2rem 0;
  border-top: 1px solid #e9ecef;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3 {
  color: #4CAF50;
  margin-bottom: 1rem;
}

.footer-section h4 {
  color: #333;
  margin-bottom: 1rem;
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 0.5rem;
}

.footer-section ul li a {
  color: #666;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-section ul li a:hover {
  color: #4CAF50;
}

.footer-bottom {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #e9ecef;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: flex;
  }
  
  .nav-links {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background-color: #4CAF50;
    flex-direction: column;
    align-items: center;
    padding: 1rem 0;
    gap: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transform: translateY(-100%);
    opacity: 0;
    pointer-events: none;
    transition: all 0.3s ease;
  }
  
  .nav-links.active {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }
  
  .nav-link {
    width: 100%;
    text-align: center;
    padding: 0.8rem 0;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 1.2rem;
  }
  
  .main-content {
    padding: 1rem 0;
  }
}
</style>