# Finance

Flask app where a user can mock buying and selling stocks.


## Setup

Start by cloning this repo and cd in the application directory.  
This app has been tested and developed with Python 3.6.9.   For maximum compatibility please create a virtual environment with the same Python version.

```
python3 -m venv env
```

Activate the enviroment with:

```
. env/bin/activate
```

Install all the dependency with:

```
pip install -r requirements.txt
```

Create and migrate the database with:

```
flask db upgrade
```

### Usage

Run the app with:

```
flask run
```

Run the tests with:

```
pytest
```