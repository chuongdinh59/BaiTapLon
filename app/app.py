# this is entry point to start project

from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("layout/login.html")




if __name__ == '__main__':
    app.run(debug=True)