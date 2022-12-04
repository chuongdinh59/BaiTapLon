from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app 
from enum import Enum as UserEnum
from datetime import datetime

book_cate = db.Table('book_cate',
                    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
                    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True))

book_author = db.Table('book_author',
                    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
                    Column('author_id', Integer, ForeignKey('author.id'), primary_key=True))
class UserRoleEnum(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRoleModel(BaseModel):
    __tablename__ = 'userrole'
    name = Column(String(20), nullable = False, default = UserRoleEnum.USER)
    user = relationship('UserModel', backref='userrole', lazy=False)
    def __str__(self):
        return self.name

class UserModel(BaseModel):
    __tablename__ = 'user'
    firstname = Column(String(100),nullable=False)
    lastname = Column(String(100),nullable=False)
    avatar = Column(Text, nullable = False, default = "")
    birthday = Column(DateTime, nullable = False)
    phone = Column(String(20), nullable = False)
    username = Column(String(50), nullable = False)
    password = Column(String(50), nullable = False)
    user_role_id =  Column(Integer, ForeignKey(UserRoleModel.id), nullable=False)
    reciept = relationship('ReceiptModel', backref='user', lazy=False)
    def __str__(self):
        return self.name

class AuthorModel(BaseModel):
   __tablename__ = 'author'
   name = Column(String(100),nullable=False)
   def __str__(self):
      return self.name

class BookModel(BaseModel):
    __tablename__ = 'book'
    name = Column(String(100),nullable=False)
    desc = Column(Text, nullable = False)
    isOutofStock = Column(Boolean, nullable = False, default = True)
    unitPrice = Column(Float, nullable = False, default = 0)
    receipt_details = relationship('RecieptDetailsModels', backref='book', lazy=True)
    def __str__(self):
        return self.name

#Category Model
class CategoryModel(BaseModel):
    __tablename__ = 'category'
    name = Column(String(100),nullable=False)
    def __str__(self):
        return self.name

# Feedback Model
class FeedbackModel(BaseModel):
    __tablename__ = 'feedback'
    content = Column(Text)
    isProcess = Column(Boolean, nullable = False, default = False)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    def __str__(self):
        return self.name

class VoucherModel(BaseModel):
    __tablename__ = 'voucher'
    code = Column(String(100), nullable = False)
    rate = Column(Float,nullable=False, default = 0)
    reciept = relationship('ReceiptModel', backref='voucher', lazy=True)
    def __str__(self):
        return self.name



class ReceiptModel(BaseModel):
    __tablename__ = 'receipt'
    orderDate = Column(DateTime, nullable = False, default = datetime.now())
    shipDate = Column(DateTime, nullable = False, default = datetime.now())
    shipAddress = Column(String(200), nullable = False)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    voucher_id = Column(Integer, ForeignKey(VoucherModel.id), nullable=False)
    details = relationship('ReceiptDetailsModels', backref='receipt', lazy=True)
    def __str__(self):
        return self.name 


class RecieptDetailsModels(BaseModel):
    __tablename__ = 'recieptdetails'
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(ReceiptModel.id), nullable=False)
    book_id = Column(Integer, ForeignKey(BookModel.id), nullable=False)
    def __str__(self):
        return self.name






with app.app_context():
  db.create_all()




