from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from models import db, Plant
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)



# Add a root route
class Home(Resource):
    def get(self):
        return {'message': 'Welcome to the Plant API'}

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        print(f"Found plants: {plants}")  # Debug print
        plants_dict = [p.to_dict() for p in plants]
        return make_response(jsonify(plants_dict), 200)

    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        return make_response(jsonify({"error": "Plant not found"}), 404)

# Add resources to API
api.add_resource(Home, '/')
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)