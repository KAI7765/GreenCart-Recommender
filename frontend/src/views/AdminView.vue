<template>
  <div class="admin">
    <div class="container">
      <h2>管理后台</h2>
      <div class="admin-nav">
        <router-link to="/admin/labels" class="admin-nav-link">绿色标签管理</router-link>
        <router-link to="/admin/products" class="admin-nav-link">商品管理</router-link>
        <router-link to="/admin/users" class="admin-nav-link">用户分析</router-link>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminView'
}
</script>

<style scoped>
.admin {
  padding: 2rem 0;
}

.container {
  width: 95%;
  max-width: 1400px;
  margin: 0 auto;
  display: block;
}

.admin h2 {
  margin-bottom: 2rem;
  color: #4CAF50;
  text-align: left;
}

.admin-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 1rem;
  justify-content: flex-start;
}

.admin-nav-link {
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  color: #333;
  font-weight: bold;
  transition: background-color 0.3s;
  font-size: 1rem;
}

.admin-nav-link:hover,
.admin-nav-link.router-link-active {
  background-color: #4CAF50;
  color: white;
}

/* 确保子组件占满容器宽度 */
.router-view {
  width: 100%;
}
</style>