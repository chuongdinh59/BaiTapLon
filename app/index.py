# this is entry point to start project
from flask import render_template, request, redirect, session, jsonify
from app import app, admin, login
from app.utils.cartUtils import getCartInfo, formatVoucher
from app.models.index import * 
from dao import BookDAO, UserDAO, RecieptDAO
from flask_login import current_user, login_user, login_required, logout_user
@app.route("/")
def index():
    l_bsell = BookDAO.getHomeProduct()
    # l_arrival = BookDAO.getHomeProduct("new-arrivals")
    # l_hots = BookDAO.getHomeProduct("hot-sales")
    # print(l_bsell)
    return render_template("client/index.html" , l_bsell = l_bsell)
@app.route("/e/sale-book")
def sale():
    if current_user.user_role is not UserRoleEnum.WAREHOUSE :
        return redirect("/")
    kw = request.args.get('name')
    b = None
    if kw:
        b = BookDAO.getAll(kw=kw)
    else: 
        b = BookDAO.getAll(page_size=3)
    # l_bsell = BookDAO.getHomeProduct()
    # l_arrival = BookDAO.getHomeProduct("new-arrivals")
    # l_hots = BookDAO.getHomeProduct("hot-sales")
    # print(l_bsell)
    return render_template("admin/sale-book.html", book = b)
@app.route("/shop")
def shop():
    redirect('/shop?page=1')
    page = request.args.get('page')
    category = request.args.get('category')
    kw = request.args.get('kw')
    sort = request.args.get("sort")
    books = BookDAO.getAll(page=page, category = category, kw = kw, sort = sort, page_size=12)
    tags = BookDAO.getTags()
    categories = BookDAO.getCategories()
    return render_template("client/shop.html", books = books, categories = categories, tags = tags)

@app.route("/login" , methods = ["post", "get"])
def loginPage():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserDAO.verifyLogin(username=username, password=password)
        if user: 
            if  user.user_role == UserRoleEnum.USER:
                login_user(user)
                return redirect("/")
            elif user.user_role == UserRoleEnum.WAREHOUSE:
                login_user(user)
                return redirect("/e/sale-book")
            else:
                return redirect('/admin')
    return render_template("layout/login.html")

@app.route('/admin-login', methods =['post'])
def adminLogin():
    username = request.form.get("username")
    password = request.form.get("password")
    user = UserDAO.verifyLogin(username= username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')

@app.route('/apply-voucher', methods = ["get", "post"])
def appyVoucher():
    code =  request.json.get("code")
    voucher = RecieptDAO.applyVoucher(code)
    v = None
    if voucher: 
        v =  jsonify(formatVoucher(voucher=voucher))
    else: 
        v = jsonify({"msg": "voucher này không hợp lệ hoặc hết hạn sử dụng", "status": 0})
    return v
@app.route("/shoping-cart" , methods = ["post", "get"])
def cart():
    if not current_user.is_authenticated:
        return redirect("/login")
    key = app.config['MY_CART']
    cart = {} if key not in session else session[key]
    if request.method == "POST":
        id = str(request.json['id'])
        if id in cart:
            cart[id]['quantity'] = cart[id]['quantity'] + 1
        else:
            name = request.json['name']
            price = request.json['price']
            cart[id] = {
                "id": id,
                "name": name,
                "price": price,
                "quantity": 1,
            }
        session[key] = cart
        return getCartInfo(cart=cart) 
    return render_template("client/cart.html" )

@app.route("/update-cart", methods = ["post"])
def update_cart():
    cart = request.json.get("cart")
    key = app.config['MY_CART']
    session[key] = cart
    return jsonify(getCartInfo(cart=cart))

@app.route("/book:<int:id>")
def book(id):
    b = BookDAO.getBook(id=id)
    comment = BookDAO.getComment(id)
    if b:
        return render_template("client/book-details.html", book = b, comment = comment)
    return render_template("client/index.html")
@login.user_loader
def load_user(user_id):
    return UserDAO.getUserById(user_id=user_id)

@app.route("/checkout")
def checkout():
    return render_template('client/checkout.html')
@app.context_processor
def common_data():
    return {
        'cart_stats':getCartInfo(session.get(app.config['MY_CART'])),
        'cart': session.get(app.config['MY_CART']) or {}
    }

@app.route("/create-reciept", methods = ['post'])
def create_reciept():
    # Tạo reciept trước
    order = request.json.get('order')
    cart = order.get("cart")
    user_id = order.get("user_id")
    address = order.get("address")
    note = order.get("note")
    voucher_id = order.get("voucher_id")
    r = RecieptDAO.createReciept( address , note , voucher_id, user_id)
    if r:
        rd = RecieptDAO.createRecieptDetails(cart=cart, r=r)
        if rd:
            key = app.config['MY_CART']
            cart = {} if key not in session else session[key]
            session[key] = {}
            return jsonify({"status": 1, "msg": "Order thành công"})
    else:
        return jsonify({"status": 0, "msg": "Order thất bại"})
@login_required
@app.route("/order")
def order():
    if current_user.is_authenticated is False:
        return redirect("/login")
    else:
        order = RecieptDAO.getAllReciept(current_user.id)
        return render_template('client/order.html', order = order)

@app.route("/post-comment", methods = ['post'])
def postComent():
    content = request.json.get('content')
    user_id = request.json.get('user_id')
    book_id = request.json.get('book_id')
    cmt = Comment(content = content, user_id = user_id, book_id=book_id)
    if cmt:
        db.session.add(cmt)
        db.session.commit()
        return jsonify({"status": 1})
    return jsonify({"status": 0})

@app.route("/check-cart", methods = ['post'])
def checkCart():
    cart = request.json.get("cart")
    isUnValid = RecieptDAO.checkCart(cart=cart)
    return jsonify({"isValid": isUnValid})
@app.route("/logout")
def loggout():
    logout_user()
    return redirect("/")
if __name__ == '__main__':
    app.run(debug=True, port=80)

