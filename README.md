# Finance

Flask app where a user can mock buying and selling stocks.


## Setup

Start by cloning this repo and cd in the application directory.  
This app has been tested and developed with Python 3.6.9.  
For maximum compatibility please create a virtual environment with the same Python version.

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

Create a free account at `https://iexcloud.io/cloud-login#/register/` to receive an API token.  
Create a `.env` file with the following setup:

```
SECRET_KEY={RANDOM_SECRET_KEY}
IEX_KEY={API_TOKEN} 
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