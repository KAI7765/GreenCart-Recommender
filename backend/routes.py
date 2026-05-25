from flask import Blueprint, jsonify, request
from models import User, Product, UserBehavior, GreenLabel, ProductGreenLabel, Recommendation, UserFeedback, UserCollection, ShoppingCart, UserPreference, db
from algorithm.user_clustering import UserClustering
from algorithm.recommendation import RecommendationEngine
from algorithm.data_preprocessing import DataPreprocessing
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import json
# 用户相关路由
user_bp = Blueprint('user', __name__)
# 管理员相关路由
admin_bp = Blueprint('admin', __name__)
# 推荐相关路由
recommend_bp = Blueprint('recommend', __name__)

# 用户注册
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    new_user = User(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# 更新用户个人资料
@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # 检查用户名是否被其他用户占用
    if username and username != user.username:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400
        user.username = username

    # 检查邮箱是否被其他用户占用
    if email and email != user.email:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 400
        user.email = email

    # 更新密码（如果提供）
    if password:
        user.password = password

    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating profile: {e}")
        return jsonify({'message': 'Failed to update profile'}), 500

# 用户登录
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token, 'user_id': user.id, 'role': user.role}), 200

# 记录用户行为
@user_bp.route('/behavior', methods=['POST'])
def record_behavior():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    behavior_type = data.get('behavior_type')
    behavior_value = data.get('behavior_value')
    
    new_behavior = UserBehavior(
        user_id=user_id,
        product_id=product_id,
        behavior_type=behavior_type,
        behavior_value=behavior_value
    )
    db.session.add(new_behavior)
    db.session.commit()
    
    # 更新用户群体
    clustering = UserClustering()
    clustering.update_user_group(user_id)
    
    return jsonify({'message': 'Behavior recorded successfully'}), 201

# 提交用户反馈
@user_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    feedback_type = data.get('feedback_type')
    
    new_feedback = UserFeedback(
        user_id=user_id,
        product_id=product_id,
        feedback_type=feedback_type
    )
    db.session.add(new_feedback)
    db.session.commit()
    
    return jsonify({'message': 'Feedback submitted successfully'}), 201

# 保存用户偏好设置
@user_bp.route('/preferences', methods=['POST'])
def save_preferences():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid request data'}), 400
        
        user_id = data.get('user_id')
        preferences = data.get('preferences')
        
        if not user_id or not preferences:
            return jsonify({'message': 'Missing required fields'}), 400
        
        # 清空用户的行为数据和反馈数据
        print(f"Clearing user data for user {user_id}")
        
        # 删除用户行为数据
        UserBehavior.query.filter_by(user_id=user_id).delete()
        print(f"Deleted user behaviors for user {user_id}")
        
        # 删除用户反馈数据
        UserFeedback.query.filter_by(user_id=user_id).delete()
        print(f"Deleted user feedback for user {user_id}")
        
        # 将偏好设置存储到数据库中
        import json
        
        # 查找现有偏好设置
        existing = UserPreference.query.filter_by(user_id=user_id).first()
        if existing:
            # 更新现有偏好设置
            existing.green_labels = json.dumps(preferences.get('greenLabels', {}))
            existing.price_range = preferences.get('priceRange', 500)
            existing.priority = preferences.get('priority', 'greenMatch')
            existing.categories = json.dumps(preferences.get('categories', {}))
            existing.green_level = preferences.get('greenLevel', 'medium')
            existing.brand_preference = preferences.get('brandPreference', '')
            existing.personalized = preferences.get('personalized', True)
        else:
            # 创建新偏好设置
            new_preference = UserPreference(
                user_id=user_id,
                green_labels=json.dumps(preferences.get('greenLabels', {})),
                price_range=preferences.get('priceRange', 500),
                priority=preferences.get('priority', 'greenMatch'),
                categories=json.dumps(preferences.get('categories', {})),
                green_level=preferences.get('greenLevel', 'medium'),
                brand_preference=preferences.get('brandPreference', ''),
                personalized=preferences.get('personalized', True)
            )
            db.session.add(new_preference)
        
        db.session.commit()
        
        return jsonify({'message': 'Preferences saved successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error saving preferences: {e}")
        return jsonify({'message': 'Failed to save preferences'}), 500

# 添加商品到收藏
@user_bp.route('/collection', methods=['POST'])
def add_to_collection():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        
        if not user_id or not product_id:
            return jsonify({'message': 'Missing required fields'}), 400
        
        # 检查商品是否存在
        if not Product.query.get(product_id):
            return jsonify({'message': 'Product not found'}), 404
        
        # 检查是否已经收藏
        existing = UserCollection.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            return jsonify({'message': 'Product already in collection'}), 400
        
        # 添加收藏
        new_collection = UserCollection(user_id=user_id, product_id=product_id)
        db.session.add(new_collection)
        db.session.commit()
        
        # 记录收藏行为
        new_behavior = UserBehavior(
            user_id=user_id,
            product_id=product_id,
            behavior_type='collect',
            behavior_value=''
        )
        db.session.add(new_behavior)
        db.session.commit()
        
        # 更新用户群体
        clustering = UserClustering()
        clustering.update_user_group(user_id)
        
        return jsonify({'message': 'Product added to collection successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding to collection: {e}")
        return jsonify({'message': 'Failed to add to collection'}), 500

# 从收藏中移除商品
@user_bp.route('/collection/<int:product_id>', methods=['DELETE'])
def remove_from_collection(product_id):
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'message': 'Missing user_id'}), 400
        
        # 查找收藏记录
        collection = UserCollection.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not collection:
            return jsonify({'message': 'Product not in collection'}), 404
        
        # 删除收藏
        db.session.delete(collection)
        db.session.commit()
        
        return jsonify({'message': 'Product removed from collection successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error removing from collection: {e}")
        return jsonify({'message': 'Failed to remove from collection'}), 500

# 获取用户的收藏列表
@user_bp.route('/collection', methods=['GET'])
def get_collection():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'message': 'Missing user_id'}), 400
        
        # 获取用户收藏的商品
        collections = UserCollection.query.filter_by(user_id=user_id).all()
        product_ids = [c.product_id for c in collections]
        
        # 获取商品详情
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        product_list = []
        for product in products:
            labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
            green_labels = [label[0] for label in labels]
            product_list.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category,
                'description': product.description,
                'image_url': product.image_url,
                'sales': product.sales,
                'rating': product.rating,
                'green_labels': green_labels
            })
        
        return jsonify(product_list), 200
    except Exception as e:
        print(f"Error getting collection: {e}")
        return jsonify({'message': 'Failed to get collection'}), 500

# 添加商品到购物车
@user_bp.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not user_id or not product_id:
            return jsonify({'message': 'Missing required fields'}), 400
        
        # 检查商品是否存在
        if not Product.query.get(product_id):
            return jsonify({'message': 'Product not found'}), 404
        
        # 检查购物车中是否已有该商品
        existing = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            # 更新数量
            existing.quantity += quantity
        else:
            # 添加新商品
            new_cart = ShoppingCart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(new_cart)
        
        db.session.commit()
        
        # 记录购物车行为
        new_behavior = UserBehavior(
            user_id=user_id,
            product_id=product_id,
            behavior_type='add_to_cart',
            behavior_value=str(quantity)
        )
        db.session.add(new_behavior)
        db.session.commit()
        
        # 更新用户群体
        clustering = UserClustering()
        clustering.update_user_group(user_id)
        
        return jsonify({'message': 'Product added to cart successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding to cart: {e}")
        return jsonify({'message': 'Failed to add to cart'}), 500

# 从购物车移除商品
@user_bp.route('/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'message': 'Missing user_id'}), 400
        
        # 查找购物车记录
        cart = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not cart:
            return jsonify({'message': 'Product not in cart'}), 404
        
        # 删除购物车记录
        db.session.delete(cart)
        db.session.commit()
        
        return jsonify({'message': 'Product removed from cart successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error removing from cart: {e}")
        return jsonify({'message': 'Failed to remove from cart'}), 500

# 更新购物车商品数量
@user_bp.route('/cart/<int:product_id>', methods=['PUT'])
def update_cart_quantity(product_id):
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        quantity = data.get('quantity')
        
        if not user_id or quantity is None:
            return jsonify({'message': 'Missing required fields'}), 400
        
        if quantity <= 0:
            return jsonify({'message': 'Quantity must be positive'}), 400
        
        # 查找购物车记录
        cart = ShoppingCart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not cart:
            return jsonify({'message': 'Product not in cart'}), 404
        
        # 更新数量
        cart.quantity = quantity
        db.session.commit()
        
        return jsonify({'message': 'Cart quantity updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating cart quantity: {e}")
        return jsonify({'message': 'Failed to update cart quantity'}), 500

# 获取用户的购物车列表
@user_bp.route('/cart', methods=['GET'])
def get_cart():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'message': 'Missing user_id'}), 400
        
        # 获取用户购物车中的商品
        carts = ShoppingCart.query.filter_by(user_id=user_id).all()
        cart_items = []
        
        for cart in carts:
            product = Product.query.get(cart.product_id)
            if product:
                labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
                green_labels = [label[0] for label in labels]
                cart_items.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'description': product.description,
                    'image_url': product.image_url,
                    'sales': product.sales,
                    'rating': product.rating,
                    'green_labels': green_labels,
                    'quantity': cart.quantity,
                    'subtotal': product.price * cart.quantity
                })
        
        # 计算总金额
        total = sum(item['subtotal'] for item in cart_items)
        
        return jsonify({
            'items': cart_items,
            'total': total
        }), 200
    except Exception as e:
        print(f"Error getting cart: {e}")
        return jsonify({'message': 'Failed to get cart'}), 500

# 管理员添加绿色标签
@admin_bp.route('/labels', methods=['POST'])
def add_label():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if GreenLabel.query.filter_by(name=name).first():
        return jsonify({'message': 'Label already exists'}), 400
    
    new_label = GreenLabel(name=name, description=description)
    db.session.add(new_label)
    db.session.commit()
    
    return jsonify({'message': 'Label added successfully'}), 201

# 管理员获取绿色标签列表
@admin_bp.route('/labels', methods=['GET'])
def get_labels():
    labels = GreenLabel.query.all()
    label_list = [{'id': label.id, 'name': label.name, 'description': label.description} for label in labels]
    return jsonify(label_list), 200

# 管理员为商品添加绿色标签
@admin_bp.route('/products/<int:product_id>/labels', methods=['POST'])
def add_product_label(product_id):
    data = request.get_json()
    label_id = data.get('label_id')
    
    if not Product.query.get(product_id):
        return jsonify({'message': 'Product not found'}), 404
    
    if not GreenLabel.query.get(label_id):
        return jsonify({'message': 'Label not found'}), 404
    
    existing = ProductGreenLabel.query.filter_by(product_id=product_id, label_id=label_id).first()
    if existing:
        return jsonify({'message': 'Label already added to product'}), 400
    
    new_association = ProductGreenLabel(product_id=product_id, label_id=label_id)
    db.session.add(new_association)
    db.session.commit()
    
    return jsonify({'message': 'Label added to product successfully'}), 201

# 获取推荐结果
@recommend_bp.route('/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    try:
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(user_id)
        return jsonify(recommendations), 200
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        # 推荐模块故障时，返回热门绿色商品
        try:
            hot_products = Product.query.join(ProductGreenLabel).group_by(Product.id).order_by(Product.sales.desc()).limit(10).all()
            hot_list = [{
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'category': product.category,
                'image_url': product.image_url,
                'sales': product.sales,
                'rating': product.rating,
                'green_labels': [label.name for label in db.session.query(GreenLabel).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()]
            } for product in hot_products]
            return jsonify(hot_list), 200
        except Exception as fallback_error:
            print(f"Error in fallback mechanism: {fallback_error}")
            return jsonify({'message': 'Failed to get recommendations'}), 500

# 导入数据
@admin_bp.route('/import-data', methods=['POST'])
def import_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid request data'}), 400
        
        preprocessor = DataPreprocessing()
        result = preprocessor.import_data(data)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error importing data: {e}")
        return jsonify({'message': 'Failed to import data'}), 500

# 获取热门绿色商品（无需登录）
@admin_bp.route('/products/hot', methods=['GET'])
def get_hot_green_products():
    try:
        # 获取有绿色标签的商品，按销量排序
        hot_products = Product.query.join(ProductGreenLabel).group_by(Product.id).order_by(Product.sales.desc()).limit(24).all()
        hot_list = []
        for product in hot_products:
            try:
                labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
                green_labels = [label[0] for label in labels]
                hot_list.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'description': product.description,
                    'image_url': product.image_url,
                    'sales': product.sales,
                    'rating': product.rating,
                    'green_labels': green_labels
                })
            except Exception as product_error:
                print(f"Error processing product {product.id}: {product_error}")
                continue
        return jsonify(hot_list), 200
    except Exception as e:
        print(f"Error getting hot green products: {e}")
        return jsonify({'message': 'Failed to get hot products'}), 500

# 管理员获取商品列表
@admin_bp.route('/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        product_list = []
        for product in products:
            try:
                labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
                green_labels = [label[0] for label in labels]
                product_list.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'category': product.category,
                    'description': product.description,
                    'image_url': product.image_url,
                    'sales': product.sales,
                    'rating': product.rating,
                    'green_labels': green_labels
                })
            except Exception as product_error:
                print(f"Error processing product {product.id}: {product_error}")
                # 跳过出错的商品，继续处理其他商品
                continue
        return jsonify(product_list), 200
    except Exception as e:
        print(f"Error getting products: {e}")
        return jsonify({'message': 'Failed to get products'}), 500

# 管理员添加商品
@admin_bp.route('/products', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid request data'}), 400
        
        # 验证必填字段
        required_fields = ['name', 'price', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        # 验证价格是否为正数
        if data['price'] <= 0:
            return jsonify({'message': 'Price must be positive'}), 400
        
        new_product = Product(
            name=data['name'],
            price=data['price'],
            category=data['category'],
            description=data.get('description', ''),
            image_url=data.get('image_url', ''),
            sales=data.get('sales', 0),
            rating=data.get('rating', 0.0)
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error adding product: {e}")
        return jsonify({'message': 'Failed to add product'}), 500

# 管理员编辑商品
@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid request data'}), 400
        
        # 查找商品
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        # 更新商品信息
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            if data['price'] <= 0:
                return jsonify({'message': 'Price must be positive'}), 400
            product.price = data['price']
        if 'category' in data:
            product.category = data['category']
        if 'description' in data:
            product.description = data['description']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'sales' in data:
            product.sales = data['sales']
        if 'rating' in data:
            product.rating = data['rating']
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating product: {e}")
        return jsonify({'message': 'Failed to update product'}), 500

# 管理员删除商品
@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        print(f"Attempting to delete product with ID: {product_id}")
        # 查找商品
        product = Product.query.get(product_id)
        print(f"Found product: {product}")
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        # 先删除关联数据，使用单独的查询和删除，确保在删除商品之前所有关联数据都被删除
        print("Deleting related data...")
        
        # 删除商品-标签关联
        db.session.execute(ProductGreenLabel.__table__.delete().where(ProductGreenLabel.product_id == product_id))
        print("Deleted product labels")
        
        # 删除用户行为关联
        db.session.execute(UserBehavior.__table__.delete().where(UserBehavior.product_id == product_id))
        print("Deleted user behaviors")
        
        # 删除用户收藏关联
        db.session.execute(UserCollection.__table__.delete().where(UserCollection.product_id == product_id))
        print("Deleted user collections")
        
        # 删除购物车关联
        db.session.execute(ShoppingCart.__table__.delete().where(ShoppingCart.product_id == product_id))
        print("Deleted shopping cart items")
        
        # 提交关联数据的删除
        db.session.commit()
        print("Committed related data deletion")
        
        # 重新获取商品（因为会话已经提交，之前的product对象可能已经失效）
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        # 删除商品
        print("Deleting product...")
        db.session.delete(product)
        print("Committing product deletion...")
        db.session.commit()
        print("Product deleted successfully")
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting product: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Failed to delete product'}), 500

# 管理员批量删除商品
@admin_bp.route('/products/batch-delete', methods=['DELETE'])
def batch_delete_products():
    try:
        data = request.get_json()
        if not data or 'product_ids' not in data:
            return jsonify({'message': 'Missing product_ids parameter'}), 400
        
        product_ids = data['product_ids']
        if not isinstance(product_ids, list):
            return jsonify({'message': 'product_ids must be a list'}), 400
        
        print(f"Attempting to batch delete products: {product_ids}")
        
        # 先删除所有关联数据
        print("Deleting related data...")
        
        # 删除商品-标签关联
        db.session.execute(ProductGreenLabel.__table__.delete().where(ProductGreenLabel.product_id.in_(product_ids)))
        print("Deleted product labels")
        
        # 删除用户行为关联
        db.session.execute(UserBehavior.__table__.delete().where(UserBehavior.product_id.in_(product_ids)))
        print("Deleted user behaviors")
        
        # 删除用户收藏关联
        db.session.execute(UserCollection.__table__.delete().where(UserCollection.product_id.in_(product_ids)))
        print("Deleted user collections")
        
        # 删除购物车关联
        db.session.execute(ShoppingCart.__table__.delete().where(ShoppingCart.product_id.in_(product_ids)))
        print("Deleted shopping cart items")
        
        # 提交关联数据的删除
        db.session.commit()
        print("Committed related data deletion")
        
        # 然后删除商品
        print("Deleting products...")
        db.session.execute(Product.__table__.delete().where(Product.id.in_(product_ids)))
        print("Deleted products")
        
        # 提交商品删除
        db.session.commit()
        print("Batch delete completed successfully")
        return jsonify({'message': 'Products deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error batch deleting products: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Failed to delete products'}), 500

# 管理员获取用户列表和统计
@admin_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    organic_label = 0
    environmental_label = 0
    degradable_label = 0
    energy_saving_label = 0
    no_additive_label = 0
    sustainable_label = 0
    recycled_label = 0
    
    group_map = {
        1: '潜在有机标签群体',
        2: '潜在环保标签群体',
        3: '潜在可降解标签群体',
        4: '潜在节能标签群体',
        5: '潜在无添加标签群体',
        6: '潜在可持续标签群体',
        7: '潜在可回收标签群体',
        0: '未分类'
    }
    
    for user in users:
        group_name = group_map.get(user.group_id, '未分类')
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'group_name': group_name,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
        if user.group_id == 1:
            organic_label += 1
        elif user.group_id == 2:
            environmental_label += 1
        elif user.group_id == 3:
            degradable_label += 1
        elif user.group_id == 4:
            energy_saving_label += 1
        elif user.group_id == 5:
            no_additive_label += 1
        elif user.group_id == 6:
            sustainable_label += 1
        elif user.group_id == 7:
            recycled_label += 1
    
    return jsonify({
        'users': user_list,
        'total': len(users),
        'organicLabel': organic_label,
        'environmentalLabel': environmental_label,
        'degradableLabel': degradable_label,
        'energySavingLabel': energy_saving_label,
        'noAdditiveLabel': no_additive_label,
        'sustainableLabel': sustainable_label,
        'recycledLabel': recycled_label
    }), 200

# 管理员获取分析数据
@admin_bp.route('/analytics', methods=['GET'])
def get_analytics():
    # 获取总用户数
    total_users = User.query.count()
    
    # 获取总商品数
    total_products = Product.query.count()
    
    # 获取推荐次数
    recommendation_count = Recommendation.query.count()
    
    # 获取用户反馈数
    feedback_count = UserFeedback.query.count()
    
    return jsonify({
        'totalUsers': total_users,
        'totalProducts': total_products,
        'recommendationCount': recommendation_count,
        'feedbackCount': feedback_count
    }), 200

