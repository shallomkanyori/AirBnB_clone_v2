#!/usr/bin/python3
"""A Flask web application."""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenities import Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def index():
    """Return AirBnb landing page."""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()

    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


@app.teardown_appcontext
def clean(exc):
    """Remove the current SQLAlchemy Session.

    Args:
        exc : Error.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
