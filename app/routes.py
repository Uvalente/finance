from app import app

@app.route("/hello")
def hello():
    return "Hello world"

@app.route('/')
def index():
    return 'Index'

@app.route('/login')
def login():
    return 'Log in'