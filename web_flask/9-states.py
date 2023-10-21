#!/usr/bin/python3
"""A Flask web application."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """Get the states resource.

    Args:
        state_id: The id of the state.
    """

    states = storage.all(State)

    if state_id:
        key = "State." + state_id
        if key in states:
            state = states[key]
        else:
            state = None

        return render_template('9-states.html', state=state)

    states = states.values()
    return render_template('9-states.html', states=states)


@app.teardown_appcontext
def clean(exc):
    """Remove the current SQLAlchemy Session.

    Args:
        exc : Error.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
