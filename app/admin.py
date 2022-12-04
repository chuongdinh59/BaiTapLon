from flask_admin.contrib.sqla import ModelView
from app.models.index import *

from flask_admin import Admin
admin = Admin(app, name='QUẢN TRỊ BÁN SÁCH', template_mode='bootstrap4')


admin.add_view(ModelView(CategoryModel, db.session))
admin.add_view(ModelView(UserModel, db.session))
# admin.add_view(ModelView(ReceiptModel, db.session))
# admin.add_view(ModelView(RecieptDetailsModels, db.session))
# admin.add_view(ModelView(AuthorModel, db.session))
# admin.add_view(ModelView(FeedbackModel, db.session))
# admin.add_view(ModelView(BookModel, db.session))
# admin.add_view(ModelView(VoucherModel, db.session))




