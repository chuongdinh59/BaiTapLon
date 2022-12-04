# this is entry point to start project
from flask import render_template
from app import app, admin

@app.route("/")
def index():
    return render_template("client/shop.html")

if __name__ == '__main__':
    app.run(debug=True)

