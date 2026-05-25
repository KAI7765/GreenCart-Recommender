from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes import user_bp, admin_bp, recommend_bp
import config

app = Flask(__name__)
app.config.from_object(config.Config)
CORS(app)

db.init_app(app)

# 初始化JWT
jwt = JWTManager(app)

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(recommend_bp, url_prefix='/api/recommend')

# 为了兼容前端的请求，添加额外的路由
app.register_blueprint(admin_bp, url_prefix='/admin', name='admin_without_api')
app.register_blueprint(recommend_bp, url_prefix='/recommend', name='recommend_without_api')
app.register_blueprint(user_bp, url_prefix='/user', name='user_without_api')

@app.route('/')
def index():
    return jsonify({'message': 'Green Product Recommendation System'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)