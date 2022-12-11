def getCartInfo(cart=None):
    total_amount, total_quantity = 0, 0
    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']
    return {
        'total_amount': total_amount,
        'total_quantity': total_quantity,
    }
def formatVoucher(voucher):
    return {
        "id": voucher.id,
        "rate": voucher.rate,
        "code": voucher.code,
        "msg": "Sử dụng voucher thành công",
        "status": 1
    }