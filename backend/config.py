import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-please-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:your_password_here@localhost:3306/green_product'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 算法参数配置
    KMEANS_N_CLUSTERS = 7
    RECOMMENDATION_TOP_N = 24
    PRICE_WEIGHT_RATIO = 0.4
    GREEN_MATCH_WEIGHT_RATIO = 0.6
    PRICE_THRESHOLD_PERCENTAGE = 10  # 价格低于同类普通商品10%以内