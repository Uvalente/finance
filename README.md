# Stock Mocks

If you are interested in stocks trading but scared of losing all your savings, this is your lucky day!  
Start fake buying and fake selling shares of your favorite company and become a fake millionaire!

This is a Flask web application developed with a TDD approach using pytest.  
I employed the Application Factory pattern to facilitate testing, and Blueprint to organize the app and separate concerns.  
Bootstrap is being used to style the app and achieve a responsive design.

The live version can be found at: [Stock Mocks](https://stock-mocks.herokuapp.com/)

## Run it locally

### API

This web application relies on IEX Cloud API.  
Please visit [iexcloud.io](https://iexcloud.io/) and register for a free account to obtain an API token. 

### Setup

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

If you prefer to use Docker to run the application locally, please start by creating a Docker Image with:

```
docker build -t finance:latest .
```

The Docker version of the application uses MySQL to store the data, therefore it is needed to start a Docker Container for the MySQL database.  
After replacting the password, you can do so with:  

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
