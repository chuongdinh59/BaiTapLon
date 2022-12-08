from flask_admin.contrib.sqla import ModelView
from app.models.index import *
from utils import QRscan
from flask_admin import Admin, expose, BaseView
from wtforms import TextAreaField
from wtforms.widgets import TextArea
admin = Admin(app, name='QUẢN TRỊ BÁN SÁCH', template_mode='bootstrap4')



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
        print(data)
        return self.render('admin/scan.html', book = data)

admin.add_view(BookModelView(BookModel, db.session))
admin.add_view(ModelView(Tag, db.session))
admin.add_view(ModelView(BookImageModel, db.session))
# admin.add_view(ScanBookView(name = "Scan_Book"))

# admin.add_view(ModelView(UserModel, db.session))
# admin.add_view(ModelView(ReceiptModel, db.session))
# admin.add_view(ModelView(ReceiptDetailsModels, db.session))
# admin.add_view(ModelView(AuthorModel, db.session))
# admin.add_view(ModelView(FeedbackModel, db.session))
# admin.add_view(ModelView(VoucherModel, db.session))




