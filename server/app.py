# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Route to get an earthquake by ID
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)  # Try to get earthquake by ID
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        })
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

# Route to get earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    # Query the earthquakes with a magnitude greater than or equal to the given value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Prepare the response data
    earthquake_data = [
        {
            "id": eq.id,
            "location": eq.location,
            "magnitude": eq.magnitude,
            "year": eq.year
        } for eq in earthquakes
    ]

    # Return the count and the list of earthquakes in JSON format
    return jsonify({
        "count": len(earthquake_data),
        "quakes": earthquake_data
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)

