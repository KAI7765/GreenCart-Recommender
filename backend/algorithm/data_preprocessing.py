import pandas as pd
import numpy as np
import re
from models import Product, GreenLabel, ProductGreenLabel, User, UserBehavior
from models import db

class DataPreprocessing:
    def __init__(self):
        # 扩展绿色关键词库
        self.green_keywords = {
            '有机': ['有机', 'organic', 'bio', 'biological'],
            '可降解': ['可降解', 'degradable', 'biodegradable', 'compostable'],
            '节能': ['节能', 'energy saving', 'energy-efficient', 'eco-friendly energy'],
            '环保': ['环保', 'eco-friendly', 'environmentally friendly', 'green'],
            '无添加': ['无添加', 'no additive', 'additive-free', 'natural'],
            '可持续': ['可持续', 'sustainable', 'sustainability'],
            '可回收': ['可回收', 'recyclable', 'recycled'],
            '低碳': ['低碳', 'low carbon', 'carbon footprint'],
            '素食': ['素食', 'vegan', 'vegetarian'],
            '天然': ['天然', 'natural', 'pure']
        }
    
    def load_data(self, file_path):
        """加载数据集"""
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self, data):
        """清洗数据"""
        # 处理缺失值
        data = data.dropna()
        
        # 剔除无效订单
        if 'price' in data.columns:
            data = data[data['price'] > 0]
        
        if 'sales' in data.columns:
            data = data[data['sales'] >= 0]
        
        if 'rating' in data.columns:
            data = data[(data['rating'] >= 0) & (data['rating'] <= 5)]
        
        # 去除重复值
        data = data.drop_duplicates()
        
        # 标准化文本数据
        if 'name' in data.columns:
            data['name'] = data['name'].apply(lambda x: x.strip())
        
        if 'description' in data.columns:
            data['description'] = data['description'].apply(lambda x: x.strip() if isinstance(x, str) else x)
        
        if 'category' in data.columns:
            data['category'] = data['category'].apply(lambda x: x.strip())
        
        return data
    
    def label_green_products(self, products):
        """标注绿色商品"""
        for product in products:
            product_name = product.name.lower()
            product_desc = product.description.lower() if product.description else ''
            
            for label_name, keywords in self.green_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in product_name or keyword.lower() in product_desc:
                        # 检查标签是否存在
                        label = GreenLabel.query.filter_by(name=label_name).first()
                        if not label:
                            label = GreenLabel(name=label_name)
                            db.session.add(label)
                            db.session.commit()
                        
                        # 检查商品是否已有该标签
                        existing = ProductGreenLabel.query.filter_by(
                            product_id=product.id, label_id=label.id
                        ).first()
                        if not existing:
                            association = ProductGreenLabel(
                                product_id=product.id, label_id=label.id
                            )
                            db.session.add(association)
            
            db.session.commit()
    
    def calculate_green_score(self, product):
        """计算商品的绿色评分"""
        product_name = product.name.lower()
        product_desc = product.description.lower() if product.description else ''
        
        score = 0
        for label_name, keywords in self.green_keywords.items():
            for keyword in keywords:
                if keyword.lower() in product_name or keyword.lower() in product_desc:
                    score += 1
                    break
        
        # 考虑绿色标签数量
        green_labels = ProductGreenLabel.query.filter_by(product_id=product.id).count()
        score += green_labels * 2
        
        return score
    
    def import_data(self, data):
        """导入数据到数据库"""
        try:
            # 导入商品数据
            if 'products' in data:
                for product_data in data['products']:
                    product = Product(
                        name=product_data['name'],
                        price=product_data['price'],
                        category=product_data['category'],
                        description=product_data.get('description', ''),
                        image_url=product_data.get('image_url', ''),
                        sales=product_data.get('sales', 0),
                        rating=product_data.get('rating', 0.0)
                    )
                    db.session.add(product)
                db.session.commit()
                
                # 标注绿色商品
                products = Product.query.all()
                self.label_green_products(products)
            
            # 导入用户数据
            if 'users' in data:
                for user_data in data['users']:
                    user = User(
                        username=user_data['username'],
                        password=user_data['password'],
                        email=user_data['email'],
                        role=user_data.get('role', 'user')
                    )
                    db.session.add(user)
                db.session.commit()
            
            # 导入用户行为数据
            if 'behaviors' in data:
                for behavior_data in data['behaviors']:
                    behavior = UserBehavior(
                        user_id=behavior_data['user_id'],
                        product_id=behavior_data['product_id'],
                        behavior_type=behavior_data['behavior_type'],
                        behavior_value=behavior_data.get('behavior_value', '')
                    )
                    db.session.add(behavior)
                db.session.commit()
            
            return {'message': 'Data imported successfully'}
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error importing data: {str(e)}'}
    
    def batch_process(self, file_path):
        """批量处理数据"""
        try:
            # 加载数据
            data = self.load_data(file_path)
            if data is None:
                return {'message': 'Failed to load data'}
            
            # 清洗数据
            cleaned_data = self.clean_data(data)
            
            # 导入数据
            if 'product_id' in cleaned_data.columns:
                # 商品数据
                products = []
                for _, row in cleaned_data.iterrows():
                    product = Product(
                        id=row.get('product_id'),
                        name=row.get('name', ''),
                        price=row.get('price', 0),
                        category=row.get('category', ''),
                        description=row.get('description', ''),
                        image_url=row.get('image_url', ''),
                        sales=row.get('sales', 0),
                        rating=row.get('rating', 0.0)
                    )
                    products.append(product)
                
                db.session.add_all(products)
                db.session.commit()
                
                # 标注绿色商品
                self.label_green_products(products)
            
            return {'message': 'Batch processing completed successfully'}
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error in batch processing: {str(e)}'}