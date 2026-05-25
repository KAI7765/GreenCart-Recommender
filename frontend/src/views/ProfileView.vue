<template>
  <div class="profile">
    <div class="container">
      <h2>个人中心</h2>
      <form @submit.prevent="updateProfile">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="profile.username" placeholder="请输入用户名" required>
        </div>

        <div class="form-group">
          <label for="email">邮箱</label>
          <input type="email" id="email" v-model="profile.email" placeholder="请输入邮箱" required>
        </div>

        <div class="form-group">
          <label for="password">新密码（留空则不修改）</label>
          <input type="password" id="password" v-model="profile.password" placeholder="请输入新密码" minlength="6">
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认新密码</label>
          <input type="password" id="confirmPassword" v-model="profile.confirmPassword" placeholder="请再次输入新密码" minlength="6">
        </div>

        <div class="form-group" v-if="error">
          <div class="error-message">{{ error }}</div>
        </div>

        <div class="form-group" v-if="success">
          <div class="success-message">{{ success }}</div>
        </div>

        <div class="button-group">
          <button type="submit" class="btn btn-primary">保存修改</button>
          <button type="button" class="btn btn-secondary" @click="goBack">返回</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileView',
  data() {
    return {
      profile: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      error: '',
      success: ''
    }
  },
  mounted() {
    this.loadCurrentUser()
  },
  methods: {
    loadCurrentUser() {
      const userData = localStorage.getItem('user')
      if (userData) {
        const user = JSON.parse(userData)
        this.profile.username = user.name || user.username || ''
        this.profile.email = user.email || ''
      } else {
        this.$router.push('/login')
      }
    },
    async updateProfile() {
      this.error = ''
      this.success = ''

      // 验证密码匹配
      if (this.profile.password !== this.profile.confirmPassword) {
        this.error = '两次输入的密码不一致'
        return
      }

      // 验证密码长度
      if (this.profile.password && this.profile.password.length < 6) {
        this.error = '密码长度不能少于6位'
        return
      }

      try {
        const user = JSON.parse(localStorage.getItem('user'))
        if (!user) {
          this.$router.push('/login')
          return
        }

        // 构建更新数据
        const updateData = {
          user_id: user.id,
          username: this.profile.username,
          email: this.profile.email
        }

        // 只有填写了新密码才包含密码字段
        if (this.profile.password) {
          updateData.password = this.profile.password
        }

        const response = await fetch('/api/user/profile', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(updateData)
        })

        const result = await response.json()

        if (response.ok) {
          // 更新 localStorage 中的用户信息
          const updatedUser = {
            ...user,
            name: this.profile.username,
            username: this.profile.username,
            email: this.profile.email
          }
          localStorage.setItem('user', JSON.stringify(updatedUser))

          this.success = '个人信息更新成功！'
          this.profile.password = ''
          this.profile.confirmPassword = ''

          // 3秒后清除成功消息
          setTimeout(() => {
            this.success = ''
          }, 3000)
        } else {
          this.error = result.message || '更新失败，请稍后重试'
        }
      } catch (error) {
        console.error('Error updating profile:', error)
        this.error = '更新失败，请检查网络连接'
      }
    },
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.profile {
  padding: 4rem 0;
}

.profile h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #4CAF50;
}

form {
  max-width: 500px;
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
  color: #333;
}

input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

input:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.success-message {
  color: #155724;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  flex: 1;
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

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

@media (max-width: 768px) {
  form {
    padding: 1.5rem;
    margin: 0 1rem;
  }

  .button-group {
    flex-direction: column;
  }
}
</style>
