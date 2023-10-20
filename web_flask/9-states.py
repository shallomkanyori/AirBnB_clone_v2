#!/usr/bin/python3
"""A Flask web application."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Return all states page."""
    states = storage.all(State).values()

    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state(id):
    """Return state page.

    Args:
        id: The id of the state.
    """

    states = storage.all(State)
    key = "State.{}".format(id)

    state = states.get(key)

    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def clean(exc):
    """Remove the current SQLAlchemy Session.

    Args:
        exc : Error.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
