from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime, Date
from sqlalchemy.orm import relationship, backref
from app import db, app 
from enum import Enum as UserEnum
from datetime import datetime
from flask_login import UserMixin


class UserRoleEnum(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserModel(BaseModel, UserMixin):
    __tablename__ = 'user'
    firstname = Column(String(100),nullable=False)
    lastname = Column(String(100),nullable=False)    
    avatar = Column(Text, default = "")
    birthday = Column(Date)
    phone = Column(String(20))
    address = Column(String(255), nullable = False)
    email = Column(String(50), nullable = False)
    username = Column(String(50), nullable = False)
    password = Column(Text, nullable = False)
    user_role = Column(Enum(UserRoleEnum),nullable = False, default=UserRoleEnum.USER)
    receipt = relationship('ReceiptModel', backref='user', lazy=False)
    comments = relationship('Comment', backref='user', lazy=True)
    def __str__(self):
        return self.firstname
class CategoryModel(BaseModel):
    __tablename__ = 'category'
    name = Column(String(100),nullable=False)
    books = relationship('BookModel', backref='category', lazy=False)
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
    thumb = Column(Text)
    category_id = Column(Integer, ForeignKey(CategoryModel.id), nullable=False)
    receipt_details = relationship('ReceiptDetailsModels', backref='book', lazy=True)
    comments = relationship('Comment', backref='book', lazy=True)
    images = relationship('BookImageModel', backref='book', lazy=True)
    tags = relationship('Tag', secondary='book_tag',
                        lazy='subquery',
                        backref=backref('book', lazy=True))
    def __str__(self):
        return self.name
class BookImageModel(BaseModel):
    __tablename__ = 'book_image'
    value = Column(Text)
    book_id = Column(Integer, ForeignKey(BookModel.id), nullable=False)


#Category Model

class Tag(BaseModel):
    name = Column(String(200), nullable=False, unique=True)
    def __str__(self):
        return self.name


class VoucherModel(BaseModel):
    __tablename__ = 'voucher'
    code = Column(String(100), nullable = False)
    rate = Column(Float,nullable=False, default = 0)
    reciept = relationship('ReceiptModel', backref='voucher', lazy=True)
    def __str__(self):
        return self.code

class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    book_id = Column(Integer, ForeignKey(BookModel.id), nullable=False)

    def __str__(self):
        return self.content

class ReceiptModel(BaseModel):
    __tablename__ = 'receipt'
    orderDate = Column(DateTime, nullable = False, default = datetime.now())
    shipDate = Column(DateTime, nullable = False, default = datetime.now())
    shipAddress = Column(String(200), nullable = False)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    note = Column(Text)
    voucher_id = Column(Integer, ForeignKey(VoucherModel.id), nullable=False)
    details = relationship('ReceiptDetailsModels', backref='receipt', lazy=True)
    def __str__(self):
        return self.__tablename__ 


class ReceiptDetailsModels(BaseModel):
    __tablename__ = 'receiptdetails'
    quantity = Column(Integer, default=0)
    # price = Column(Float, default=0)
    receip_id = Column(Integer, ForeignKey(ReceiptModel.id), nullable=False)
    book_id = Column(Integer, ForeignKey(BookModel.id), nullable=False)
    def __str__(self):
        return self.__tablename__


book_tag = db.Table('book_tag',
                    Column('book_id', Integer, ForeignKey('book.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))

with app.app_context():
  db.create_all()
  
  # Add some tag
#   tag1 = Tag(name="Phổ biến")
#   tag2 = Tag(name="Truyện tranh")
#   tag3 = Tag(name="Thiếu nhi")
#   tag4 = Tag(name="Sách giáo khoa lớp 9")
#   db.session.add(tag1)
#   db.session.add(tag2)
#   db.session.add(tag4)
#   db.session.add(tag3)
#   c1 = CategoryModel(name="Văn học")
#   c2 = CategoryModel(name="Kinh tế")
#   c3 = CategoryModel(name="Sách thiếu nhi")
#   c4 = CategoryModel(name="Tâm lý - kỹ năng sống")
#   c5 = CategoryModel(name="Nuôi dạy con")
#   c6 = CategoryModel(name="Sách thiếu nhi")
#   c7 = CategoryModel(name="Tiểu sử - hồi ký")
#   c8 = CategoryModel(name="Sách giáo khoa")
#   c9 = CategoryModel(name="Sách học ngoại ngữ")
#   c10 = CategoryModel(name="Sách nước ngoài")
#   db.session.add(c1)
#   db.session.add(c2)
#   db.session.add(c3)
#   db.session.add(c4)
#   db.session.add(c5)
#   db.session.add(c6)
#   db.session.add(c7)
#   db.session.add(c8)
#   db.session.add(c9)
#   db.session.add(c10)
#   db.session.commit()

    # name = Column(String(100),nullable=False)
    # desc = Column(Text, nullable = False)
    # isOutofStock = Column(Boolean, nullable = False, default = True)
    # unitPrice = Column(Float, nullable = False, default = 0)
    # thumb = Column(Text)

    # b2 = BookModel(name = "Sách 2" , desc = "Sách 2 ", unitPrice = 70000, category_id = 2)
    # b3 = BookModel(name = "Sách 3" , desc = "Sách 3 ", unitPrice = 70000, category_id = 3)
    # b4 = BookModel(name = "Sách 4" , desc = "Sách 4 ", unitPrice = 70000, category_id = 4)
    # db.session.add(b2)
    # db.session.add(b3)
    # db.session.add(b4)
    # db.session.commit()

    




