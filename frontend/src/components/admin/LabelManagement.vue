<template>
  <div class="label-management">
    <h3>绿色标签管理</h3>
    <div class="add-label-form">
      <h4>添加新标签</h4>
      <form @submit.prevent="addLabel">
        <div class="form-group">
          <label for="label-name">标签名称</label>
          <input type="text" id="label-name" v-model="newLabel.name" required>
        </div>
        <div class="form-group">
          <label for="label-description">标签描述</label>
          <textarea id="label-description" v-model="newLabel.description" rows="3"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">添加标签</button>
      </form>
    </div>
    <div class="labels-list">
      <h4>标签列表</h4>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>标签名称</th>
            <th>描述</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="label in labels" :key="label.id">
            <td>{{ label.id }}</td>
            <td>{{ label.name }}</td>
            <td>{{ label.description }}</td>
            <td>
              <button @click="editLabel(label)" class="btn btn-secondary">编辑</button>
              <button @click="deleteLabel(label.id)" class="btn btn-danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LabelManagement',
  data() {
    return {
      labels: [],
      newLabel: {
        name: '',
        description: ''
      }
    }
  },
  mounted() {
    this.getLabels()
  },
  methods: {
    async getLabels() {
      try {
        const response = await fetch('/api/admin/labels')
        if (response.ok) {
          this.labels = await response.json()
        }
      } catch (error) {
        console.error('Error getting labels:', error)
      }
    },
    async addLabel() {
      try {
        const response = await fetch('/api/admin/labels', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newLabel)
        })
        
        if (response.ok) {
          this.getLabels()
          this.newLabel = { name: '', description: '' }
        } else {
          const error = await response.json()
          alert(error.message)
        }
      } catch (error) {
        console.error('Error adding label:', error)
        alert('添加标签失败')
      }
    },
    editLabel(label) {
      // 编辑功能实现
      this.newLabel = { ...label }
    },
    async deleteLabel(labelId) {
      if (confirm('确定要删除这个标签吗？')) {
        try {
          const response = await fetch(`/api/admin/labels/${labelId}`, {
            method: 'DELETE'
          })
          
          if (response.ok) {
            this.getLabels()
          }
        } catch (error) {
          console.error('Error deleting label:', error)
          alert('删除标签失败')
        }
      }
    }
  }
}
</script>

<style scoped>
.label-management {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-label-form {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  padding: 0.6rem 1.2rem;
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
  background-color: #2196F3;
  color: white;
  margin-right: 0.5rem;
}

.btn-secondary:hover {
  background-color: #0b7dda;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-danger:hover {
  background-color: #da190b;
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