import numpy as np
from sklearn.cluster import KMeans
from models import User, UserBehavior, Product, ProductGreenLabel
from models import db
import config

class UserClustering:
    def __init__(self):
        self.n_clusters = config.Config.KMEANS_N_CLUSTERS
    
    def extract_user_features(self, user_id):
        """提取用户特征"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # 初始化特征向量 - 基于具体的绿色标签
        features = {
            'organic_behavior_count': 0,     # 有机标签商品行为次数
            'environmental_behavior_count': 0, # 环保标签商品行为次数
            'degradable_behavior_count': 0,   # 可降解标签商品行为次数
            'energy_saving_behavior_count': 0, # 节能标签商品行为次数
            'no_additive_behavior_count': 0,  # 无添加标签商品行为次数
            'sustainable_behavior_count': 0,  # 可持续标签商品行为次数
            'recycled_behavior_count': 0,     # 可回收标签商品行为次数
            'total_behavior_count': 0,        # 总行为次数
            'avg_purchase_price': 0.0         # 平均购买价格
        }
        
        # 获取用户行为
        behaviors = UserBehavior.query.filter_by(user_id=user_id).all()
        
        purchase_prices = []
        
        for behavior in behaviors:
            # 检查行为类型，设置权重
            weight = 0
            if behavior.behavior_type == 'view':
                weight = 0.1  # 查看详情行为权重
            elif behavior.behavior_type == 'collect':
                weight = 0.5  # 收藏行为权重
            elif behavior.behavior_type == 'add_to_cart':
                weight = 0.3  # 加购物车行为权重
            elif behavior.behavior_type == 'purchase':
                weight = 1.0  # 购买行为权重
            
            if weight > 0:
                features['total_behavior_count'] += weight
                product = Product.query.get(behavior.product_id)
                if product:
                    if behavior.behavior_type == 'purchase':
                        purchase_prices.append(product.price)
                    # 检查商品的具体绿色标签
                    product_labels = ProductGreenLabel.query.filter_by(product_id=product.id).all()
                    for pl in product_labels:
                        green_label = pl.green_label
                        if green_label and green_label.name:
                            label_name = green_label.name.lower()
                            if '有机' in label_name or 'organic' in label_name:
                                features['organic_behavior_count'] += weight
                            elif '环保' in label_name or 'environmental' in label_name or 'eco' in label_name:
                                features['environmental_behavior_count'] += weight
                            elif '可降解' in label_name or 'degradable' in label_name:
                                features['degradable_behavior_count'] += weight
                            elif '节能' in label_name or 'energy saving' in label_name:
                                features['energy_saving_behavior_count'] += weight
                            elif '无添加' in label_name or 'no additive' in label_name:
                                features['no_additive_behavior_count'] += weight
                            elif '可持续' in label_name or 'sustainable' in label_name:
                                features['sustainable_behavior_count'] += weight
                            elif '可回收' in label_name or 'recycled' in label_name:
                                features['recycled_behavior_count'] += weight
        
        # 计算平均购买价格
        if purchase_prices:
            features['avg_purchase_price'] = np.mean(purchase_prices)
        
        # 转换为特征向量
        feature_vector = np.array([
            features['organic_behavior_count'],
            features['environmental_behavior_count'],
            features['degradable_behavior_count'],
            features['energy_saving_behavior_count'],
            features['no_additive_behavior_count'],
            features['sustainable_behavior_count'],
            features['recycled_behavior_count'],
            features['total_behavior_count'],
            features['avg_purchase_price']
        ])
        
        # 归一化
        if np.max(feature_vector) > 0:
            feature_vector = feature_vector / np.max(feature_vector)
        
        return feature_vector
    
    def cluster_users(self):
        """对所有用户进行聚类"""
        users = User.query.all()
        
        # 提取所有用户的特征
        user_features = []
        user_ids = []
        
        for user in users:
            features = self.extract_user_features(user.id)
            if features is not None:
                user_features.append(features)
                user_ids.append(user.id)
        
        if not user_features:
            return
        
        # 转换为numpy数组
        X = np.array(user_features)
        
        # 执行K-means聚类
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # 更新用户群体
        for i, user_id in enumerate(user_ids):
            user = User.query.get(user_id)
            # 映射聚类结果到群体类型
            # 0: 有机标签群体, 1: 环保标签群体, 2: 可降解标签群体, 3: 节能标签群体, 4: 无添加标签群体, 5: 可持续标签群体, 6: 可回收标签群体
            user.group_id = clusters[i] + 1  # 从1开始编号
        
        db.session.commit()
    
    def update_user_group(self, user_id):
        """更新单个用户的群体"""
        # 提取该用户的特征
        features = self.extract_user_features(user_id)
        if features is None:
            return
        
        # 获取所有用户的特征用于聚类
        users = User.query.all()
        user_features = []
        user_ids = []
        
        for user in users:
            user_feature = self.extract_user_features(user.id)
            if user_feature is not None:
                user_features.append(user_feature)
                user_ids.append(user.id)
        
        if not user_features:
            return
        
        # 执行K-means聚类
        X = np.array(user_features)
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # 更新用户群体
        for i, uid in enumerate(user_ids):
            if uid == user_id:
                user = User.query.get(uid)
                user.group_id = clusters[i] + 1  # 从1开始编号
                db.session.commit()
                break
    
    def get_user_group(self, user_id):
        """获取用户群体"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # 群体映射 - 改为更具体的绿色标签群体
        group_map = {
            1: '潜在有机标签群体',
            2: '潜在环保标签群体',
            3: '潜在可降解标签群体',
            4: '潜在节能标签群体',
            5: '潜在无添加标签群体',
            6: '潜在可持续标签群体',
            7: '潜在可回收标签群体'
        }
        
        return group_map.get(user.group_id, '未分类')