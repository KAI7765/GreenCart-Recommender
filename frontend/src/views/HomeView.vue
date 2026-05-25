<template>
  <div class="home">
    <div class="hero">
      <div class="container">
        <h2>绿色消费，从这里开始</h2>
        <p>为您推荐符合您需求的绿色产品，让环保成为生活的一部分</p>
        <router-link to="/recommendations" class="btn btn-primary">查看推荐</router-link>
      </div>
    </div>
    <div class="features">
      <div class="container">
        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>精准推荐</h3>
          <p>基于您的消费行为和偏好，为您推荐最适合的绿色产品</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌿</div>
          <h3>绿色认证</h3>
          <p>所有推荐商品均经过绿色认证，确保环保属性真实可靠</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💰</div>
          <h3>性价比优选</h3>
          <p>为您找到价格合理的绿色产品，让环保消费不再昂贵</p>
        </div>
      </div>
    </div>
    <div class="stats">
      <div class="container">
        <div class="stat-item">
          <div class="stat-number">1000+</div>
          <div class="stat-label">绿色商品</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">500+</div>
          <div class="stat-label">活跃用户</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">98%</div>
          <div class="stat-label">用户满意度</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: 80vh;
}

.hero {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  padding: 6rem 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjZmZmZmZmMTAiPjwvcmVjdD4KPHBhdGggZD0iTTAgNUw1IDBaTTYgNEw0IDZaTS0xIDFMMSAtMVoiIHN0cm9rZT0iI2ZmZmZmZiIgc3Ryb2tlLXdpZHRoPSIxIj48L3BhdGg+Cjwvc3ZnPg==');
  opacity: 0.1;
  animation: float 20s linear infinite;
}

@keyframes float {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-20px);
  }
}

.hero h2 {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out;
}

.hero p {
  font-size: 1.2rem;
  margin-bottom: 2.5rem;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out 0.2s both;
}

.btn {
  display: inline-block;
  padding: 1rem 2.5rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
  animation: fadeInUp 1s ease-out 0.4s both;
}

.btn-primary {
  background-color: white;
  color: #4CAF50;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  background-color: #f1f1f1;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.features {
  padding: 6rem 0;
  background-color: #f8f9fa;
}

.feature-card {
  background-color: white;
  padding: 2.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  display: block;
}

.feature-card h3 {
  color: #4CAF50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

.stats {
  padding: 4rem 0;
  background-color: white;
}

.stat-item {
  text-align: center;
  margin-bottom: 2rem;
}

.stat-number {
  font-size: 3rem;
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1.1rem;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero {
    padding: 4rem 0;
  }
  
  .hero h2 {
    font-size: 2rem;
  }
  
  .hero p {
    font-size: 1rem;
  }
  
  .btn {
    padding: 0.8rem 2rem;
  }
  
  .features {
    padding: 4rem 0;
  }
  
  .feature-card {
    padding: 2rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
}

@media (min-width: 768px) {
  .features .container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
  
  .feature-card {
    margin-bottom: 0;
  }
  
  .stats .container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
  
  .stat-item {
    margin-bottom: 0;
  }
}

@media (max-width: 480px) {
  .hero h2 {
    font-size: 1.8rem;
  }
  
  .feature-icon {
    font-size: 2.5rem;
  }
  
  .feature-card h3 {
    font-size: 1.3rem;
  }
}
</style>