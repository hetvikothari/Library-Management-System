from library import app

@app.route("/home")
def home():
    return 'home page'