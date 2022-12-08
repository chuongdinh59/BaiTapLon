# this is entry point to start project
from flask import render_template, request
from app import app, admin
from dao import BookDAO

@app.route("/")
def index():
    # BookDAO.getBestSeller()
    return render_template("client/index.html")
@app.route("/shop")
def shop():
    page = request.args.get('page')
    print(page)
    books = BookDAO.getAll(page=page)
    category = request.args.get('category')
    return render_template("client/shop.html", books = books)
if __name__ == '__main__':
    app.run(debug=True, port=80)

