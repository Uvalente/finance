from app import app

@app.route("/hello")
def index():
    return "Hello world"