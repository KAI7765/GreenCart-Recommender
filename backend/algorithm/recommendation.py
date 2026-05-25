import numpy as np
from models import User, Product, UserBehavior, ProductGreenLabel, Recommendation, GreenLabel, UserPreference
from models import db
from algorithm.user_clustering import UserClustering
import config

class RecommendationEngine:
    def __init__(self):
        self.clustering = UserClustering()
        self.top_n = config.Config.RECOMMENDATION_TOP_N
        self.price_weight = config.Config.PRICE_WEIGHT_RATIO
        self.green_match_weight = config.Config.GREEN_MATCH_WEIGHT_RATIO
        self.price_threshold = config.Config.PRICE_THRESHOLD_PERCENTAGE

        self.cf_weight = 0.35
        self.cb_weight = 0.45
        self.pw_weight = 0.20

    def normalize_scores(self, scores_dict):
        """将得分字典归一化到0-1范围"""
        if not scores_dict:
            return {}
        min_score = min(scores_dict.values())
        max_score = max(scores_dict.values())
        if max_score == min_score:
            return {k: 1.0 for k in scores_dict}
        return {k: (v - min_score) / (max_score - min_score) for k, v in scores_dict}

    def merge_recommendations(self, cf_scores, cb_scores, pw_scores):
        """融合三种算法的推荐结果"""
        all_products = set()
        all_products.update(cf_scores.keys())
        all_products.update(cb_scores.keys())
        all_products.update(pw_scores.keys())

        cf_normalized = self.normalize_scores(cf_scores)
        cb_normalized = self.normalize_scores(cb_scores)
        pw_normalized = self.normalize_scores(pw_scores)

        merged_scores = {}
        for product_id in all_products:
            cf = cf_normalized.get(product_id, 0)
            cb = cb_normalized.get(product_id, 0)
            pw = pw_normalized.get(product_id, 0)
            merged_scores[product_id] = (
                self.cf_weight * cf +
                self.cb_weight * cb +
                self.pw_weight * pw
            )

        sorted_products = sorted(merged_scores.items(), key=lambda x: x[1], reverse=True)
        return [p[0] for p in sorted_products]

    def get_recommendations(self, user_id):
        """获取推荐结果"""
        try:
            preference = UserPreference.query.filter_by(user_id=user_id).first()
            user_group = self.clustering.get_user_group(user_id)

            if preference and preference.personalized:
                all_green_products = db.session.query(Product).join(ProductGreenLabel).all()
                all_green_product_ids = [p.id for p in all_green_products]
                all_green_product_details = self.get_product_details(all_green_product_ids)
                preference_recommendations = self.apply_user_preferences(user_id, all_green_product_details)
                if preference_recommendations:
                    filtered_recommendations = self.filter_user_feedback(user_id, preference_recommendations)
                    self.save_recommendations(user_id, filtered_recommendations, user_group)
                    return filtered_recommendations

            user_behaviors = UserBehavior.query.filter_by(user_id=user_id).all()
            has_history = len(user_behaviors) > 0

            if not has_history or not any(label in user_group for label in ['潜在有机标签群体', '潜在环保标签群体', '潜在可降解标签群体', '潜在节能标签群体', '潜在无添加标签群体', '潜在可持续标签群体', '潜在可回收标签群体']):
                recommendations = self.get_hot_green_products()
            else:
                cf_scores = self.collaborative_filtering(user_id)
                cb_scores = self.content_based_recommendation(user_id)
                pw_scores = self.price_weighted_recommendation(user_id)

                merged_product_ids = self.merge_recommendations(cf_scores, cb_scores, pw_scores)
                recommendations = self.get_product_details(merged_product_ids)

            filtered_recommendations = self.filter_user_feedback(user_id, recommendations)

            if len(filtered_recommendations) < self.top_n:
                all_green_products = db.session.query(Product).join(ProductGreenLabel).all()
                all_green_product_ids = [p.id for p in all_green_products]
                all_green_product_details = self.get_product_details(all_green_product_ids)

                from models import UserFeedback
                feedbacks = UserFeedback.query.filter_by(user_id=user_id).all()
                excluded_product_ids = set()
                for feedback in feedbacks:
                    if feedback.feedback_type in ['not_interested', 'price_too_high']:
                        excluded_product_ids.add(feedback.product_id)

                for product in filtered_recommendations:
                    excluded_product_ids.add(product['id'])

                import json
                preference = UserPreference.query.filter_by(user_id=user_id).first()
                price_range = preference.price_range if preference else 500

                additional_products = [product for product in all_green_product_details
                                      if product['id'] not in excluded_product_ids and product['price'] <= price_range]
                filtered_recommendations.extend(additional_products[:self.top_n - len(filtered_recommendations)])

            self.save_recommendations(user_id, filtered_recommendations, user_group)
            return filtered_recommendations
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return self.get_hot_green_products()

    def filter_user_feedback(self, user_id, recommendations):
        """排除用户不感兴趣或认为价格过高的商品"""
        try:
            from models import UserFeedback
            feedbacks = UserFeedback.query.filter_by(user_id=user_id).all()

            excluded_product_ids = set()
            for feedback in feedbacks:
                if feedback.feedback_type in ['not_interested', 'price_too_high']:
                    excluded_product_ids.add(feedback.product_id)

            filtered = [product for product in recommendations if product['id'] not in excluded_product_ids]

            if not filtered:
                return self.get_hot_green_products()

            return filtered
        except Exception as e:
            print(f"Error filtering user feedback: {e}")
            return recommendations

    def apply_user_preferences(self, user_id, recommendations):
        """应用用户偏好设置"""
        try:
            import json
            preference = UserPreference.query.filter_by(user_id=user_id).first()
            if not preference:
                return recommendations

            green_labels = json.loads(preference.green_labels) if preference.green_labels else {}
            price_range = preference.price_range
            categories = json.loads(preference.categories) if preference.categories else {}

            filtered = []
            for product in recommendations:
                if product['price'] > price_range:
                    continue

                category_key = product['category'].lower()
                category_map = {
                    '食品': 'food', '日用品': 'daily', '家居用品': 'home',
                    '母婴用品': 'baby', '家电': 'appliance', '服装': 'clothing',
                    '美妆': 'beauty', '运动用品': 'sports'
                }
                mapped_category_key = category_map.get(product['category'], product['category'].lower())
                if mapped_category_key in categories and not categories[mapped_category_key]:
                    continue

                has_preferred_label = False
                for label in product['green_labels']:
                    label_map = {
                        '有机': 'organic', '可降解': 'degradable', '节能': 'energySaving',
                        '环保': 'environmental', '无添加': 'noAdditive',
                        '可持续': 'sustainable', '可回收': 'recycled',
                        '素食': 'vegetarian', '天然': 'natural', '低碳': 'lowCarbon'
                    }
                    mapped_label_key = label_map.get(label, label.lower().replace('产品', '').replace(' ', ''))
                    if mapped_label_key in green_labels and green_labels[mapped_label_key]:
                        has_preferred_label = True
                        break
                if green_labels and not has_preferred_label:
                    continue

                filtered.append(product)

            if not filtered:
                all_green_products = db.session.query(Product).join(ProductGreenLabel).all()
                all_green_product_ids = [p.id for p in all_green_products]
                all_green_product_details = self.get_product_details(all_green_product_ids)
                price_filtered = [product for product in all_green_product_details if product['price'] <= price_range]
                if price_filtered:
                    return price_filtered[:self.top_n]
                else:
                    return self.get_hot_green_products()

            return filtered
        except Exception as e:
            print(f"Error applying user preferences: {e}")
            return recommendations

    def collaborative_filtering(self, user_id):
        """协同过滤推荐，返回商品ID及其得分"""
        user_behaviors = UserBehavior.query.filter_by(user_id=user_id).all()

        purchased_product_ids = set()
        for b in user_behaviors:
            if b.behavior_type == 'purchase':
                purchased_product_ids.add(b.product_id)

        similar_users = {}
        for behavior in user_behaviors:
            if behavior.behavior_type in ['purchase', 'collect', 'add_to_cart']:
                weight = 1.0 if behavior.behavior_type == 'purchase' else (0.5 if behavior.behavior_type == 'collect' else 0.3)
                if ProductGreenLabel.query.filter_by(product_id=behavior.product_id).first():
                    other_users = UserBehavior.query.filter_by(
                        product_id=behavior.product_id
                    ).all()
                    for other in other_users:
                        if other.user_id != user_id:
                            if other.user_id not in similar_users:
                                similar_users[other.user_id] = 0
                            similar_users[other.user_id] += weight

        product_scores = {}
        for similar_user_id, similarity in similar_users.items():
            user_other_behaviors = UserBehavior.query.filter_by(user_id=similar_user_id).all()
            for behavior in user_other_behaviors:
                product_id = behavior.product_id
                if (ProductGreenLabel.query.filter_by(product_id=product_id).first() and
                    product_id not in purchased_product_ids):
                    weight = 1.0 if behavior.behavior_type == 'purchase' else (0.5 if behavior.behavior_type == 'collect' else 0.3)
                    if product_id not in product_scores:
                        product_scores[product_id] = 0
                    product_scores[product_id] += weight * similarity

        return product_scores

    def content_based_recommendation(self, user_id):
        """基于内容的推荐，返回商品ID及其得分"""
        user_behaviors = UserBehavior.query.filter_by(user_id=user_id).all()

        interests = {
            'categories': {}, 'keywords': {}, 'green_labels': {}, 'price_range': []
        }

        for behavior in user_behaviors:
            if behavior.behavior_type == 'view':
                weight = 1.0
                product = Product.query.get(behavior.product_id)
                if product:
                    category = product.category
                    if category not in interests['categories']:
                        interests['categories'][category] = 0
                    interests['categories'][category] += weight
                    interests['price_range'].append(product.price)
                    labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
                    for label in labels:
                        label_name = label[0]
                        if label_name not in interests['green_labels']:
                            interests['green_labels'][label_name] = 0
                        interests['green_labels'][label_name] += weight

            elif behavior.behavior_type == 'purchase':
                weight = 3.0
                product = Product.query.get(behavior.product_id)
                if product:
                    category = product.category
                    if category not in interests['categories']:
                        interests['categories'][category] = 0
                    interests['categories'][category] += weight
                    interests['price_range'].append(product.price)
                    labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
                    for label in labels:
                        label_name = label[0]
                        if label_name not in interests['green_labels']:
                            interests['green_labels'][label_name] = 0
                        interests['green_labels'][label_name] += weight

            elif behavior.behavior_type == 'collect':
                weight = 2.0
                product = Product.query.get(behavior.product_id)
                if product:
                    category = product.category
                    if category not in interests['categories']:
                        interests['categories'][category] = 0
                    interests['categories'][category] += weight
                    interests['price_range'].append(product.price)
                    labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
                    for label in labels:
                        label_name = label[0]
                        if label_name not in interests['green_labels']:
                            interests['green_labels'][label_name] = 0
                        interests['green_labels'][label_name] += weight

            elif behavior.behavior_type == 'add_to_cart':
                weight = 1.5
                product = Product.query.get(behavior.product_id)
                if product:
                    category = product.category
                    if category not in interests['categories']:
                        interests['categories'][category] = 0
                    interests['categories'][category] += weight
                    interests['price_range'].append(product.price)
                    labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
                    for label in labels:
                        label_name = label[0]
                        if label_name not in interests['green_labels']:
                            interests['green_labels'][label_name] = 0
                        interests['green_labels'][label_name] += weight

            elif behavior.behavior_type == 'search':
                keywords = behavior.behavior_value.split()
                for keyword in keywords:
                    if keyword not in interests['keywords']:
                        interests['keywords'][keyword] = 0
                    interests['keywords'][keyword] += 1.0

        avg_price = sum(interests['price_range']) / len(interests['price_range']) if interests['price_range'] else 500

        green_products = db.session.query(Product).join(ProductGreenLabel).all()

        product_scores = {}
        for product in green_products:
            score = 0

            if product.category in interests['categories']:
                score += interests['categories'][product.category] * 2

            product_text = f"{product.name} {product.description}".lower()
            for keyword, weight in interests['keywords'].items():
                if keyword.lower() in product_text:
                    score += weight * 1.5

            product_labels = db.session.query(GreenLabel.name).join(ProductGreenLabel).filter(ProductGreenLabel.product_id == product.id).all()
            for label in product_labels:
                label_name = label[0]
                if label_name in interests['green_labels']:
                    score += interests['green_labels'][label_name] * 3

            price_diff = abs(product.price - avg_price)
            price_score = max(0, 10 - (price_diff / avg_price) * 10)
            score += price_score

            if score > 0:
                product_scores[product.id] = score

        return product_scores

    def price_weighted_recommendation(self, user_id):
        """价格加权推荐，返回商品ID及其得分"""
        user_behaviors = UserBehavior.query.filter_by(user_id=user_id, behavior_type='purchase').all()
        user_price_preference = []
        for behavior in user_behaviors:
            product = Product.query.get(behavior.product_id)
            if product:
                user_price_preference.append(product.price)

        avg_user_price = sum(user_price_preference) / len(user_price_preference) if user_price_preference else 300

        green_products = db.session.query(Product).join(ProductGreenLabel).all()

        product_scores = {}
        for product in green_products:
            similar_products = Product.query.filter_by(category=product.category).all()
            if similar_products:
                avg_price = np.mean([p.price for p in similar_products])
                price_advantage = (avg_price - product.price) / avg_price * 100

                if price_advantage <= self.price_threshold:
                    green_labels = ProductGreenLabel.query.filter_by(product_id=product.id).count()
                    price_preference_match = max(0, 10 - (abs(product.price - avg_user_price) / avg_user_price) * 10)
                    score = (green_labels * self.green_match_weight) + (price_advantage * self.price_weight) + (price_preference_match * 0.2)
                    product_scores[product.id] = score

        return product_scores

    def get_hot_green_products(self):
        """获取热门绿色商品"""
        hot_products = Product.query.join(ProductGreenLabel).group_by(Product.id).order_by(Product.sales.desc()).limit(self.top_n).all()
        if not hot_products:
            hot_products = Product.query.join(ProductGreenLabel).group_by(Product.id).limit(self.top_n).all()
        return self.get_product_details([p.id for p in hot_products])

    def get_product_details(self, product_ids):
        """获取商品详细信息"""
        if not product_ids:
            return []
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

        return product_list

    def save_recommendations(self, user_id, recommendations, group_type):
        """保存推荐结果到数据库"""
        Recommendation.query.filter_by(user_id=user_id).delete()

        for i, product in enumerate(recommendations):
            score = 1.0 / (i + 1)
            recommendation = Recommendation(
                user_id=user_id,
                product_id=product['id'],
                score=score,
                group_type=group_type
            )
            db.session.add(recommendation)

        db.session.commit()
