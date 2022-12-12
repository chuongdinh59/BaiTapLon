from flask_admin.contrib.sqla import ModelView
from app.models.index import *
from utils import QRscan
from flask import redirect, request
from flask_admin import Admin, expose, BaseView,AdminIndexView
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from app.dao import RecieptDAO
from flask_login import logout_user, current_user

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN
class BookManageView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and( current_user.user_role == UserRoleEnum.ADMIN or current_user.user_role == UserRoleEnum.WAREHOUSE)

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)
class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()
class BookModelView (ModelView):
    column_filters = ['name', 'unitPrice','isOutofStock']
    column_labels = {
        'name': 'Tên sản phẩm',
        'unitPrice': 'Giá',
        'desc': 'Mô tả',
        'isOutofStock': 'Tình trạng'
    }
    column_exclude_list = ('thumb')
    can_view_details = True
    can_export = True
    page_size = 5
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'desc': CKTextAreaField
    }
    page_size = 5

class ScanBookView(BaseView):
    @expose('/')
    def index(self):
        data = QRscan.scan()
        return self.render('admin/scan.html', book = data)
class LogoutView(AuthenticatedView):
    @expose('/')
    def logoutview(self):
       logout_user()
       return self.render('admin/index.html')
class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = RecieptDAO.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats = stats)
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = RecieptDAO.count_book_by_cate()
        return self.render('admin/index.html', stats=stats)

admin = Admin(app, name='QUẢN TRỊ BÁN SÁCH', template_mode='bootstrap4' , index_view=MyAdminView())

admin.add_view(AuthenticatedModelView(BookModel, db.session, name="Quản lý sách"))
admin.add_view(AuthenticatedModelView(Tag, db.session))
admin.add_view(LogoutView(name = "Đăng xuất"))

# admin.add_view(ModelView(UserModel, db.session))
admin.add_view(AuthenticatedModelView(ReceiptModel, db.session))
admin.add_view(AuthenticatedModelView(ReceiptDetailsModels, db.session))
admin.add_view(StatsView(name = "Thống kê"))
# admin.add_view(ModelView(AuthorModel, db.session))
# admin.add_view(ModelView(FeedbackModel, db.session))
# admin.add_view(ModelView(VoucherModel, db.session))




