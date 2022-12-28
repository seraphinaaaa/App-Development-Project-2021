from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField, EmailField,validators, TextAreaField, SelectField, RadioField, DateField, IntegerField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from nxthen.models import User
from wtforms.widgets import TextArea

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, message='Password should be at least %(min)d characters long')])
    confirm = PasswordField('Confirm Password',validators=[DataRequired(message='*Required'), EqualTo('password',message="Passwords must match!")])
    reg_submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login_submit = SubmitField('Login')


class UpdateAccount(RegistrationForm):
    edit_submit = SubmitField('Edit Account')
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png','jpeg'])])

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

# for review page
class ReviewForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    product_service = StringField("Product Service", validators=[DataRequired()])
    review_text = StringField("Review Text", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")

#for contact us page
class ContactUsForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    issue = StringField("Describe your issue", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")


# for booking page
class BookingForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    date = DateField('Date', validators=[DataRequired()])
    time = SelectField('Time', choices=[('1pm'), ('2pm'), ('3pm'), ('4pm'), ('5pm')], validators=[DataRequired()])
    submit = SubmitField("Submit")

#report modal
class ReportForm(FlaskForm):
    title= StringField("Title", validators=[DataRequired()])
    report_text=StringField("Report Text", validators=[DataRequired()], widget=TextArea())