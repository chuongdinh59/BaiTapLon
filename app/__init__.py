from flask import Flask 
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
app.secret_key = '12#^&*+_%&*)(*(&(*^&^$%$#((*65t87676'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/bookstore_1?charset=utf8mb4' % quote('75760208lv')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MY_CART'] = 'cart'
db = SQLAlchemy(app=app)
login = LoginManager(app = app)




