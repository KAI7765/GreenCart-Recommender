# GreenCart Recommender

> A personalized green product recommendation system based on e-commerce user behavior analysis.

> 基于用户行为分析的绿色产品个性化推荐系统。

---

## Introduction | 项目简介

GreenCart Recommender is a Python-powered recommendation system designed to address the challenge of matching eco-conscious consumers with green products in e-commerce platforms. By analyzing user behavior patterns and applying clustering algorithms, the system accurately identifies user segments and delivers personalized green product recommendations.

本系统围绕电商绿色产品个性化推荐展开，通过分析用户行为数据并应用聚类算法，精准划分用户群体，实现绿色商品的个性化推荐。

---

## Tech Stack | 技术栈

| Layer | Technology |
|-------|-----------|
| **Backend** | Python, Flask |
| **Frontend** | Vue 3, Vite |
| **Database** | MySQL 5.7+ |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (K-means, Collaborative Filtering) |

---

## Features | 功能特性

### User-facing | 用户端
- User registration & authentication | 用户注册登录
- Personalized green product recommendations | 个性化绿色商品推荐
- Behavior tracking (browsing, purchasing) | 用户行为记录（浏览、购买）
- Feedback submission (not interested, overpriced) | 反馈提交（不感兴趣、价格过高）

### Admin-facing | 管理员端
- Green label management | 绿色标签管理
- Product management with green labeling | 商品管理及绿色标签标注
- User analytics dashboard | 用户数据分析

### Algorithm | 算法特色
- K-means user segmentation (active green, potential green, price-sensitive green) | K-means 用户群体划分
- Collaborative filtering & content-based recommendation | 协同过滤与基于内容推荐
- Price-weighted recommendation strategy | 价格加权推荐策略

---

## Installation | 安装步骤

### Prerequisites | 前置要求

- Python 3.8+
- MySQL 5.7+
- Node.js 14+
- npm 6+

### 1. Database Initialization | 数据库初始化

```bash
mysql -u root -p < sql/create_tables.sql
```

### 2. Backend Setup | 后端配置

```bash
cd backend
pip install -r requirements.txt
```

Edit `backend/config.py` to configure your database connection:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:your_password_here@localhost:3306/green_product'
```

### 3. Start Backend | 启动后端

```bash
python app.py
```

The backend service will run at `http://localhost:5000`.

### 4. Frontend Setup | 前端配置

```bash
cd frontend
npm install
```

### 5. Start Frontend | 启动前端

```bash
npm run dev
```

The frontend will run at `http://localhost:3000`.

---

## Project Structure | 项目结构

```
green/
├── backend/                  # Backend | 后端代码
│   ├── algorithm/            # Recommendation algorithms | 算法模块
│   ├── app.py                # Application entry | 后端入口
│   ├── config.py             # Configuration | 配置文件
│   ├── models.py             # Database models | 数据库模型
│   ├── routes.py             # API routes | API路由
│   └── requirements.txt      # Python dependencies | 依赖文件
├── docs/                     # Documentation | 文档
├── frontend/                 # Frontend | 前端代码
│   ├── src/                  # Source code | 前端源码
│   ├── index.html            # Entry HTML | 前端入口
│   ├── package.json          # Node dependencies | 前端依赖
│   └── vite.config.js        # Vite configuration | Vite配置
├── sql/                      # SQL scripts | SQL脚本
│   └── create_tables.sql     # Database initialization | 数据库初始化脚本
└── README.md                 # Project description | 项目说明
```

---

## License | 许可证

This project is available under the MIT License. See the [LICENSE](LICENSE) file for details.

本项目基于 MIT 许可证开源。
