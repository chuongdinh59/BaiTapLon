from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app 
from enum import Enum as UserEnum
from datetime import datetime



class UserRoleEnum(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserModel(BaseModel):
    __tablename__ = 'user'
    firstname = Column(String(100),nullable=False)
    lastname = Column(String(100),nullable=False)
    avatar = Column(Text, nullable = False, default = "")
    birthday = Column(DateTime, nullable = False)
    phone = Column(String(20), nullable = False)
    username = Column(String(50), nullable = False)
    password = Column(String(50), nullable = False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    receipt = relationship('ReceiptModel', backref='user', lazy=False)
    comments = relationship('Comment', backref='user', lazy=True)
    def __str__(self):
        return self.name
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
        return self.name

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
    voucher_id = Column(Integer, ForeignKey(VoucherModel.id), nullable=False)
    details = relationship('ReceiptDetailsModels', backref='receipt', lazy=True)
    def __str__(self):
        return self.name 


class ReceiptDetailsModels(BaseModel):
    __tablename__ = 'receiptdetails'
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receip_id = Column(Integer, ForeignKey(ReceiptModel.id), nullable=False)
    book_id = Column(Integer, ForeignKey(BookModel.id), nullable=False)
    def __str__(self):
        return self.name


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
#   db.session.commit()




