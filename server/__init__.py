from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize database and migration tools
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Restaurant, Pizza, RestaurantPizza

    @app.route('/')
    def index():
        return '<h1>Pizza Restaurant API</h1>'

    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        return jsonify([r.to_dict() for r in restaurants])

    @app.route('/restaurants/<int:id>', methods=['GET'])
    def get_restaurant_by_id(id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        data = restaurant.to_dict()
        data['restaurant_pizzas'] = [rp.to_dict() for rp in restaurant.restaurant_pizzas]
        return jsonify(data)

    @app.route('/restaurants/<int:id>', methods=['DELETE'])
    def delete_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return jsonify({"error": "Restaurant not found"}), 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

    @app.route('/pizzas', methods=['GET'])
    def get_pizzas():
        pizzas = Pizza.query.all()
        return jsonify([p.to_dict() for p in pizzas])

    @app.route('/restaurant_pizzas', methods=['POST'])
    def create_restaurant_pizza():
        data = request.get_json()
        try:
            new_rp = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            db.session.add(new_rp)
            db.session.commit()
            return jsonify(new_rp.to_dict()), 201
        except Exception:
            db.session.rollback()
            return jsonify({"errors": ["validation errors"]}), 400

    return app
