# 绿色产品推荐系统部署文档

## 1. 环境配置

### 1.1 后端环境
- Python 3.8+
- MySQL 5.7+

### 1.2 前端环境
- Node.js 14+
- npm 6+

## 2. 数据库初始化

1. 打开MySQL命令行或MySQL Workbench
2. 执行以下SQL语句创建数据库和表结构：

```bash
mysql -u root -p < sql/create_tables.sql
```

3. 验证数据库是否创建成功：

```sql
SHOW DATABASES;
USE green_product;
SHOW TABLES;
```

## 3. 后端服务启动

1. 进入后端目录：

```bash
cd backend
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 修改数据库配置（可选）：

编辑 `config.py` 文件，修改数据库连接信息：

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password_here@localhost:3306/green_product'
```

4. 启动后端服务：

```bash
python app.py
```

服务将在 `http://localhost:5000` 运行。

## 4. 前端项目运行

1. 进入前端目录：

```bash
cd frontend
```

2. 安装依赖：

```bash
npm install
```

3. 启动前端开发服务器：

```bash
npm run dev
```

前端将在 `http://localhost:3000` 运行。

## 5. 功能测试

### 5.1 用户端测试
1. 注册新用户
2. 登录系统
3. 查看推荐商品
4. 记录用户行为（浏览、购买）
5. 提交反馈（不感兴趣、价格过高）

### 5.2 管理员端测试
1. 登录管理员账号
2. 管理绿色标签（添加、编辑、删除）
3. 管理商品（添加、编辑、添加绿色标签）
4. 查看用户分析数据

### 5.3 API测试

使用Postman或curl测试API接口：

- 注册：POST /user/register
- 登录：POST /user/login
- 获取推荐：GET /recommend/{user_id}
- 记录行为：POST /user/behavior
- 提交反馈：POST /user/feedback
- 管理员获取标签：GET /admin/labels
- 管理员添加标签：POST /admin/labels
- 管理员获取商品：GET /admin/products
- 管理员添加商品：POST /admin/products
- 管理员获取用户：GET /admin/users

## 6. 部署到生产环境

### 6.1 后端部署
1. 使用Gunicorn作为WSGI服务器：

```bash
pip install gunicorn
```

2. 启动服务：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 6.2 前端部署
1. 构建生产版本：

```bash
npm run build
```

2. 将 `dist` 目录部署到Nginx或Apache服务器。

## 7. 常见问题与解决方案

### 7.1 数据库连接失败
- 检查MySQL服务是否运行
- 检查数据库连接配置是否正确
- 检查数据库用户权限

### 7.2 后端服务启动失败
- 检查依赖是否安装完整
- 检查端口是否被占用
- 检查数据库连接是否正常

### 7.3 前端页面无法加载
- 检查后端服务是否运行
- 检查前端代理配置是否正确
- 检查浏览器控制台是否有错误信息

### 7.4 推荐功能不工作
- 检查用户行为数据是否足够
- 检查商品数据是否包含绿色标签
- 检查推荐算法是否正常执行

## 8. 系统功能扩展

- 接入深度学习模型提升推荐精度
- 添加多端适配（移动端、小程序）
- 增加大数据量处理能力
- 集成第三方绿色认证API
- 添加用户偏好设置功能
