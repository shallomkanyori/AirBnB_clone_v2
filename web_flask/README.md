## AirBnB clone - Web framework

#### Task 0
[0-hello_route.py](0-hello_route.py) is a simple Flask web application
- Routes:
	- `/`: displays "Hello HBNB!"

#### Task 1
[1-hbnb_route.py](1-hbnb_route.py) is a Python script that starts a Flask web application:
- Routes:
	- `/`: displays "Hello HBNB!"
	- `/hbnb`: displays “HBNB”

#### Task 2
[2-c_route.py](2-c_route.py) is a Python script that starts a Flask web application:
- Routes:
	- `/`: displays "Hello HBNB!"
	- `/hbnb`: displays “HBNB”
	- `/c/<text>`: displays “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)

#### Task 3
[3-python_route.py](3-python_route.py) is a Python script that starts a Flask web application:
- Routes:
	- `/`: displays "Hello HBNB!"
	- `/hbnb`: displays “HBNB”
	- `/c/<text>`: displays “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	- `/python/<text>`: displays “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		- The default value of `text` is “is cool”

#### Task 4
[4-number_route.py](4-number_route.py) is a Python script that starts a Flask web application:
- Routes:
	- `/`: displays "Hello HBNB!"
	- `/hbnb`: displays “HBNB”
	- `/c/<text>`: displays “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	- `/python/<text>`: displays “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		- The default value of `text` is “is cool”
	- `/number/<n>`: displays “`n` is a number” only if `n` is an integer

#### Task 5
[5-number_template.py](5-number_template.py) is a Python script that starts a Flask web application:
- Routes:
	- `/`: displays "Hello HBNB!"
	- `/hbnb`: displays “HBNB”
	- `/c/<text>`: displays “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	- `/python/<text>`: displays “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		- The default value of `text` is “is cool”
	- `/number/<n>`: displays “`n` is a number” only if `n` is an integer
	- `/number_template/<n>`: displays a HTML page, [templates/5-number.html](templates/5-number.html), only if `n` is an integer:
		- `H1` tag: “Number: `n`” inside the tag BODY

#### Task 6
[6-number_odd_or_even.py](6-number_odd_or_even.py) is a Python script that starts a Flask web application:
- Routes:
	- `/`: displays "Hello HBNB!"
	- `/hbnb`: displays “HBNB”
	- `/c/<text>`: displays “C ” followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
	- `/python/<text>`: displays “Python ”, followed by the value of the `text` variable (replace underscore `_` symbols with a space ` `)
		- The default value of `text` is “is cool”
	- `/number/<n>`: displays “`n` is a number” only if `n` is an integer
	- `/number_template/<n>`: displays a HTML page, [templates/5-number.html](templates/5-number.html), only if `n` is an integer:
		- `H1` tag: “Number: `n`” inside the tag BODY
	- `/number_odd_or_even/<n>`: displays a HTML page only if `n` is an integer:
		- `H1` tag: “Number: `n` is `even|odd`” inside the tag `BODY`
