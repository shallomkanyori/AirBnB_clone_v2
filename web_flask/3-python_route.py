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


@app.route('/c/<text>', strict_slashes=False)
def croute(text):
    """The /c/<text> route.

    Args:
        text(str): The text to display. Underscores are replaced with spaces.
    """

    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pyroute(text="is cool"):
    """The /python/<text> route.

    Args:
        text(str): The text to display. Underscores are replaced with spaces.
    """

    text = text.replace("_", " ")
    return "Python {}".format(text)


if __name__ == "__main__":
    app.run()
