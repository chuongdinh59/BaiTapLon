from app.models.index import * 
from app import db
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import alias
import hashlib


def getBestSeller():
    # Lấy những sản phẩn có tag name là best seller
    # query = BookModel.query.join(book_tag)\
    #     .filter( BookModel.id == book_tag.c.book_id).alias("temp")
    
    # query = temp.join(Tag).filter(query.c.tag_id == Tag.id).all() 

    pass

def getNewArival():
    pass

def load_products(category_id=None, kw=None):
    query = BookModel.query
    if category_id:
        query = query.filter(BookModel.category_id == category_id)
    if kw:
        query = query.filter(BookModel.name.contains(kw))

    return query.all()

def getAll(page = None):
    query = BookModel.query
    if page:
        page = int(page)
        page_size = 1
        query = query.limit(page_size).offset(page*page_size - 1)
    print(query.all())    
    return query.all()