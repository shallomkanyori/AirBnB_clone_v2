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
	- `/number_odd_or_even/<n>`: displays a HTML page, [templates/6-number_odd_or_even.html](templates/6-number_odd_or_even.html), only if `n` is an integer:
		- `H1` tag: “Number: `n` is `even|odd`” inside the tag `BODY`

#### Task 7
Update some parts of the storage engine:

Update FileStorage: ([../models/engine/file_storage.py](../models/engine/file_storage.py))
- Added public method `def close(self):`: calls `reload()` method for deserializing the JSON file to objects
Update DBStorage: ([../models/engine/db_storage.py](../models/engine/db_storage.py))
- Added public method `def close(self):`: call `remove()` method on the private session attribute (`self.__session`)

#### Task 8
[7-states_list.py](7-states_list.py) is a script that starts a Flask web application:
- Uses `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`)
- After each request, removes the current SQLAlchemy Session:
	- Declares a method to handle `@app.teardown_appcontext`
	- Calls in this method `storage.close()`
- Routes:
	- `/states_list`: displays a HTML page, [templates/7-states_list.html](templates/7-states_list.html): (inside the tag `BODY`)
		- `H1` tag: “States”
		- `UL` tag: with the list of all `State` objects present in `DBStorage` sorted by `name` (A->Z)
			- `LI` tag: description of one `State`: `<state.id>: <B><state.name></B>`

#### Task 9
[8-cities_by_states.py](8-cities_by_states.py) is a script that starts a Flask web application:
- Uses `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`)
- To load all cities of a `State`:
	- If the storage engine is DBStorage, uses `cities` relationship
	- Otherwise, uses the public getter method `cities`
- After each request, removes the current SQLAlchemy Session:
	- Declares a method to handle `@app.teardown_appcontext`
	- Calls in this method `storage.close()`
- Routes:
	- `/cities_by_states`: displays a HTML page, [templates/8-cities_by_states.html](templates/8-cities_by_states.html): (inside the tag `BODY`)
		- `H1` tag: “States”
		- `UL` tag: with the list of all `State` objects present in `DBStorage` sorted by `name` (A->Z)
			- `LI` tag: description of one `State`: `<state.id>: <B><state.name></B>` + `UL` tag: with the list of `City` objects linked to the `State` sorted by `name` (A->Z)
				- `LI` tag: description of one `City`: `<city.id>: <B><city.name></B>`
