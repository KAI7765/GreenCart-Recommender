from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')  # user or admin
    group_id = db.Column(db.Integer, default=0)  # 0: 未分类, 1: 主动绿色群体, 2: 潜在绿色群体, 3: 性价比绿色群体
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 商品表
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    sales = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 绿色标签表
class GreenLabel(db.Model):
    __tablename__ = 'green_labels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # 有机、可降解、节能等
    description = db.Column(db.Text)

# 商品-绿色标签关联表
class ProductGreenLabel(db.Model):
    __tablename__ = 'product_green_labels'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('green_labels.id'), nullable=False)

# 用户行为表
class UserBehavior(db.Model):
    __tablename__ = 'user_behaviors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    behavior_type = db.Column(db.String(20), nullable=False)  # view, purchase, collect, search
    behavior_value = db.Column(db.String(255))  # 搜索关键词等
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 推荐结果表
class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    group_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 用户反馈表
class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    feedback_type = db.Column(db.String(20), nullable=False)  # not_interested, price_too_high
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# 用户收藏表
class UserCollection(db.Model):
    __tablename__ = 'user_collections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # 确保用户对同一商品只收藏一次
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='_user_product_uc'),)

# 购物车表
class ShoppingCart(db.Model):
    __tablename__ = 'shopping_carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)  # 商品数量
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # 确保用户对同一商品在购物车中只有一条记录
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='_user_cart_product_uc'),)

# 用户偏好设置表
class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    green_labels = db.Column(db.Text)  # JSON格式存储绿色标签偏好
    price_range = db.Column(db.Float, default=500)
    priority = db.Column(db.String(50), default='greenMatch')
    categories = db.Column(db.Text)  # JSON格式存储分类偏好
    green_level = db.Column(db.String(20), default='medium')
    brand_preference = db.Column(db.Text)
    personalized = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # 确保每个用户只有一条偏好设置记录
    __table_args__ = (db.UniqueConstraint('user_id', name='_user_preference_uc'),)