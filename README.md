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

### Docker

Start by creating a Docker Image with:

```
docker build -t finance:latest .
```

The Docker version of the application use MySQL to store the data, therefore it is needed to start a Docker Container for the MySQL database.
You can do so with (remember to replace the password):

```
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=finance -e MYSQL_USER=finance \
    -e MYSQL_PASSWORD={DATABASE_PASSWORD} \
    mysql/mysql-server:5.7
```

Once the MySQL container is up and running, it's time to start the application container and link them together.
Remember to replace the ENV variables and password in the following command:

```
docker run --name finance -dp 8000:5000 -e SECRET_KEY={RANDOM_SECRET_KEY} \
    -e IEX_KEY={API_TOKEN} \
    --link mysql:dbserver \
    -e SQLALCHEMY_DATABASE_URI=mysql+pymysql://finance:{DATABASE_PASSWORD}@dbserver/finance \
    finance:latest
```

The app should be fully operational and accessible at http://localhost:8000/
