<template>
  <div class="user-analysis">
    <h3>用户分析</h3>
    <div class="user-stats">
      <div class="stat-card">
        <h4>总用户数</h4>
        <p class="stat-value">{{ totalUsers }}</p>
      </div>
      <div class="stat-card">
        <h4>潜在有机标签群体</h4>
        <p class="stat-value">{{ organicLabelUsers }}</p>
      </div>
      <div class="stat-card">
        <h4>潜在环保标签群体</h4>
        <p class="stat-value">{{ environmentalLabelUsers }}</p>
      </div>
      <div class="stat-card">
        <h4>潜在可降解标签群体</h4>
        <p class="stat-value">{{ degradableLabelUsers }}</p>
      </div>
      <div class="stat-card">
        <h4>潜在节能标签群体</h4>
        <p class="stat-value">{{ energySavingLabelUsers }}</p>
      </div>
      <div class="stat-card">
        <h4>潜在无添加标签群体</h4>
        <p class="stat-value">{{ noAdditiveLabelUsers }}</p>
      </div>
      <div class="stat-card">
        <h4>潜在可持续标签群体</h4>
        <p class="stat-value">{{ sustainableLabelUsers }}</p>
      </div>
      <div class="stat-card">
        <h4>潜在可回收标签群体</h4>
        <p class="stat-value">{{ recycledLabelUsers }}</p>
      </div>
    </div>
    <div class="user-list">
      <h4>用户列表</h4>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>用户群体</th>
            <th>注册时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.group_name }}</td>
            <td>{{ user.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserAnalysis',
  data() {
    return {
      users: [],
      totalUsers: 0,
      organicLabelUsers: 0,
      environmentalLabelUsers: 0,
      degradableLabelUsers: 0,
      energySavingLabelUsers: 0,
      noAdditiveLabelUsers: 0,
      sustainableLabelUsers: 0,
      recycledLabelUsers: 0
    }
  },
  mounted() {
    this.getUsers()
  },
  methods: {
    async getUsers() {
      try {
        const response = await fetch('/api/admin/users')
        if (response.ok) {
          const data = await response.json()
          this.users = data.users
          this.totalUsers = data.total
          this.organicLabelUsers = data.organicLabel || 0
          this.environmentalLabelUsers = data.environmentalLabel || 0
          this.degradableLabelUsers = data.degradableLabel || 0
          this.energySavingLabelUsers = data.energySavingLabel || 0
          this.noAdditiveLabelUsers = data.noAdditiveLabel || 0
          this.sustainableLabelUsers = data.sustainableLabel || 0
          this.recycledLabelUsers = data.recycledLabel || 0
        }
      } catch (error) {
        console.error('Error getting users:', error)
      }
    }
  }
}
</script>

<style scoped>
.user-analysis {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-card h4 {
  margin-bottom: 1rem;
  color: #666;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #4CAF50;
}

.user-list {
  margin-top: 2rem;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.table th, .table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

.table th {
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
}

.table tr:hover {
  background-color: #f1f1f1;
}
</style>