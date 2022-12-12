from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime, Date
from sqlalchemy.orm import relationship, backref
from app import db, app 
from enum import Enum as UserEnum
from datetime import datetime
from flask_login import UserMixin


class UserRoleEnum(UserEnum):
    USER = 1
    ADMIN = 2
    WAREHOUSE = 3


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
    numberOfBook =  Column(Integer,default=50, nullable = False)
    receipt_details = relationship('ReceiptDetailsModels', backref='book', lazy=True)
    comments = relationship('Comment', backref='book', lazy=True)
    tags = relationship('Tag', secondary='book_tag',
                        lazy='subquery',
                        backref=backref('book', lazy=True))
    def __str__(self):
        return self.name
# class BookImageModel(BaseModel):
#     __tablename__ = 'book_image'
#     value = Column(Text)
#     book_id = Column(Integer, ForeignKey(BookModel.id), nullable=False)


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
    voucher_id = Column(Integer, ForeignKey(VoucherModel.id), )
    details = relationship('ReceiptDetailsModels', backref='receipt', lazy=True)
    def __str__(self):
        return self.__tablename__ 


class ReceiptDetailsModels(BaseModel):
    __tablename__ = 'receiptdetails'
    quantity = Column(Integer, default=0)
    price = Column(Integer, default=0)
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
    # b2 = BookModel(name = "Nhà Giả Kim (Tái Bản 2020)" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 55000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_36793.jpg")
    # b3 = BookModel(name = "Đất Trời Vần Vũ" , desc = "Đất trời vần vũ được đánh giá rất cao khi xuất bản lần đầu 10 năm trước, đoạt giải C tiểu thuyết Hội Nhà văn VN 2006-2010, tuy khi còn ở dạng bản thảo, đây từng được xem là 1 cuốn sách khó nhằn với giới chức Đất trời vần vũ được đánh giá rất cao khi xuất bản lần đầu 10 năm trước, đoạt giải C tiểu thuyết Hội Nhà văn VN 2006-2010, tuy khi còn ở dạng bản thảo, đây từng được xem là 1 cuốn sách khó nhằn với giới chức kiểm duyệt. Nếu chờ đợi 1 tiểu thuyết thuật tả thông thường, dễ nắm bắt, thì sẽ ít nhiều thất vọng. Là 1 trong rất ít tiểu thuyết viết về Thiên chúa giáo ở Việt Nam, nhưng lồng trong đức tin Thiên chúa là câu chuyện về một vùng đất thiêng từ thời cổ sử lập đất đến thời hiện đại. Biểu tượng xuyên suốt những câu chuyện chồng chéo “xuyên không” là lưỡi dao thiêng ở vùng đất tên Cù lao Dao. Câu chuyện được kể bám theo biểu tượng đó ", unitPrice = 83000, category_id = 1, thumb = "https://cdn0.fahasa.com/media/catalog/product/i/m/image_186065.jpg")
    # b4 = BookModel(name = "Bước Chậm Lại Giữa Thế Gian Vội Vã (Tái Bản 2018)" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng?Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 59000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/b/u/buoc_cham_lai_giua_the_gian_voi_va.u335.d20160817.t102115.612356.jpg")
    # b5 = BookModel(name = "Cây Cam Ngọt Của Tôi" , desc = "“Vị chua chát của cái nghèo hòa trộn với vị ngọt ngào khi khám phá ra những điều khiến cuộc đời này đáng sống... một tác phẩm kinh điển của Brazil.” - Booklist“Một cách nhìn cuộc sống gần như hoàn chỉnh từ con mắt trẻ thơ… có sức mạnh sưởi ấm và làm tan nát cõi lòng, dù người đọc ở lứa tuổi nào.” - The National Hãy làm quen với Zezé, cậu bé tinh nghịch siêu hạng đồng thời cũng đáng yêu bậc nhất, với ước mơ lớn lên trở thành nhà thơ cổ thắt nơ bướm. Chẳng phải ai cũng công nhận khoản “đáng yêu” kia đâu nhé. Bởi vì, ở cái xóm ngoại ô nghèo ấy, nỗi khắc khổ bủa vây đã che mờ mắt người ta trước trái tim thiện lương cùng trí tưởng tượng tuyệt vời của cậu bé con năm tuổi. ", unitPrice = 75000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_217480.jpg")
    # b6 = BookModel(name = "Tôi Là Bêtô (Tái Bản 2018)" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 68000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_180164_1_43_1_57_1_4_1_2_1_210_1_29_1_98_1_25_1_21_1_5_1_3_1_18_1_18_1_45_1_26_1_32_1_14_1_1236.jpg")
    # b7 = BookModel(name = "Rừng Nauy (Tái Bản 2021)" , desc = "Câu chuyện bắt đầu từ một chuyến bay trong ngày mưa ảm đạm, một người đàn ông 37 tuổi chợt nghe thấy bài hát gắn liền với hình ảnh người yêu cũ, thế là quá khứ ùa về xâm chiếm thực tại. Mười tám năm trước, người đàn ông ấy là chàng Toru Wanatabe trẻ trung, mỗi chủ nhật lại cùng nàng Naoko lang thang vô định trên những con phố Tokyo. Họ sánh bước bên nhau để thấy mình còn sống, còn tồn tại, và gắng gượng tiếp tục sống, tiếp tục tồn tại sau cái chết của người bạn cũ Kizuki. Cho đến khi Toru nhận ra rằng mình thực sự yêu và cần có Naoko thì cũng là lúc nàng không thể chạy trốn những ám ảnh quá khứ, không thể hòa nhập với cuộc sống thực tại và trở về dưỡng bệnh trong một khu trị liệu khép kín. Toru, bên cạnh giảng đường vô nghĩa chán ngắt, bên cạnh những đêm chơi bời chuyển từ cảm giác thích thú đến uể oải, ghê tởm...vẫn kiên nhẫn chờ đợi và hy vọng vào sự hồi phục của Naoko. Cuối cùng, những lá thư, những lần thăm hỏi, hồi ức về  lần ân ái duy nhất của Toru không thể níu Naoko ở lại, nàng chọn cái chết như một lối đi thanh thản. Từ trong mất mát, Toru nhận ra rằng mình cần tiếp tục sống và bắt đầu tình yêu mới với Midori.", unitPrice = 120000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_240307.jpg")

    # b8 = BookModel(name = "Tôi Thấy Hoa Vàng Trên Cỏ Xanh (Bản In Mới - 2018)" , desc = "Những câu chuyện nhỏ xảy ra ở một ngôi làng nhỏ: chuyện người, chuyện cóc, chuyện ma, chuyện công chúa và hoàng tử , rồi chuyện đói ăn, cháy nhà, lụt lội,... Bối cảnh là trường học, nhà trong xóm, bãi tha ma. Dẫn chuyện là cậu bé 15 tuổi tên Thiều. Thiều có chú ruột là chú Đàn, có bạn thân là cô bé Mận. Nhưng nhân vật đáng yêu nhất lại là Tường, em trai Thiều, một cậu bé học không giỏi. Thiều, Tường và những đứa trẻ sống trong cùng một làng, học cùng một trường, có biết bao chuyện chung. Chúng nô đùa, cãi cọ rồi yêu thương nhau, cùng lớn lên theo năm tháng, trải qua bao sự kiện biến cố của cuộc đời.", unitPrice = 85000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_180164_1_43_1_57_1_4_1_2_1_210_1_29_1_98_1_25_1_21_1_5_1_3_1_18_1_18_1_45_1_26_1_32_1_14_1_2199.jpg")
    # b9 = BookModel(name = "Làm Bạn Với Bầu Trời" , desc = "Làm Bạn Với Bầu Trời Một câu chuyện giản dị, chứa đầy bất ngờ cho tới trang cuối cùng. Và đẹp lộng lẫy, vì lòng vị tha và tình yêu thương, khiến mắt rưng rưng vì một nỗi mừng vui hân hoan. Cuốn sách như một đốm lửa thắp lên lòng khát khao sống tốt trên đời.Viết về điều tốt đã không dễ, viết sao cho người đọc có thể đón nhận đầy cảm xúc tích cực, và muốn được hưởng, được làm những điều tốt dù nhỏ bé... mới thật là khó. Làm bạn với bầu trời của Nguyễn Nhật Ánh đã làm được điều này. ", unitPrice = 88000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/u/n/untitled-2_44.jpg")
    # b10 = BookModel(name = "Dấu Chân Trên Cát (Tái Bản 2020)" , desc = "“Dấu chân trên cát” là tác phẩm được dịch giả Nguyên Phong phóng tác kể về xã hội Ai Cập thế kỷ thứ XIV trước CN, qua lời kể của nhân vật chính -  Sinuhe. Ngày nay, người ta biết đến triều đại các vua chúa Ai Cập thời cổ qua sách vở của người Hy Lạp. Sở dĩ các sử gia Hy Lạp biết được các chi tiết này vì họ đã học hỏi từ người Ai Cập bị đày biệt xứ tên là Sinuhe. Đây là một nhân vật lạ lùng, đã có công mang văn minh Ai Cập truyền vào Hy Lạp khi quốc gia này còn ở tình trạng kém mở mang so với Ai Cập lúc đó.Các sử gia ngày nay đã đưa ra nhiều giả thuyết về nhân vật Sinuhe này. Có người cho rằng ông là một lái buôn đến Hy Lạp lập nghiệp, nhưng làm sao lái buôn lại mở trường dạy học và để lại nhiều tài liệu quý giá như thế được? Từ ngàn xưa,  chỉ riêng giai cấp vua chúa là giáo sĩ mới được hưởng quy chế giáo dục toàn vẹn như vậy mà thôi. ", unitPrice = 118000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_12629_1.jpg")
    # b11 = BookModel(name = "Có Hai Con Mèo Ngồi Bên Cửa Sổ (Tái Bản 2018)" , desc = "Có Hai Con Mèo Ngồi Bên Cửa Sổ (Tái Bản 2018).CÓ HAI CON MÈO NGỒI BÊN CỬA SỔ là tác phẩm đầu tiên của nhà văn Nguyễn Nhật Ánh viết theo thể loại đồng thoại. Đặc biệt hơn nữa là viết về tình bạn của hai loài vốn là thù địch của nhau mèo và chuột. Đó là tình bạn giữa mèo Gấu và chuột Tí Hon.Để biết tại sao mèo Gấu lại chơi thân với chuột Tí Hon, thì mời bạn hãy mở sách ra.Cuốn truyện mỏng mảnh vừa phải, hình vẽ của họa sĩ Hoàng Tường sinh động đến từng nét nũng nịu hay kiêu căng của nàng mèo người yêu mèo Gấu, câu chuyện thì hấp dẫn duyên dáng điểm những bài thơ tình lãng mạn nao lòng song đọc to lên thì khiến cười hinh hích… ", unitPrice = 68000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/c/o/cohaiconmeobencuasotaiban2018_1.jpg")
    # b12 = BookModel(name = "999 Lá Thư Gửi Cho Chính Mình - Mong Bạn Trở Thành Phiên Bản Hoàn Hảo Nhất (Tập 1)" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 103000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/9/9/999lathu-taibbb1_2.jpg")
    # b13 = BookModel(name = "Bí Mật Của Naoko" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta”", unitPrice = 86000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_9655.jpg")
    # b14 = BookModel(name = "Số Đỏ" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta”", unitPrice = 44000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_220968.jpg")
    # b15 = BookModel(name = "Tìm Em Nơi Anh - Find Me" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta”", unitPrice = 92000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_225272.jpg")
    # b16 = BookModel(name = "Những Đêm Không Ngủ Những Ngày Chậm Trôi" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 68000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_227604.jpg")
    # b17 = BookModel(name = "Chuyện Kể Rằng Có Nàng Và Tôi" , desc = "Làm Bạn Với Bầu Trời Một câu chuyện giản dị, chứa đầy bất ngờ cho tới trang cuối cùng. Và đẹp lộng lẫy, vì lòng vị tha và tình yêu thương, khiến mắt rưng rưng vì một nỗi mừng vui hân hoan. Cuốn sách như một đốm lửa thắp lên lòng khát khao sống tốt trên đời. Viết về điều tốt đã không dễ, viết sao cho người đọc có thể đón nhận đầy cảm xúc tích cực, và muốn được hưởng, được làm những điều tốt dù nhỏ bé... mới thật là khó. Làm bạn với bầu trời của Nguyễn Nhật Ánh đã làm được điều này. ", unitPrice = 57000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/b/i/bia_chuyen-ke-rang-co-nang-va-toi_final.jpg")
    # b18 = BookModel(name = "Có Một Ngày, Bố Mẹ Sẽ Già Đi" , desc = "Làm Bạn Với Bầu Trời Một câu chuyện giản dị, chứa đầy bất ngờ cho tới trang cuối cùng. Và đẹp lộng lẫy, vì lòng vị tha và tình yêu thương, khiến mắt rưng rưng vì một nỗi mừng vui hân hoan. Cuốn sách như một đốm lửa thắp lên lòng khát khao sống tốt trên đời. Viết về điều tốt đã không dễ, viết sao cho người đọc có thể đón nhận đầy cảm xúc tích cực, và muốn được hưởng, được làm những điều tốt dù nhỏ bé... mới thật là khó. Làm bạn với bầu trời của Nguyễn Nhật Ánh đã làm được điều này. ", unitPrice = 76000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/c/o/co-mot-ngay-bo-me-se-gia-di.jpg")
    # b19 = BookModel(name = "Vui Vẻ Không Quạu Nha (Tái Bản 2021)" , desc = "Làm Bạn Với Bầu Trời Một câu chuyện giản dị, chứa đầy bất ngờ cho tới trang cuối cùng. Và đẹp lộng lẫy, vì lòng vị tha và tình yêu thương, khiến mắt rưng rưng vì một nỗi mừng vui hân hoan. Cuốn sách như một đốm lửa thắp lên lòng khát khao sống tốt trên đời. Viết về điều tốt đã không dễ, viết sao cho người đọc có thể đón nhận đầy cảm xúc tích cực, và muốn được hưởng, được làm những điều tốt dù nhỏ bé... mới thật là khó. Làm bạn với bầu trời của Nguyễn Nhật Ánh đã làm được điều này. ", unitPrice = 55000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_33312_2.jpg")
    # b20 = BookModel(name = "Màu Nhạt Nắng" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 119000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_33312_2.jpg")
    # b21 = BookModel(name = "Hẹn Nhau Phía Sau Tan Vỡ" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 70000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/b/i/bia_hen-nhau-sau-tan-vo_2.jpg")
    # b22 = BookModel(name = "Hay Chúng Mình Đừng Hứa Hẹn Gì Nhau" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 92000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/g/t/gt_hay-ch_ng-m_nh-_ng-h_a-h_n-g_-nhaubia1600.jpg")
    # b23 = BookModel(name = "Hai Mặt Của Gia Đình" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 78000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_31258.jpg")
    # b24 = BookModel(name = "Lì Quá Để Nói Quài" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 62000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/9/7/9786043556797.jpg")
    # b25 = BookModel(name = "Đừng Nhạt Nữa" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 76000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_226024.jpg")
    # b26 = BookModel(name = "Cảm Ơn Anh Đã Đánh Mất Em" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 79000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/b/b/bbbcam-on-anh-da-danh-mat-em.jpg")
    # b27 = BookModel(name = "Thế Giới Này Âm Thầm Yêu Em" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 108000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/b/i/bia-1_the-gioy-am-tham-yeu-em.jpg")
    # b28 = BookModel(name = "Vô Thường (Tái Bản 2018)" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 63000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/f/7/f7992bd171a14232b2ca827967c7f774_310x514_1.jpg")
    # b29 = BookModel(name = "Phía Sau Nghi Can X (Tái Bản 2019)" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 87000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_187738.jpg")
    # b30 = BookModel(name = "Thiên Thần Và Ác Quỷ (Tái Bản 2020)" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 146300, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/t/h/thien-than-va-ac-quy-bia-truoc_tb_.jpg")
    # b31 = BookModel(name = "Vụ Ám Sát Ông Roger Ackroyd (Tái Bản 2019)" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc.", unitPrice = 100000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_180925.jpg")
    # b32 = BookModel(name = "Thôn Tám Mộ" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 108000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/t/h/thon-tam-mo---bia-1.jpg")
    # b33 = BookModel(name = "Luật Im Lặng (Mario Puzo)" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 76000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_119110.jpg")
    # b34 = BookModel(name = "Kẻ Lãng Quên" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 148000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/9/7/9786043494624.jpg")
    # b35 = BookModel(name = "Vén Màn Bí Mật - Here To Stay" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 103000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_45248.jpg")
    # b36 = BookModel(name = "Ẩn Ức Trắng" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 54500, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_31871.jpg")
    # b37 = BookModel(name = "Vệt Sóng Tràn" , desc = "Truyện Tôi là Bêtô là sáng tác mới nhất của nhà văn Nguyễn Nhật Ánh được viết theo phong cách hoàn toàn khác so với những tác phẩm trước đây của ông. Những mẩu chuyện, hay những phát hiện của chú chó Bêtô đầy thú vị, vừa hài hước, vừa chiêm nghiệm một cách nhẹ nhàng “vô vàn những điều thú vị mà cuộc sống cố tình giấu kín ở ngóc ngách nào đó trong tâm hồn của mỗi chúng ta” ", unitPrice = 74500, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/b/_/b_a-tr_c-v_t-s_ng-tr_n.jpg")
    # b38 = BookModel(name = "Hang Dã Thú (Tái Bản 2018)" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 77500, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_178727.jpg")
    # b39 = BookModel(name = "Cổ Học Tinh Hoa (Tái Bản 2021)" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 88000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_231631.jpg")
    # b40 = BookModel(name = "Thi Nhân Việt Nam (Tái Bản 2022)" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 76000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/8/9/8935236426466.jpg")
    # b41 = BookModel(name = "Bước Ra Từ Thầm Lặng" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 84000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/9/7/9786045805619.jpg")
    # b42 = BookModel(name = "Để Thành Nhà Văn (Tái Bản 2021)" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 40000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_226231.jpg")
    # b43 = BookModel(name = "Thư Gửi Con (Tái Bản)" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 47000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195110.jpg")
    # b44 = BookModel(name = "Tổng Biên Tập - Chuyện Người Trong Cuộc" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc.", unitPrice = 228000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_237216.jpg")
    # b45 = BookModel(name = "5678 Bước Chân Quanh Hồ Gươm" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 73000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/8/9/8934974135036.jpg")
    # b46 = BookModel(name = "Bạn Văn Bạn Mình: Cây Bút Đời Người" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 72000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_240035.jpg")
    # b47 = BookModel(name = "Lộn Tùng Phèo" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước.", unitPrice = 68000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_228413.jpg")
    # b48 = BookModel(name = "Tuyệt Vọng Lời" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 68000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_228417.jpg")
    # b49 = BookModel(name = "Tôi Đi Tìm Tôi" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 128000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_1805.jpg")
    # b50 = BookModel(name = "Mùi Hương Trầm" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 158000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/3/3/3300000014302.jpg")
    # b51 = BookModel(name = "Đi Bộ Xuyên Việt Với Cây Đàn Guitar" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 99000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_186778.jpg")
    # b52 = BookModel(name = "Các Bạn Tôi Ở Trên Ấy" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 111000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/_/-/_-tr_n-_y_b_a-1.jpg")
    # b53 = BookModel(name = "Giấc Mơ Mỹ - Đường Đến Stanford" , desc = "Tiểu thuyết Nhà giả kim của Paulo Coelho như một câu chuyện cổ tích giản dị, nhân ái, giàu chất thơ, thấm đẫm những minh triết huyền bí của phương Đông. Trong lần xuất bản đầu tiên tại Brazil vào năm 1988, sách chỉ bán được 900 bản. Nhưng, với số phận đặc biệt của cuốn sách dành cho toàn nhân loại, vượt ra ngoài biên giới quốc gia, Nhà giả kim đã làm rung động hàng triệu tâm hồn, trở thành một trong những cuốn sách bán chạy nhất mọi thời đại, và có thể làm thay đổi cuộc đời người đọc. ", unitPrice = 68000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/8/9/8936117740381_1_1_1.jpg")
    # b54 = BookModel(name = "Trái Tim Trên Những Con Đường" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 71000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/t/r/traitimtrenconduong-1.jpg")
    # b55 = BookModel(name = "Giáo Sư Phiêu Lưu Ký - Tản Mạn Với Một Nhà Toán Học" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 140000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/g/s/gsplkbc.jpg")
    # b56 = BookModel(name = "Du Ký Phan Quang - Tiếc Nuối Hoa Hồng" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 360000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/d/u/du-k_-phan-quang--600.jpg")
    # b57 = BookModel(name = "Italy, Đi Rồi Sẽ Đến" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 69300, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/8/9/8935251406702_1.jpg")
    # b58 = BookModel(name = "Ta Ba Lô Trên Đất Á (Tái Bản 2018)" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 86600, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/t/a/ta_ba_lo_tren_dat_a-02.jpg")
    # b59 = BookModel(name = "Trên Đường Về Nhớ Đầy" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 68000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/n/x/nxbtre_full_08472018_094704.jpg")
    # b60 = BookModel(name = "Chốc Lát Những Bến Bờ" , desc = "Chen vai thích cánh để có một chỗ bám trên xe buýt giờ đi làm, nhích từng xentimét bánh xe trên đường lúc tan sở, quay cuồng với thi cử và tiến độ công việc, lu bù vướng mắc trong những mối quan hệ cả thân lẫn sơ… bạn có luôn cảm thấy thế gian xung quanh mình đang xoay chuyển quá vội vàng? Nếu có thể, hãy tạm dừng một bước. ", unitPrice = 92000, category_id = 1, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_185479.jpg")
    # b61 = BookModel(name = "Thay Đổi Cuộc Sống Với Nhân Số Học" , desc = "Đầu năm 2020, chuỗi chương trình “Thay đổi cuộc sống với Nhân số học” của  biên tập viên, người dẫn chương trình quen thuộc tại Việt Nam Lê Đỗ Quỳnh Hương ra đời trên Youtube, với mục đích chia sẻ kiến thức, giúp mọi người tìm hiểu và phát triển, hoàn thiện bản thân, các mối quan hệ xã hội thông qua bộ môn Nhân số học. Chương trình đã nhận được sự yêu mến và phản hồi tích cực của rất nhiều khán giả và độc giả sau mỗi tập phát sóng. Nhân số học là một môn nghiên cứu sự tương quan giữa những con số trong ngày sinh, cái tên với cuộc sống, vận mệnh, đường đời và tính cách của mỗi người. Bộ môn này đã được nhà toán học Pythagoras khởi xướng cách đây 2.600 năm và sau này được nhiều thế hệ học trò liên tục kế thừa, phát triển.   ", unitPrice = 175000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/t/d/tdcsvnsh.jpg")
    # b62 = BookModel(name = "Đọc Vị Bất Kỳ Ai (Tái Bản 2019)" , desc = "Cuốn sách được chia làm hai phần và 15 chương: Phần 1: Bảy câu hỏi cơ bản: Học cách phát hiện ra điều người khác nghĩ hay cảm nhận một cách dễ dàng và nhanh chóng trong bất kỳ hoàn cảnh nào. Phần 2: Những kế hoạch chi tiết cho hoạt động trí óc - hiểu được quá trình ra quyết định. Vượt ra ngoài việc đọc các suy nghĩ và cảm giác đơn thuần: Hãy học cách người khác suy nghĩ để có thể nắm bắt bất kỳ ai, phán đoán hành xử và hiểu được họ còn hơn chính bản thân họ. ", unitPrice = 69000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_12542.jpg")
    # b63 = BookModel(name = "Hiểu Về Trái Tim (Tái Bản 2019)" , desc = "Xuất bản lần đầu tiên vào năm 2011, Hiểu Về Trái Tim trình làng cũng lúc với kỷ lục: cuốn sách có số lượng in lần đầu lớn nhất: 100.000 bản. Trung tâm sách kỷ lục Việt Nam công nhận kỳ tích ấy nhưng đến nay, con số phát hành của Hiểu về trái tim vẫn chưa có dấu hiệu chậm lại. Là tác phẩm đầu tay của nhà sư Minh Niệm, người sáng lập dòng thiền hiểu biết (Understanding Meditation), kết hợp giữa tư tưởng Phật giáo Đại thừa và Thiền nguyên thủy Vipassana, nhưng Hiểu Về Trái Tim không phải tác phẩm thuyết giáo về Phật pháp. Cuốn sách rất “đời” với những ưu tư của một người tu nhìn về cõi thế. Ở đó, có hạnh phúc, có đau khổ, có tình yêu, có cô đơn, có tuyệt vọng, có lười biếng, có yếu đuối, có buông xả… Nhưng, tất cả những hỉ nộ ái ố ấy đều được khoác lên tấm áo mới, một tấm áo tinh khiết và xuyên suốt, khiến người đọc khi nhìn vào, đều thấy mọi sự như nhẹ nhàng hơn… ", unitPrice = 115000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_14922.jpg")
    # b64 = BookModel(name = "Đời Ngắn Đừng Ngủ Dài (Tái Bản 2018)" , desc = "“Mọi lựa chọn đều giá trị. Mọi bước đi đều quan trọng. Cuộc sống vẫn diễn ra theo cách của nó, không phải theo cách của ta. Hãy kiên nhẫn. Tin tưởng. Hãy giống như người thợ cắt đá, đều đặn từng nhịp, ngày qua ngày. Cuối cùng, một nhát cắt duy nhất sẽ phá vỡ tảng đá và lộ ra viên kim cương. Người tràn đầy nhiệt huyết và tận tâm với việc mình làm không bao giờ bị chối bỏ. Sự thật là thế.” Bằng những lời chia sẻ thật ngắn gọn, dễ hiểu về những trải nghiệm và suy ngẫm trong đời, Robin Sharma tiếp tục phong cách viết của ông từ cuốn sách Điều vĩ đại đời thường để mang đến cho độc giả những bài viết như lời tâm sự, vừa chân thành vừa sâu sắc. ", unitPrice = 55000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_180164_1_43_1_57_1_4_1_2_1_210_1_29_1_98_1_25_1_21_1_5_1_3_1_18_1_18_1_45_1_26_1_32_1_14_1_2730.jpg")
    # b65 = BookModel(name = "Rèn Luyện Tư Duy Phản Biện" , desc = "Như bạn có thể thấy, chìa khóa để trở thành một người có tư duy phản biện tốt chính là sự tự nhận thức. Bạn cần phải đánh giá trung thực những điều trước đây bạn nghĩ là đúng, cũng như quá trình suy nghĩ đã dẫn bạn tới những kết luận đó. Nếu bạn không có những lý lẽ hợp lý, hoặc nếu suy nghĩ của bạn bị ảnh hưởng bởi những kinh nghiệm và cảm xúc, thì lúc đó hãy cân nhắc sử dụng tư duy phản biện! Bạn cần phải nhận ra được rằng con người, kể từ khi sinh ra, rất giỏi việc đưa ra những lý do lý giải cho những suy nghĩ khiếm khuyết của mình. Nếu bạn đang có những kết luận sai lệch này thì có một sự thật là những đức tin của bạn thường mâu thuẫn với nhau và đó thường là kết quả của thiên kiến xác nhận, nhưng nếu bạn biết điều này, thì bạn đã tiến gần hơn tới sự thật rồi! ", unitPrice = 84000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_18448.jpg")
    # b66 = BookModel(name = "Tuổi Trẻ Đáng Giá Bao Nhiêu (Tái Bản 2021)" , desc = "“Bạn hối tiếc vì không nắm bắt lấy một cơ hội nào đó, chẳng có ai phải mất ngủ. Bạn trải qua những ngày tháng nhạt nhẽo với công việc bạn căm ghét, người ta chẳng hề bận lòng. Bạn có chết mòn nơi xó tường với những ước mơ dang dở, đó không phải là việc của họ. Suy cho cùng, quyết định là ở bạn. Muốn có điều gì hay không là tùy bạn. Nên hãy làm những điều bạn thích. Hãy đi theo tiếng nói trái tim. Hãy sống theo cách bạn cho là mình nên sống. Vì sau tất cả, chẳng ai quan tâm.” ", unitPrice = 59000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_239651.jpg")
    # b67 = BookModel(name = "Sức Mạnh Tiềm Thức (Tái Bản 2021)" , desc = "Là một trong những quyển sách về nghệ thuật sống nhận được nhiều lời ngợi khen và bán chạy nhất mọi thời đại, Sức Mạnh Tiềm Thức đã giúp hàng triệu độc giả trên thế giới đạt được những mục tiêu quan trọng trong đời chỉ bằng một cách đơn giản là thay đổi tư duy. Sức Mạnh Tiềm Thức giới thiệu và giải thích các phương pháp tập trung tâm thức nhằm xoá bỏ những rào cản tiềm thức đã ngăn chúng ta đạt được những điều mình mong muốn. ", unitPrice = 99000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_237646.jpg")
    # b68 = BookModel(name = "OSHO - Yêu - Being In Love" , desc = "Những người đói khát trong nhu cầu, những người luôn kỳ vọng ở tình yêu chính là những người đau khổ nhất. Hai kẻ đói khát tìm thấy nhau trong một mối quan hệ yêu đương cùng những kỳ vọng người kia sẽ mang đến cho mình thứ mình cần – về cơ bản sẽ nhanh chóng thất vọng về nhau và cùng mang đến ngục tù khổ đau cho nhau. Trong cuốn sách Yêu, Osho - bậc thầy tâm linh, người được tôn vinh là một trong 1000 người kiến tạo của thế kỷ 20 – đã đưa ra những kiến giải sâu sắc về nhu cầu tâm lý có sức mạnh lớn nhất của nhân loại và “chỉ cho chúng ta cách trải nghiệm tình yêu”. ", unitPrice = 120000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/b/e/beinglove.jpg")
    # b69 = BookModel(name = "Yêu Những Điều Không Hoàn Hảo" , desc = "“Ngẫm lại cuộc sống của chính mình, ta sẽ nhận thấy rất nhiều điều không hoàn hảo. Trước hết, chỉ nhìn vào bản thân mình thôi ta đã cảm nhận được nhiều thiếu sót rồi: lời nói và hành động mâu thuẫn với nhau, vụng về trong những mối quan hệ xã hội, chuyện học hành, công việc không suôn sẻ như ý muốn. Chưa kể đôi khi ta còn khiến người khác tổn thương, thậm chí còn làm những việc khiến bản thân cảm thấy tội lỗi và hối hận. Và khi nhìn vào những người thân trong gia đình, bạn bè, đồng nghiệp, ta cũng nhận thấy những điều không-hoàn-hảo tương tự như vậy.  ", unitPrice = 99000, category_id = 4, thumb="https://cdn0.fahasa.com/media/catalog/product/4/c/4ceb6ba3bd81614df8ff4c1411b11f59.jpg")
    # b70 = BookModel(name = "Ký Ức Theo Dòng Đời" , desc = "Anh đã làm một công việc chiêu hiền đãi sĩ cực kỳ nhạy cảm trong một thời buổi rất, rất khó khăn, khi kiến thức bị xem nhẹ và kẻ sĩ bị đẩy ra lề xã hội. Anh không chỉ giúp họ được ngồi lại, mà còn có thể ngồi chung với nhau, không phân biệt nguồn đào tạo, trong một tinh thần hòa hợp hiếm có. Từ đó, người trí thức được đánh giá lại và có thể đóng góp năng lực, phần nào, cho xã hội, một nền kinh tế đang chuyển mình. Nhưng với tính cách khiêm cung và hòa đồng, anh không thấy mình là Mạnh Thường Quân. Anh hòa mình vào các môn khách, trở thành một trong số đó, một cách hồn nhiên, chân tình, tự nhiên như một con cá trong đàn cá. ", unitPrice = 185000, category_id = 7, thumb="https://cdn0.fahasa.com/media/catalog/product/8/9/8934974150961.jpg")
    # b71 = BookModel(name = "Gã Nghiện Giày - Tự Truyện Của Nhà Sáng Lập Nike" , desc = "Một câu chuyện cuốn hút, và truyền cảm hứng.... 24 tuổi, lấy bằng MBA ở Đại học Stanford, trăn trở với những câu hỏi lớn của cuộc đời, băn khoăn không biết tiếp tục làm việc cho một tập đoàn lớn hay tạo dựng sư nghiệp riêng cho mình... 24 tuổi, năm 1962, Phil Knight quyết định rằng con đường khác thường mới là lựa chọn duy nhất dành cho ông... Rồi ông khoác ba lô đi đến Tokyo, Hongkong, Bangkok, Việt Nam, Calcutta, Kathmandu, Bombay, Cairo, Jerusalem, Rome, Florence, Milan, Venice, Paris,, Munich, Vienna, London, Hy Lạp... Để rồi khi về lại quê nhà ở bang Oregon, ông quyết định mở công ty nhập khẩu giày chạy từ Nhật. Ban đầu chỉ một đôi để thử, rồi vài chục đôi, bán tại tầng hầm của gia đình bố mẹ Phil. Đam mê, quyết tâm, dám chấp nhận thất bại, vượt qua nhiều chông gai từ chuyện thiếu vốn, đến chuyện cạnh tranh từ đối thủ nhập khẩu khác… Phil Knight đã đưa công ty nhập khẩu giày ra đời với 50 đô-la mư của bố phát triển đến doanh nghiệp có doanh số hơn 1 triệu đô-la chỉ 10 năm sau đó, năm 1972. ", unitPrice = 176000, category_id = 7, thumb="https://cdn0.fahasa.com/media/catalog/product/8/9/8934974150961.jpg")
    # b72 = BookModel(name = "Chấn Hưng Nhật Bản" , desc = "Chấn Hưng Nhật Bản .Nhật Bản là một trong ba nền kinh tế lớn nhất thế giới với nguồn vốn dồi dào, công nghệ tiên tiến, có kinh nghiệm quản lý hiện đại và hiệu quả. Là nước xuất khẩu vốn khổng lồ, với hơn 1 nghìn tỉ USD đầu tư trực tiếp ở nước ngoài nên Nhật Bản là đối tác kinh tế quan trọng với nhiều nước trên thế giới, trong đó có Việt Nam. Trên con đường đi lên trở thành một trong ba nền kinh tế lớn nhất thế giới, Nhật Bản đã phải trải qua hai cuộc tái thiết đất nước vô cùng quan trọng, diễn ra vào thời kỳ Phục hưng Minh Trị năm 1868 và diễn ra sau Chiến tranh thế giới thứ hai. Trong cả hai lần tự tái thiết này, Nhật Bản đã tạo ra một nỗ lực to lớn để du nhập, làm chủ, cải tiến, thay đổi công nghệ và bí quyết ngành công nghiệp của phương Tây. Và nhờ đó, Nhật Bản dường như trở nên bất bại trong lĩnh vực công nghiệp và công nghệ. ", unitPrice = 112000, category_id = 7, thumb="https://cdn0.fahasa.com/media/catalog/product/b/i/bia_chan-hung-nhat-ban.jpg")
    # b74 = BookModel(name = "Bùi Kiến Thành - Người Mở Khóa Lãng Du" , desc = "Bùi Kiến Thành là chuyên gia nổi  tiếng trong lĩnh vực kinh tế tài chính. Nhưng ít ai biết rằng, ông chính là cố vấn cho ba đời Thủ tướng: Võ Văn Kiệt, Phan Văn Khải, Nguyễn Tấn Dũng. Chính ông là tác giả của khẩu hiệu: “Dân giàu, nước mạnh…” trong thời kì đầu Đổi mới, là một trong số những người trực tiếp khai thông quan hệ Việt - Mỹ, góp phần giải quyết những vấn đề liên quan đến chủ quyền lãnh hải Việt Nam… ", unitPrice = 84000, category_id = 7, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_25903.jpg")
    # b75 = BookModel(name = "Trước Bình Minh Luôn Là Đêm Tối" , desc = "Trước bình minh luôn là đêm tối là hành trình của một chàng trai sắp 30 tuổi, với những thành tích đáng nể và tinh thần không ngừng nỗ lực khẳng định vị thế, tầm vóc của khởi nghiệp Việt trên toàn thế giới. ", unitPrice = 125000, category_id = 7, thumb="https://cdn0.fahasa.com/media/catalog/product/8/9/8935251407655.jpg")
    # b77 = BookModel(name = "Bí Mật Tư Duy Triệu Phú (Tái Bản 2021)" , desc = "Trong cuốn sách này T. Harv Eker sẽ tiết lộ những bí mật tại sao một số người lại đạt được những thành công vượt bậc, được số phận ban cho cuộc sống sung túc, giàu có, trong khi một số người khác phải chật vật, vất vả mới có một cuộc sống qua ngày. Bạn sẽ hiểu được nguồn gốc sự thật và những yếu tố quyết định thành công, thất bại để rồi áp dụng, thay đổi cách suy nghĩ, lên kế hoạch rồi tìm ra cách làm việc, đầu tư, sử dụng nguồn tài chính của bạn theo hướng hiệu quả nhất.", unitPrice = 79000, category_id = 2, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_188995_1_1.jpg")
    # b78 = BookModel(name = "Nhà Đầu Tư Thông Minh (Tái Bản 2020)" , desc = "Là nhà tư vấn đầu tư vĩ đại nhất của thế kỷ 20, Benjamin Graham đã giảng dạy và truyền cảm hứng cho nhiều người trên khắp thế giới. Triết lý “đầu tư theo giá trị“ của Graham, bảo vệ nhà đầu tư khỏi những sai lầm lớn và dạy anh ta phát triển các chiến lược dài hạn, đã khiến Nhà đầu tư thông minh trở thành cẩm nang của thị trường chứng khoán kể từ lần xuất bản đầu tiên vào năm 1949. ", unitPrice = 168000, category_id = 2, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_44030.jpg")
    # b80 = BookModel(name = "Giáo Dục Não Phải - Tương Lai Cho Con Bạn" , desc = "Người Việt Nam chúng ta thường tự hào rằng mình là một dân tộc thông minh. Thật khó để chứng minh theo lý thuyết thống kê và bằng các tiêu chí chặt chẽ, vững chắc rằng một dân tộc thông minh hơn những dân tộc khác. Nhưng dân tộc chúng ta không thiếu những cá nhân kiệt xuất, thiên tài để chống đỡ cho lý luận, cho niềm tự hào về một dân tộc thông minh. Để xây dựng một dân tộc thông minh, cần rất nhiều hơn là những cá nhân riêng biệt. Ở đó cần có ý thức hệ, hệ thống nhận thức vì giáo dục và cho giáo dục, nơi mà giá trị của giáo dục là cốt lõi của giá trị con người. Và giá trị con người phải dựa trên cốt lõi từ nền giáo dục. Chúng ta cần một sự chuyển dịch bền vững về tư duy giá trị giáo dục, hơn là chỉ những thay đổi... ", unitPrice = 74000, category_id = 5, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_223589.jpg")
    # b81 = BookModel(name = "Bí Ẩn Của Não Phải (Tái Bản 2019)" , desc = "Mỗi Đứa Trẻ Là Một Thiên Tài! Những Thành Tựu Của Phương Pháp Tiếp Cận Mới Nhất Trong Giáo Dục Đối với trẻ nhỏ việc giúp bé phát triển khả năng tư duy sáng tạo là điều rất quan trọng, vì vậy cha mẹ cần quan tâm giúp trẻ rèn luyện kích thích hoạt động của não phải để bồi dưỡng cho trẻ khả năng tư duy sáng tạo. Bởi lẽ việc phát triển não phải cho trẻ không phải chỉ phát triển về cảm xúc, về sự sáng tạo mà những kết quả đó sẽ giúp ích rất nhiều cho sự phát triển toàn não bộ. Khi được giáo dục đúng cách, não phải sẽ phát triển và tạo sự liên kết với não trái một cách tốt nhất. ", unitPrice = 83000, category_id = 5, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_3973.jpg")
    # b82 = BookModel(name = "Dạy Con Dùng Tiền (Tái Bản 2019)" , desc = "Adam Khoo và Keon Chee viết ra một quyển sách dựa trên kinh nghiệm của chính họ. Dạy Con Dùng Tiền đưa ra những hướng dẫn thực tế cho tất cả dạng cha mẹ - đã kết hôn, đã ly hôn, giàu, nghèo - về cách nuôi dạy những đứa trẻ có trách nhiệm tài chính trong một thời đại có quá nhiều tiền bạc. TIỀN TIÊU VẶT + THU NHẬP KHÁC = TIẾT KIỆM + TIÊU XÀI + CHIA SẺ ", unitPrice = 63000, category_id = 5, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_4953.jpg")
    # b83 = BookModel(name = "Dạy Con Tư Duy" , desc = "Cuốn sách giúp cha mẹ khám phá sức mạnh của não bộ, hướng dẫn con phát triển năng lực bản thân và khám phá nhà vô địch trong mọi đứa trẻ. “Quyển sách này mang đến người đọc phương tiện để thay đổi bản thân và phong cách nuôi dạy trẻ của mình. Nó hướng dẫn chúng ta tiếp thu tư duy nhà vô địch và giúp ta có khả năng “khám phá nhà vô địch” trong mọi đứa trẻ”, Giáo sư Allan Snyder, Viện sĩ Hội Hoàng gia Anh quốc, Nhà sáng lập kiêm Giám đốc chương trình Centre for the Mind nhận xét về tác phẩm DạyCon Tư Duy như vậy. ", unitPrice = 73000, category_id = 5, thumb="https://cdn0.fahasa.com/media/catalog/product/d/a/daycontuduy.jpg")
    # b84 = BookModel(name = "Chuyện Con Mèo Dạy Hải Âu Bay (Tái Bản 2019)" , desc = "Cô hải âu Kengah bị nhấn chìm trong váng dầu – thứ chất thải nguy hiểm mà những con người xấu xa bí mật đổ ra đại dương. Với nỗ lực đầy tuyệt vọng, cô bay vào bến cảng Hamburg và rơi xuống ban công của con mèo mun, to đùng, mập ú Zorba. Trong phút cuối cuộc đời, cô sinh ra một quả trứng và con mèo mun hứa với cô sẽ thực hiện ba lời hứa chừng như không tưởng với loài mèo: Không ăn quả trứng. Chăm sóc cho tới khi nó nở. Dạy cho con hải âu bay. ", unitPrice = 41000, category_id = 6, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_188285.jpg")
    # b85 = BookModel(name = "Dế Mèn Phiêu Lưu Ký - Tái Bản 2020" , desc = " “Một con dế đã từ tay ông thả ra chu du thế giới tìm những điều tốt đẹp cho loài người. Và con dế ấy đã mang tên tuổi ông đi cùng trên những chặng đường phiêu lưu đến với cộng đồng những con vật trong văn học thế giới, đến với những xứ sở thiên nhiên và văn hóa của các quốc gia khác. Dế Mèn Tô Hoài đã lại sinh ra Tô Hoài Dế Mèn, một nhà văn trẻ mãi không già trong văn chương...” - Nhà phê bình Phạm Xuân Nguyên ", unitPrice = 42000, category_id = 6, thumb="https://cdn0.fahasa.com/media/catalog/product/d/e/de-men-50k_1.jpg")
    # b86 = BookModel(name = "Bubu Và Titi - Hành Trình Học Hỏi Từ Thử Thách" , desc = "“Bubu và Titi” kể về các chuyến phiêu lưu thú vị của cậu bé Bubu và cá heo Titi. Mở đầu câu chuyện, Bubu đang vừa thơ thẩn đi dọc bãi biển Vịnh Hải Dương vừa ngắm nhìn ánh mặt trời đang dần ngả vàng ở phía tây, thì chợt cậu phát hiện có cái gì đó vùng vẫy trên bãi cát – A! Đó là chú heo với chiếc vây đuôi bị khuyết một mảnh Titi, chú đang bị mắc vào tấm lưới đánh cá. Bubu giúp Titi thoát khỏi tấm lưới; đó là khởi đầu của một tình bạn trong trẻo và các chuyến phiêu lưu thú vị. ", unitPrice = 74000, category_id = 6, thumb="https://cdn0.fahasa.com/media/catalog/product/9/7/9786043751741.jpg")
    # b87 = BookModel(name = "Tập Tô Chữ Mẫu Giáo - Tủ Sách Bé Vào Lớp 1" , desc = "Bộ sách Chuẩn bị cho bé vào lớp 1 sẽ giúp cha mẹ giải tỏa những lo lắng, băn khoăn đó. Nội dung sách gần gũi với chương trình sách giáo khoa chuẩn, bao gồm:  giúp bé luyện tay theo các nét cơ bản đầu tiên; như móc, sổ, ngang, sọc, xước, vòng, giúp bé làm quen với bảng chữ cái gồm 29 chữ theo cách viết thường và viết hoa;  ngoài ra, bé còn được làm quen với các con số và những phép tính đơn giản v.v… ", unitPrice = 55000, category_id = 8, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_29257.jpg")
    # b88 = BookModel(name = "Tiếng Anh 6 - Friends Plus - Student Book" , desc = " Sách Tiếng Anh 6 Friends Plus – Student Book bám sát các chủ đề, chủ điểm kiến thức ngôn ngữ trong chương trình; cung cấp cho học sinh các kĩ năng cần thiết để tự tin giao tiếp bằng tiếng Anh; đáp ứng nhu cầu đánh giá quá trình học tập của học sinh theo định hướng phát triển năng lực. ", unitPrice = 86000, category_id = 8, thumb="https://cdn0.fahasa.com/media/catalog/product/9/7/9786040288271.jpg")
    # b89 = BookModel(name = "Bài Tập Tiếng Anh Lớp 8 - Không Đáp Án (2020)" , desc = "Bài Tập Tiếng Anh 8 là tập hợp các bài tập thực hành về từ vựng (vocabulary), ngữ pháp (grammar), đàm thoại (conversation) và đọc hiểu (reading comprehension), nhằm giúp học sinh luyện tập các nội dung trọng tâm của bài học. Các bài tập được biên soạn theo từng đơn vị bài học (Unit), gồm hai phần A và B có nội dung tương ứng với các phần bài học trong sách giáo khoa. Sau phần bài tập của mỗi đơn vị bài học có một bài kiểm tra (Test For Unit), sau 4 đơn vị bài học có bài tự kiểm tra (Test Yourself) được soạn như bài kiểm tra một tiết và sau Unit 8 và Unit 16 có hai bài kiểm tra học kì nhằm giúp các em ôn luyện và củng cố kiến thức đã học. ", unitPrice = 26000, category_id = 8, thumb="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_50093.jpg")
    # b90 = BookModel(name = "30 Chủ Đề Từ Vựng Tiếng Anh (Tập 1)" , desc = "Ngữ pháp và từ vựng là hai mảng không thể thiếu trong quá trình học ngoại ngữ nói chung và học tiếng Anh nói riêng. Hai phạm trù này sẽ góp phần giúp chúng ta đạt được sự thành thạo về ngôn ngữ. Nếu như ngữ pháp có các quy tắc, có cấu trúc để tuân theo thì từ vựng lại không có bất cứ quy tắc nào. Do đó, đa số người học đều thấy rất khó để học và nhớ được từ vựng. Đó là còn chưa kể tới có rất nhiều từ có nghĩa giống nhau nhưng lại được sử dụng trong các ngữ cảnh khác nhau và một từ thì lại có rất nhiều nghĩa. ", unitPrice = 110000, category_id = 9, thumb="https://cdn0.fahasa.com/media/catalog/product/h/h/hh-30-chu-de-tu-vung-tieng-anh_1.jpg")
    # b91 = BookModel(name = "Giải Thích Ngữ Pháp Tiếng Anh (Tái Bản 2022)" , desc = "Sách 2 ", unitPrice = 139000, category_id = 9, thumb="https://cdn0.fahasa.com/media/catalog/product/z/3/z3097453775918_7ea22457f168a4de92d0ba8178a2257b.jpg")
    # b92 = BookModel(name = "30 Chủ Đề Từ Vựng Tiếng Anh (Tập 2)" , desc = "Ngữ pháp và từ vựng là hai mảng không thể thiếu trong quá trình học ngoại ngữ nói chung và học tiếng Anh nói riêng. Hai phạm trù này sẽ góp phần giúp chúng ta đạt được sự thành thạo về ngôn ngữ. Nếu như ngữ pháp có các quy tắc, có cấu trúc để tuân theo thì từ vựng lại không có bất cứ quy tắc nào. Do đó, đa số người học đều thấy rất khó để học và nhớ được từ vựng. Đó là còn chưa kể tới có rất nhiều từ có nghĩa giống nhau nhưng lại được sử dụng trong các ngữ cảnh khác nhau và một từ thì lại có rất nhiều nghĩa. ", unitPrice = 161000, category_id = 9, thumb="https://cdn0.fahasa.com/media/catalog/product/h/h/hh-30-chu-de-tu-vung-tieng-anh-2_1.jpg")

    # db.session.add(b2)
    # db.session.add(b3)
    # db.session.add(b4)
    # db.session.add(b5)
    # db.session.add(b6)
    # db.session.add(b7)
    # db.session.add(b8)
    # db.session.add(b9)
    # db.session.add(b10)
    # db.session.add(b11)
    # db.session.add(b12)
    # db.session.add(b13)
    # db.session.add(b14)
    # db.session.add(b15)
    # db.session.add(b16)
    # db.session.add(b17)
    # db.session.add(b18)
    # db.session.add(b19)
    # db.session.add(b20)
    # db.session.add(b21)
    # db.session.add(b22)
    # db.session.add(b23)
    # db.session.add(b24)
    # db.session.add(b25)
    # db.session.add(b26)
    # db.session.add(b27)
    # db.session.add(b28)
    # db.session.add(b29)
    # db.session.add(b30)
    # db.session.add(b31)
    # db.session.add(b32)
    # db.session.add(b33)
    # db.session.add(b34)
    # db.session.add(b35)
    # db.session.add(b36)
    # db.session.add(b37)
    # db.session.add(b38)
    # db.session.add(b39)
    # db.session.add(b40)
    # db.session.add(b41)
    # db.session.add(b42)
    # db.session.add(b43)
    # db.session.add(b44)
    # db.session.add(b45)
    # db.session.add(b46)
    # db.session.add(b47)
    # db.session.add(b48)
    # db.session.add(b49)
    # db.session.add(b50)
    # db.session.add(b51)
    # db.session.add(b52)
    # db.session.add(b53)
    # db.session.add(b54)
    # db.session.add(b55)
    # db.session.add(b56)
    # db.session.add(b57)
    # db.session.add(b58)
    # db.session.add(b59)
    # db.session.add(b60)
    # db.session.add(b61)
    # db.session.add(b62)
    # db.session.add(b63)
    # db.session.add(b64)
    # db.session.add(b65)
    # db.session.add(b66)
    # db.session.add(b67)
    # db.session.add(b68)
    # db.session.add(b69)
    # db.session.add(b70)
    # db.session.add(b71)
    # db.session.add(b72)
    # db.session.add(b74)
    # db.session.add(b75)
    # db.session.add(b77)
    # db.session.add(b78)
    # db.session.add(b80)
    # db.session.add(b81)
    # db.session.add(b82)
    # db.session.add(b83)
    # db.session.add(b84)
    # db.session.add(b85)
    # db.session.add(b86)
    # db.session.add(b87)
    # db.session.add(b88)
    # db.session.add(b89)
    # db.session.add(b90)
    # db.session.add(b91)
    # db.session.add(b92)
    # db.session.commit()


    




