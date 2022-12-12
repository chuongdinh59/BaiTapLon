from app.models.index import * 
from app import db
from flask_login import current_user
from sqlalchemy import func, desc

def getHomeProduct(type = "best seller"):
    # query = BookModel.query.join(Tag, c ,  isouter=True)\
    #     .filter(book_tag.c.tag_id == Tag.id  and BookModel.id == book_tag.c.id)
    # query = query.join(BookModel).filter(BookModel.id == query.id)
    # query = db.session.query(BookModel)\
    #                   .join(book_tag, BookModel.id.__eq__(book_tag.c.book_id))\
    #                   .join(Tag, Tag.id.__eq__(book_tag.c.book_id))
    # query = db.session.query(BookModel.id, BookModel.name, BookModel.desc, BookModel.isOutofStock, BookModel.unitPrice, BookModel.thumb, BookModel.category_id)\
    #                  .join(book_tag, book_tag.c.book_id == BookModel.id)\
    #                  .join(Tag, Tag.name.__eq__("best seller") and book_tag.c.tag_id == Tag.id )
    query = BookModel.query\
                     .join(book_tag, book_tag.c.book_id == BookModel.id)\
                     .join(Tag, book_tag.c.tag_id == Tag.id ).filter(Tag.name == type )
    return query.limit(8).all()



def load_products(category_id=None, kw=None):
    query = BookModel.query
    if category_id:
        query = query.filter(BookModel.category_id == category_id)
    if kw:
        query = query.filter(BookModel.name.contains(kw))

    return query.all()

def getAll(page = None, category = None, kw = None, tag = None, sort = None, page_size = None):
    query = BookModel.query.filter(BookModel.isOutofStock.__eq__(1))
    if category:
        query = query.filter(category == BookModel.category_id)
    if kw:
        kw = kw.replace("+"," ")
        query = query.filter(BookModel.name.contains(kw))
    if page is None:
        page = 1
    if sort:
        if sort == "0":
            query = query.order_by()
        else:
            query = query.order_by(desc(BookModel.unitPrice))
    if tag:
        query = query
    if page_size:
        page = int(page)
        # page_size = 12
        query = query.limit(page_size).offset(page*page_size - page_size)
    return query.all()

def getCategories():
    return CategoryModel.query.all()

def getTags():
    return Tag.query.all()

def getBook(id):
    return BookModel.query.get(id)

def getComment(book_id):
    return Comment.query.join(UserModel, UserModel.id == Comment.user_id).filter(Comment.book_id==book_id)\
        .with_entities(UserModel.firstname, Comment.content, Comment.created_date).all()
