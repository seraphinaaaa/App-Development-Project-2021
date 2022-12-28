from nxthen import db
from datetime import datetime


class AddProduct(db.Model):
    __bind_key__= 'two'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2),nullable=False)
    discount = db.Column(db.Integer, default=0)
    desc = db.Column(db.Text, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')



    def __repr__(self):
        return '<Addproduct %r>' % self.name

class AddSales(db.Model):
    __bind_key__= 'six'
    id = db.Column(db.Integer, primary_key=True)
    product_name=db.Column(db.String(80), nullable=False)
    receipt=db.Column(db.String(80), nullable=False)
    quantities = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.String(80), nullable=False)
    sales_date=db.Column(db.DateTime,default=datetime.now)
    total= db.Column(db.Integer, default=0)

db.create_all(bind="two")
db.create_all(bind="six")


