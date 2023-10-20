#!/usr/bin/python3
"""A simple Flask web application."""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """The index page."""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """The /hbnb page."""
    return "HBNB"


if __name__ == "__main__":
    app.run()
