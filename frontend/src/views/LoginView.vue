<template>
  <div class="login">
    <div class="container">
      <h2>登录</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="form.username" required>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="form.password" required>
        </div>
        <button type="submit" class="btn btn-primary">登录</button>
        <p class="register-link">还没有账号？<router-link to="/register">立即注册</router-link></p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async login() {
      try {
        console.log('Login method called')
        console.log('Login form:', this.form)
        console.log('Sending login request to:', '/api/user/login')
        
        // 直接测试后端API
        const response = await fetch('http://localhost:5000/api/user/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        })
        
        console.log('Login response status:', response.status)
        if (response.ok) {
          const data = await response.json()
          console.log('Login response data:', data)
          localStorage.setItem('token', data.access_token)
          localStorage.setItem('user', JSON.stringify({
            id: data.user_id,
            role: data.role
          }))
          console.log('Redirecting to /recommendations')
          this.$router.push('/recommendations')
        } else {
          const error = await response.json()
          console.log('Login error:', error)
          alert(error.message)
        }
      } catch (error) {
        console.error('Login error:', error)
        alert(`登录失败，请稍后重试: ${error.message}`)
      }
    }
  }
}
</script>

<style scoped>
.login {
  padding: 4rem 0;
}

.login h2 {
  text-align: center;
  margin-bottom: 2rem;
  color: #4CAF50;
}

form {
  max-width: 400px;
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

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
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

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #4CAF50;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>