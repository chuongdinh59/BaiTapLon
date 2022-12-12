from app.models.index import * 
from app import db
from sqlalchemy import func
def applyVoucher(code = None):
    if code is None:
        return None
    voucher = VoucherModel.query.filter(VoucherModel.code.__eq__(code)).first()
    if voucher:
        return voucher
    return None
    

def createReciept(address , note , voucher_id, user_id):
    # print(cart, address , note , voucher, user_id)
    r = ReceiptModel(shipAddress = address,  user_id = user_id, voucher_id = voucher_id, note = note)
    db.session.add(r)
    db.session.commit()
    return r

def createRecieptDetails(cart, r):
    for c in cart.values():
        rd = ReceiptDetailsModels(quantity=c.get("quantity"), receip_id=r.id, book_id = c.get("id"), price = c.get("price"))
        db.session.add(rd)
        db.session.commit()
        print(c.get("id"))
        b = BookModel.query.get(c.get("id"))
        b.numberOfBook -= int(c.get("quantity"))
        if b.numberOfBook <= 0:
            b.isOutofStock = 0
        # if new_no == 0:
        db.session.commit()
    return True

def getAllReciept(user_id): 
    query = ReceiptModel.query.join(UserModel,ReceiptDetailsModels ).filter(UserModel.id == ReceiptModel.user_id and ReceiptDetailsModels.receip_id == ReceiptModel.id)\
        .filter(UserModel.id.__eq__(user_id))
    return query.all()

def count_book_by_cate():
    query = db.session.query(CategoryModel.id, CategoryModel.name, func.count(BookModel.id))\
                     .join(BookModel, BookModel.category_id.__eq__(CategoryModel.id), isouter=True)\
                     .group_by(CategoryModel.id)
    return query.all()

def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(BookModel.id, BookModel.name, func.sum(ReceiptDetailsModels.quantity*ReceiptDetailsModels.price))\
                      .join(ReceiptDetailsModels, ReceiptDetailsModels.book_id.__eq__(BookModel.id))\
                      .join(ReceiptModel, ReceiptModel.id.__eq__(ReceiptDetailsModels.receip_id))
    if kw:
        query = query.filter(BookModel.name.contains(kw))

    if from_date:
        query = query.filter(ReceiptModel.orderDate.__ge__(from_date))

    if to_date:
        query = query.filter(ReceiptModel.orderDate.__le__(to_date))

    return query.group_by(BookModel.id).order_by(BookModel.name).all()

def checkCart(cart):
    isUnValid = {}
    for c in cart.values():
        b = BookModel.query.get(c.get("id"))
        if b.numberOfBook - int(c.get("quantity")) < 0:
            isUnValid.update({c.get("id"): {"id": b.id, "name": b.name}})
    return isUnValid

with app.app_context():
    # count_book_by_cate()
    print(count_book_by_cate())
    # pass

