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

#### Task 10
[9-states.py](9-states.py) is a script that starts a Flask web application:
- Uses `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`)
- To load all cities of a `State`:
	- If the storage engine is DBStorage, uses `cities` relationship
	- Otherwise, uses the public getter method `cities`
- After each request, removes the current SQLAlchemy Session:
	- Declares a method to handle `@app.teardown_appcontext`
	- Calls in this method `storage.close()`
- Routes:
	- `/states`: displays a HTML page, [templates/9-states.html](templates/9-states.html): (inside the tag `BODY`)
		- `H1` tag: “States”
		- `UL` tag: with the list of all `State` objects present in `DBStorage` sorted by `name` (A->Z)
			- `LI` tag: description of one `State`: `<state.id>: <B><state.name></B>`
	- `/states/<id>`: display a HTML page: (inside the tag `BODY`)
		- If a `State` object is found with this `id`:
			- `H1` tag: “State: ”
			- `H3` tag: “Cities:”
			- `UL` tag: with the list of `City` objects linked to the `State`     sorted by `name` (A->Z)
				- `LI` tag: description of one `City`: `<city.id>: <B><city.name></B>`i
		- Otherwise:
			- `H1` tag: "Not found!"

#### Task 11
[10-hbnb_filters.py](10-hbnb_filters.py) is a Python script that starts a Flask web application:
- Uses `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`)
- To load all cities of a `State`:
	- If the storage engine is DBStorage, uses `cities` relationship
	- Otherwise, uses the public getter method `cities`
- After each request, removes the current SQLAlchemy Session:
	- Declares a method to handle `@app.teardown_appcontext`
	- Calls in this method `storage.close()`
- Routes:
	- `/hbnb_filters`: displays a HTML page like [6-index.html](https://github.com/shallomkanyori/AirBnB_clone/blob/master/web_static/6-index.html)
		- Copy files `3-footer.css`, `3-header.css`, `4-common.css` and `6-filters.css` to web_flask/static/styles
		- Copy files `icon.png` and `logo.png` to `web_flask/static/images`
		- Update .popover class in `6-filters.css` to allow scrolling in the popover and a max height of 300 pixels.
		- Use `6-index.html` content as source code for the template [10-hbnb_filters.html](templates/10-hbnb_filters.html)
		- Replace the content of the `H4` tag under each filter title (`H3` States and `H3` Amenities) by `&nbsp;`
		- `State`, `City` and `Amenity` objects must be loaded from `DBStorage` and sorted by name (A->Z)


#### Task 12
[100-hbnb.py](100-hbnb.py) is a Python script that starts a Flask web application:
- Uses `storage` for fetching data from the storage engine (`FileStorage` or `DBStorage`)
- To load all cities of a `State`:
	- If the storage engine is DBStorage, uses `cities` relationship
	- Otherwise, uses the public getter method `cities`
- After each request, removes the current SQLAlchemy Session:
	- Declares a method to handle `@app.teardown_appcontext`
	- Calls in this method `storage.close()`
- Routes:
	- `/hbnb`: displays a HTML page like [8-index.html](https://github.com/shallomkanyori/AirBnB_clone/blob/master/web_static/8-index.html)
		- Copy files `3-footer.css`, `3-header.css`, `4-common.css`, `6-filters.css` and `8-places.css` to web_flask/static/styles
		- Copy all images to `web_flask/static/images`
		- Update .popover class in `6-filters.css` to allow scrolling in the popover and a max height of 300 pixels.
		- Use `8-index.html` content as source code for the template [100-hbnb.html](templates/100-hbnb.html)
		- Update `8-places.css` to always have the price by night on the top right of each place element, and the name correctly aligned and visible
		- Replace the content of the `H4` tag under each filter title (`H3` States and `H3` Amenities) by `&nbsp;`
		- `State`, `City`, `Amenity` and `Place` objects must be loaded from `DBStorage` and sorted by name (A->Z)
