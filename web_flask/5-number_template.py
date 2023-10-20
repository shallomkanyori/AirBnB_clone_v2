#!/usr/bin/python3
"""A Flask web application."""
from flask import Flask, render_template

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
        text (str): The text to display. Underscores are replaced with spaces.
    """

    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def nroute(n):
    """The /number/<n> route.

    Args:
        n (int): The number to be displayed.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def nroute_temp(n):
    """The /number_template/<n> route.

    Args:
        n (int): The number to be displayed.
    """
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
