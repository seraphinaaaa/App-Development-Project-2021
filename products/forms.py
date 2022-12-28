from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, TextAreaField, validators, SubmitField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class Addproducts(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    discount = IntegerField('Discount %', default=0)
    description = TextAreaField('Description', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    image_file = FileField('Upload Picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField('Submit')

class UpdateProduct(Addproducts):
    edit_submit = SubmitField('Edit Product')


class CheckoutForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    zip = StringField('Zip Code', validators=[DataRequired()])
    card_name= StringField('Card Name', validators=[DataRequired()])
    card_number= StringField('Card number', validators=[DataRequired()])
    card_cvv=IntegerField(validators=[DataRequired()])
    month=StringField('Exp Month',validators=[DataRequired()])
    year=StringField('Exp Year',validators=[DataRequired()])
    submit = SubmitField('Checkout')

