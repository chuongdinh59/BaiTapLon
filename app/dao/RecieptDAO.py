from app.models.index import * 
from app import db
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
        rd = ReceiptDetailsModels(quantity=c.get("quantity"), receip_id=r.id, book_id = c.get("id"))
        db.session.add(rd)
        db.session.commit()
    return True

def getAllReciept(): 
    pass 

