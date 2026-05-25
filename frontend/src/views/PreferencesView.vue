<template>
  <div class="preferences">
    <div class="container">
      <h2>个人偏好设置</h2>
      <form @submit.prevent="savePreferences">
        <div class="form-group">
          <label>绿色消费偏好</label>
          <div class="preference-options">
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.greenLabels.organic"> 有机产品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.greenLabels.degradable"> 可降解产品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.greenLabels.energySaving"> 节能产品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.greenLabels.environmental"> 环保产品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.greenLabels.noAdditive"> 无添加产品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.greenLabels.sustainable"> 可持续发展产品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.greenLabels.recycled"> 可回收产品
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label for="price-range">价格偏好</label>
          <input type="range" id="price-range" v-model.number="preferences.priceRange" min="0" max="2000" step="100">
          <span class="price-value">¥{{ preferences.priceRange }} 以下</span>
        </div>
        
        <div class="form-group">
          <label>推荐优先级</label>
          <select v-model="preferences.priority">
            <option value="greenMatch">绿色属性匹配度</option>
            <option value="price">价格优先</option>
            <option value="sales">销量优先</option>
            <option value="rating">评分优先</option>
            <option value="newest">最新产品</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>商品分类偏好</label>
          <div class="preference-options">
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.food"> 食品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.daily"> 日用品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.home"> 家居用品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.baby"> 母婴用品
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.appliance"> 家电
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.clothing"> 服装
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.beauty"> 美妆
            </label>
            <label class="checkbox-option">
              <input type="checkbox" v-model="preferences.categories.sports"> 运动用品
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label>环保程度偏好</label>
          <div class="preference-options">
            <label class="radio-option">
              <input type="radio" v-model="preferences.greenLevel" value="high"> 高环保标准
            </label>
            <label class="radio-option">
              <input type="radio" v-model="preferences.greenLevel" value="medium"> 中等环保标准
            </label>
            <label class="radio-option">
              <input type="radio" v-model="preferences.greenLevel" value="low"> 基础环保标准
            </label>
          </div>
        </div>
        
        <div class="form-group">
          <label>品牌偏好</label>
          <input type="text" v-model="preferences.brandPreference" placeholder="输入您喜欢的品牌，多个品牌用逗号分隔">
        </div>
        
        <div class="form-group">
          <label>个性化推荐开关</label>
          <label class="switch">
            <input type="checkbox" v-model="preferences.personalized">
            <span class="slider round"></span>
          </label>
          <span class="switch-label">开启个性化推荐</span>
        </div>
        
        <button type="submit" class="btn btn-primary">保存设置</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PreferencesView',
  data() {
    return {
      preferences: {
        greenLabels: {
          organic: false,
          degradable: false,
          energySaving: false,
          environmental: false,
          noAdditive: false,
          sustainable: false,
          recycled: false
        },
        priceRange: 500,
        priority: 'greenMatch',
        categories: {
          food: false,
          daily: false,
          home: false,
          baby: false,
          appliance: false,
          clothing: false,
          beauty: false,
          sports: false
        },
        greenLevel: 'medium',
        brandPreference: '',
        personalized: true
      }
    }
  },
  mounted() {
    console.log('PreferencesView mounted')
    this.loadPreferences()
  },
  methods: {
    loadPreferences() {
      const saved = localStorage.getItem('preferences')
      if (saved) {
        this.preferences = JSON.parse(saved)
      }
    },
    savePreferences() {
      localStorage.setItem('preferences', JSON.stringify(this.preferences))
      // 发送偏好设置到后端，以便后端推荐系统使用
      this.sendPreferencesToBackend()
      this.$router.push('/recommendations')
    },
    async sendPreferencesToBackend() {
      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) return
        
        await fetch('/api/user/preferences', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            user_id: user.id,
            preferences: this.preferences
          })
        })
      } catch (error) {
        console.error('Error sending preferences:', error)
      }
    }
  }
}
</script>

<style scoped>
.preferences {
  padding: 4rem 0;
}

.preferences h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #4CAF50;
}

form {
  max-width: 600px;
  margin: 0 auto;
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.preference-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.checkbox-option,
.radio-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-right: 1rem;
}

input[type="range"] {
  width: 100%;
  margin: 0.5rem 0;
}

.price-value {
  display: block;
  text-align: center;
  font-weight: bold;
  color: #4CAF50;
}

select,
input[type="text"] {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #4CAF50;
}

input:focus + .slider {
  box-shadow: 0 0 1px #4CAF50;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

.switch-label {
  margin-left: 10px;
  font-weight: normal;
}

.btn {
  display: block;
  width: 100%;
  padding: 0.8rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

/* 响应式设计 */
@media (max-width: 768px) {
  form {
    padding: 1.5rem;
  }
  
  .preference-options {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .checkbox-option,
  .radio-option {
    margin-right: 0;
  }
}
</style>