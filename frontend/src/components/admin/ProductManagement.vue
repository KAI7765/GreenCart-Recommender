<template>
  <div class="product-management">
    <h3>商品管理</h3>
    <div class="add-product-form">
      <h4>添加新商品</h4>
      <form @submit.prevent="addProduct">
        <div class="form-group">
          <label for="product-name">商品名称</label>
          <input type="text" id="product-name" v-model="newProduct.name" required>
        </div>
        <div class="form-group">
          <label for="product-price">价格</label>
          <input type="number" id="product-price" v-model.number="newProduct.price" required min="0">
        </div>
        <div class="form-group">
          <label for="product-category">分类</label>
          <input type="text" id="product-category" v-model="newProduct.category" required>
        </div>
        <div class="form-group">
          <label for="product-description">描述</label>
          <textarea id="product-description" v-model="newProduct.description" rows="3"></textarea>
        </div>
        <div class="form-group">
          <label for="product-image">图片URL</label>
          <input type="text" id="product-image" v-model="newProduct.image_url">
        </div>
        <div class="form-group">
          <label for="product-sales">销量</label>
          <input type="number" id="product-sales" v-model.number="newProduct.sales" min="0">
        </div>
        <div class="form-group">
          <label for="product-rating">评分</label>
          <input type="number" id="product-rating" v-model.number="newProduct.rating" min="0" max="5" step="0.1">
        </div>
        <button type="submit" class="btn btn-primary">添加商品</button>
      </form>
    </div>
    <div class="batch-import-form">
      <h4>批量导入商品</h4>
      <div class="form-group">
        <label for="file-upload">选择JSON文件</label>
        <input type="file" id="file-upload" ref="fileInput" @change="handleFileChange" accept=".json">
      </div>
      <button @click="batchImport" class="btn btn-success" :disabled="!selectedFile">批量导入</button>
      <p class="help-text">请上传包含商品数据的JSON文件，格式参考：{"products": [{"name": "商品名称", "price": 19.9, "category": "食品", ...}]}</p>
      <button @click="testImport" class="btn btn-info">测试导入</button>
      <button @click="directImport" class="btn btn-warning">直接导入</button>
    </div>
    <div class="products-list">
      <div class="list-header">
        <h4>商品列表</h4>
        <button @click="batchDelete" class="btn btn-danger" :disabled="selectedProducts.length === 0">批量删除</button>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>
              <input type="checkbox" v-model="selectAll" @change="handleSelectAll">
            </th>
            <th>ID</th>
            <th>名称</th>
            <th>价格</th>
            <th>分类</th>
            <th>绿色标签</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>
              <input type="checkbox" v-model="selectedProducts" :value="product.id">
            </td>
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>¥{{ product.price.toFixed(2) }}</td>
            <td>{{ product.category }}</td>
            <td>
              <span v-for="label in product.green_labels" :key="label" class="green-label">{{ label }}</span>
            </td>
            <td>
              <button @click="editProduct(product)" class="btn btn-secondary">编辑</button>
              <button @click="addLabelToProduct(product)" class="btn btn-success">添加标签</button>
              <button @click="deleteProduct(product.id)" class="btn btn-danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- 添加标签弹窗 -->
    <div v-if="showLabelModal" class="modal">
      <div class="modal-content">
        <h4>为商品添加标签</h4>
        <form @submit.prevent="saveLabelToProduct">
          <div class="form-group">
            <label for="label-select">选择标签</label>
            <select id="label-select" v-model="selectedLabelId" required>
              <option value="">请选择标签</option>
              <option v-for="label in labels" :key="label.id" :value="label.id">{{ label.name }}</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showLabelModal = false" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">确认</button>
          </div>
        </form>
      </div>
    </div>
    <!-- 编辑商品弹窗 -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h4>编辑商品</h4>
        <form @submit.prevent="saveEditProduct">
          <div class="form-group">
            <label for="edit-product-name">商品名称</label>
            <input type="text" id="edit-product-name" v-model="currentEditProduct.name" required>
          </div>
          <div class="form-group">
            <label for="edit-product-price">价格</label>
            <input type="number" id="edit-product-price" v-model.number="currentEditProduct.price" required min="0">
          </div>
          <div class="form-group">
            <label for="edit-product-category">分类</label>
            <input type="text" id="edit-product-category" v-model="currentEditProduct.category" required>
          </div>
          <div class="form-group">
            <label for="edit-product-description">描述</label>
            <textarea id="edit-product-description" v-model="currentEditProduct.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label for="edit-product-image">图片URL</label>
            <input type="text" id="edit-product-image" v-model="currentEditProduct.image_url">
          </div>
          <div class="form-group">
            <label for="edit-product-sales">销量</label>
            <input type="number" id="edit-product-sales" v-model.number="currentEditProduct.sales" min="0">
          </div>
          <div class="form-group">
            <label for="edit-product-rating">评分</label>
            <input type="number" id="edit-product-rating" v-model.number="currentEditProduct.rating" min="0" max="5" step="0.1">
          </div>
          <div class="modal-actions">
            <button type="button" @click="showEditModal = false" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductManagement',
  data() {
    return {
      products: [],
      labels: [],
      newProduct: {
        name: '',
        price: 0,
        category: '',
        description: '',
        image_url: '',
        sales: 0,
        rating: 0
      },
      currentEditProduct: {
        id: '',
        name: '',
        price: 0,
        category: '',
        description: '',
        image_url: '',
        sales: 0,
        rating: 0
      },
      showLabelModal: false,
      showEditModal: false,
      selectedProductId: null,
      selectedLabelId: null,
      selectedFile: null,
      selectedProducts: [],
      selectAll: false
    }
  },
  mounted() {
    this.getProducts()
    this.getLabels()
  },
  methods: {
    async getProducts() {
      try {
        console.log('Fetching products from:', '/api/admin/products')
        const response = await fetch('/api/admin/products')
        console.log('Response status:', response.status)
        if (response.ok) {
          const data = await response.json()
          console.log('Products data:', data)
          this.products = data
        } else {
          console.error('Error response:', response)
        }
      } catch (error) {
        console.error('Error getting products:', error)
      }
    },
    async getLabels() {
      try {
        console.log('Fetching labels from:', '/api/admin/labels')
        const response = await fetch('/api/admin/labels')
        console.log('Response status:', response.status)
        if (response.ok) {
          const data = await response.json()
          console.log('Labels data:', data)
          this.labels = data
        } else {
          console.error('Error response:', response)
        }
      } catch (error) {
        console.error('Error getting labels:', error)
      }
    },
    async addProduct() {
      try {
        const response = await fetch('/api/admin/products', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.newProduct)
        })
        
        if (response.ok) {
          this.getProducts()
          this.newProduct = {
            name: '',
            price: 0,
            category: '',
            description: '',
            image_url: '',
            sales: 0,
            rating: 0
          }
        } else {
          const error = await response.json()
          alert(error.message)
        }
      } catch (error) {
        console.error('Error adding product:', error)
        alert('添加商品失败')
      }
    },
    editProduct(product) {
      // 编辑功能实现
      this.currentEditProduct = { ...product }
      this.showEditModal = true
    },
    async saveEditProduct() {
      try {
        const response = await fetch(`/api/admin/products/${this.currentEditProduct.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.currentEditProduct)
        })
        
        if (response.ok) {
          this.getProducts()
          this.showEditModal = false
        } else {
          const error = await response.json()
          alert(error.message)
        }
      } catch (error) {
        console.error('Error updating product:', error)
        alert('编辑商品失败')
      }
    },
    async deleteProduct(productId) {
      if (!confirm('确定要删除这个商品吗？')) return
      
      try {
        const response = await fetch(`/api/admin/products/${productId}`, {
          method: 'DELETE'
        })
        
        if (response.ok) {
          this.getProducts()
        } else {
          const error = await response.json()
          alert(error.message)
        }
      } catch (error) {
        console.error('Error deleting product:', error)
        alert('删除商品失败')
      }
    },
    addLabelToProduct(product) {
      this.selectedProductId = product.id
      this.showLabelModal = true
    },
    async saveLabelToProduct() {
      try {
        const response = await fetch(`/api/admin/products/${this.selectedProductId}/labels`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ label_id: this.selectedLabelId })
        })
        
        if (response.ok) {
          this.getProducts()
          this.showLabelModal = false
          this.selectedProductId = null
          this.selectedLabelId = null
        } else {
          const error = await response.json()
          alert(error.message)
        }
      } catch (error) {
        console.error('Error adding label to product:', error)
        alert('添加标签失败')
      }
    },
    handleFileChange(event) {
      this.selectedFile = event.target.files[0]
    },
    async batchImport() {
      if (!this.selectedFile) {
        alert('请选择要导入的JSON文件')
        return
      }
      
      console.log('Selected file:', this.selectedFile)
      console.log('File name:', this.selectedFile.name)
      console.log('File type:', this.selectedFile.type)
      console.log('File size:', this.selectedFile.size)
      
      try {
        const reader = new FileReader()
        reader.onload = async (e) => {
          try {
            console.log('File content length:', e.target.result.length)
            console.log('First 500 characters:', e.target.result.substring(0, 500))
            
            // 检查文件内容是否以HTML开头
            if (e.target.result.trim().startsWith('<!DOCTYPE') || e.target.result.trim().startsWith('<html')) {
              console.error('File is HTML, not JSON:', e.target.result.substring(0, 200))
              alert('选择的文件不是JSON文件，而是HTML文件，请重新选择')
              return
            }
            
            const data = JSON.parse(e.target.result)
            console.log('Parsed data:', data)
            
            // 检查解析后的数据是否包含products属性
            if (!data || !data.products || !Array.isArray(data.products)) {
              console.error('Invalid JSON structure:', data)
              alert('JSON文件结构错误，缺少products数组')
              return
            }
            
            console.log('Sending data to:', '/api/admin/import-data')
            const response = await fetch('/api/admin/import-data', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
            })
            
            console.log('Response status:', response.status)
            if (response.ok) {
              const result = await response.json()
              console.log('Import result:', result)
              alert(result.message)
              this.getProducts()
              this.selectedFile = null
              this.$refs.fileInput.value = ''
            } else {
              console.error('Error response status:', response.status)
              // 尝试解析错误信息
              try {
                const error = await response.json()
                alert(error.message)
              } catch (e) {
                // 如果响应不是JSON格式，直接显示错误状态
                alert(`服务器返回错误: ${response.status} ${response.statusText}`)
              }
            }
          } catch (error) {
            console.error('Error parsing JSON file:', error)
            alert(`JSON文件格式错误: ${error.message}`)
          }
        }
        reader.readAsText(this.selectedFile, 'utf-8')
      } catch (error) {
        console.error('Error during batch import:', error)
        alert('批量导入失败')
      }
    },
    async testImport() {
      try {
        // 直接测试后端API，使用固定的JSON文件路径
        const response = await fetch('http://localhost:5000/api/admin/import-data', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "products": [
              {
                "name": "测试商品1",
                "price": 19.90,
                "category": "食品",
                "description": "测试商品1的描述",
                "image_url": "https://img.freepik.com/free-photo/fresh-organic-vegetables-in-a-box_1150-38087.jpg",
                "sales": 100,
                "rating": 4.5
              },
              {
                "name": "测试商品2",
                "price": 29.90,
                "category": "家居用品",
                "description": "测试商品2的描述",
                "image_url": "https://img.freepik.com/free-photo/corn-starch-biodegradable-tableware-set_23-2148875989.jpg",
                "sales": 200,
                "rating": 4.6
              }
            ]
          })
        })
        
        if (response.ok) {
          const result = await response.json()
          alert(result.message)
          this.getProducts()
        } else {
          const error = await response.json()
          alert(error.message)
        }
      } catch (error) {
        console.error('Error during test import:', error)
        alert('测试导入失败')
      }
    },
    async directImport() {
      try {
        // 直接从文件系统读取green_products_50.json文件
        const response = await fetch('/green_products_50.json')
        console.log('Fetch JSON file status:', response.status)
        if (response.ok) {
          const data = await response.json()
          console.log('JSON file data:', data)
          
          // 发送到后端导入接口
          const importResponse = await fetch('/api/admin/import-data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          })
          
          if (importResponse.ok) {
            const result = await importResponse.json()
            alert(result.message)
            this.getProducts()
          } else {
            const error = await importResponse.json()
            alert(error.message)
          }
        } else {
          alert('无法读取green_products_50.json文件')
        }
      } catch (error) {
        console.error('Error during direct import:', error)
        alert('直接导入失败')
      }
    },
    handleSelectAll() {
      if (this.selectAll) {
        this.selectedProducts = this.products.map(product => product.id)
      } else {
        this.selectedProducts = []
      }
    },
    async batchDelete() {
      if (this.selectedProducts.length === 0) return
      
      if (!confirm('确定要删除选中的商品吗？')) return
      
      try {
        const response = await fetch('/api/admin/products/batch-delete', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ product_ids: this.selectedProducts })
        })
        
        if (response.ok) {
          this.getProducts()
          this.selectedProducts = []
          this.selectAll = false
        } else {
          const error = await response.json()
          alert(error.message)
        }
      } catch (error) {
        console.error('Error deleting products:', error)
        alert('批量删除失败')
      }
    }
  }
}
</script>

<style scoped>
.product-management {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-product-form {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.batch-import-form {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e9ecef;
}

.help-text {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #666;
  font-style: italic;
}

.btn-success {
  background-color: #4CAF50;
  color: white;
  margin-top: 1rem;
}

.btn-success:hover {
  background-color: #45a049;
}

.btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input, textarea, select {
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

.btn-success {
  background-color: #4CAF50;
  color: white;
  margin-right: 0.5rem;
}

.btn-success:hover {
  background-color: #45a049;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-danger:hover {
  background-color: #d32f2f;
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

.green-label {
  background-color: #4CAF50;
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  margin-right: 0.5rem;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.table th input[type="checkbox"],
.table td input[type="checkbox"] {
  width: auto;
  margin: 0;
  cursor: pointer;
}

.table th:first-child,
.table td:first-child {
  text-align: center;
  width: 60px;
}
</style>