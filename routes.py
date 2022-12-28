from flask import render_template, url_for, flash, redirect, request, abort, session
from nxthen import app, db, bcrypt, photos
from nxthen.Forms import RegistrationForm, LoginForm, ReviewForm, UpdateAccount, ContactUsForm, BookingForm, ReportForm
from nxthen.models import User, Reviews, Messages, Booking, Report
from flask_login import login_user, current_user, logout_user, login_required

from nxthen.products.forms import Addproducts, UpdateProduct, CheckoutForm
from nxthen.products.models import AddProduct, AddSales
from werkzeug.utils import secure_filename
import datetime
import random
import string

import os
import secrets
from PIL import Image

#BOOKINGS PAGE
@app.route('/createBooking', methods=['GET', 'POST'])
def create_booking():
    form = BookingForm(request.form)
    if request.method == "POST" and form.submit():
        try:
            booking = Booking(first_name=form.first_name.data,
                             last_name=form.last_name.data,
                             email=form.email.data,
                             date=form.date.data,
                              time=form.time.data)
            db.session.add(booking)
            db.session.commit()
            flash(f'Your session has been successfully booked!', 'success')
            print("a new booking has been created")
            return redirect(url_for('home'))
        except:
            print("error booking")
    return render_template('createBooking.html', form=form)

@app.route('/retrieveBooking')
@login_required
def retrieve_booking():
    bookings = Booking.query.order_by(Booking.booking_id)
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    print("Bookings retrieved - admin side")
    return render_template('retrieveBookings.html', bookings=bookings, reports=reports,total_reports=total_reports)

@app.route('/deleteBookingAdmin/<int:id>', methods=['POST'])
def delete_booking_admin(id):
    booking_to_delete_admin = Booking.query.get_or_404(id)
    try:
        db.session.delete(booking_to_delete_admin)
        db.session.commit()
        flash(f'Booking has been successfully deleted!')
        print("a booking has been deleted - admin")
        return redirect(url_for('retrieve_booking'))
    except:
        print("error deleting booking - admin")
        return redirect(url_for('retrieve_booking'))
    booking = Booking.query.order_by(Booking.booking_id)
    return render_template('retrieveBooking.html', booking=booking)





#CONTACT US PAGE
@app.route('/contactUs')
def contact_us():
    messages = Messages.query.order_by(Messages.message_id)
    print("contact us page retrieved - user side")
    return render_template('contactUs.html', messages=messages)

@app.route('/createMessage', methods=['POST', 'GET'])
def create_message():
    form = ContactUsForm(request.form)
    if request.method == "POST" and form.submit():
        try:
            message = Messages(first_name=form.first_name.data,
                             last_name=form.last_name.data,
                             email=form.email.data,
                             issue=form.issue.data,)
            db.session.add(message)
            db.session.commit()
            flash(f'Your form has been successfully submitted!')
            print("a new message has been sent")
            return redirect(url_for('contact_us'))
        except:
            print("error creating message")
        finally:
            db.session.close()
    return render_template('createMessage.html', form=form)

@app.route('/retrieveContactUs')
def retrieve_messages():
    messages = Messages.query.order_by(Messages.message_id)
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    print("contact us page retrieved - admin side")
    return render_template('retrieveContactUs.html', messages=messages, total_reports=total_reports, reports=reports)

@app.route('/deleteMessageAdmin/<int:id>', methods=['POST'])
def delete_message_admin(id):
    message_to_delete_admin = Messages.query.get_or_404(id)
    try:
        db.session.delete(message_to_delete_admin)
        db.session.commit()
        flash(f"Customer's issue has been successfully resolved!")
        print("a message has been deleted - admin")
        return redirect(url_for('retrieve_messages'))
    except:
        print("error deleting message - admin")
        return redirect(url_for('retrieve_messages'))
    messages = Messages.query.order_by(Messages.date_posted)
    return render_template('retrieveContactUs.html', messages=messages)


# ACCOUNT MANAGEMENT
@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if request.method == 'POST' and register_form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(first_name=register_form.first_name.data,last_name=register_form.last_name.data,email=register_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', register_form=register_form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form= LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            if user.is_admin:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', login_form=login_form)

@app.route("/forgetPassword",methods=["POST","GET"])
def forget_password():
    login_form=LoginForm()
    if request.method=="POST":
        flash("Password reset link has been sent to your email! Please check your inbox")
        return redirect(url_for('home'))
    return render_template('forgetPassword.html',login_form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have successfully been logged out!','success')
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form= UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.email = form.email.data
        current_user.first_name=form.first_name.data
        current_user.last_name=form.last_name.data
        current_user.password=hashed_password
        db.session.commit()
        flash('Account successfully updated', 'success')
        return redirect((url_for('account')))
    elif request.method == 'GET':
        form.first_name.data=current_user.first_name
        form.last_name.data=current_user.last_name
        form.email.data=current_user.email
        form.picture.data=current_user.image_file

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Edit', image_file=image_file, form=form)


@app.route("/account/<int:id>/delete",methods=['POST','GET'])
@login_required
def delete_account(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        logout()
        flash('Account successfully deleted!', 'success')
    except:
        flash('Error in deleting account')
    return redirect(url_for('home'))

@app.route("/retrieveUsers/<int:id>/delete",methods=['POST','GET'])
@login_required
def delete_account_admin(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Account successfully deleted!', 'success')
        return redirect((url_for('retrieve_users')))
    except:
        flash('Error in deleting account')
        return redirect((url_for('retrieve_users')))
    users = User.query.order_by(User.id)
    return render_template('retrieveUsers.html', users=users)

@app.route("/adminaccount", methods=['POST','GET'])
@login_required
def adminaccount():
    form= UpdateAccount()
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password=hashed_password
        db.session.commit()
        flash('Account successfully updated', 'success')
        return redirect((url_for('adminaccount')))
    return render_template('adminAccount.html', title='Edit', form=form, reports=reports, total_reports=total_reports )

@app.route('/retrieveUsers')
def retrieve_users():
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    users = User.query.order_by(User.id)
    print("Users retrieved - admin side")
    return render_template('retrieveUsers.html', users=users, reports=reports, total_reports=total_reports)

@app.route('/addAdmin',methods=['POST','GET'])
@login_required
def add_admin():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=hashed_password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        flash('Admin account has been created! You are now able to log in ', 'success')
        return redirect(url_for('dashboard'))

    return render_template('index.html', title='Register', form=form)

# REVIEW PAGE

@app.route('/reviewPage')
def review_page():
    reviews = Reviews.query.order_by(Reviews.date_posted)
    print("review page retrieved - user side")
    return render_template('reviewPage.html', reviews=reviews)

@app.route('/createReview', methods=['GET', 'POST'])
@login_required
def create_review():
    form = ReviewForm(request.form)
    if request.method == "POST" and form.submit():
        try:
            review = Reviews(first_name=current_user.first_name,
                             last_name=current_user.last_name,
                             email=current_user.email,
                             product_service=form.product_service.data,
                             review_text=form.review_text.data,author=current_user)
            db.session.add(review)
            db.session.commit()
            flash(f'Your review has been successfully submitted!', 'success')
            print("a new review has been created")
            return redirect(url_for('review_page'))
        except:
            print("error creating review")
    return render_template('createReview.html', form=form)

@app.route('/retrieveReviews')
def retrieve_reviews():
    reviews = Reviews.query.order_by(Reviews.date_posted)
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    print("review page retrieved - admin side")
    return render_template('retrieveReview.html', reviews=reviews, total_reports=total_reports, reports=reports)

@app.route('/deleteReviewAdmin/<int:id>', methods=['POST'])
def delete_review_admin(id):
    review_to_delete_admin = Reviews.query.get_or_404(id)
    try:
        db.session.delete(review_to_delete_admin)
        db.session.commit()
        flash(f'Review has been successfully deleted!')
        print("a review has been deleted - admin")
        return redirect(url_for('retrieve_reviews'))
    except:
        print("error deleting review - admin")
        return redirect(url_for('retrieve_reviews'))
    reviews = Reviews.query.order_by(Reviews.date_posted)
    return render_template('retrieveReviews.html', reviews=reviews)

@app.route('/deleteReviewUser/<int:id>', methods=['POST'])
def delete_review_user(id):
    review_to_delete_user = Reviews.query.get_or_404(id)
    if review_to_delete_user.author != current_user:
        abort(403)
    try:
        db.session.delete(review_to_delete_user)
        db.session.commit()
        flash(f'Your review has been successfully deleted!')
        print("a review has been deleted - user")
        return redirect(url_for('review_page'))
    except:
        print("error deleting review - user")
        return redirect(url_for('review_page'))
    reviews = Reviews.query.order_by(Reviews.date_posted)
    return render_template('reviewPage.html', reviews=reviews)

@app.route('/updateReview/<int:id>', methods=['POST','GET'])
def update_review(id):
    review = Reviews.query.get_or_404(id)
    if review.author != current_user:
        abort(403)
    update_form = ReviewForm()
    if request.method == "POST" and update_form.submit():
        review.first_name = update_form.first_name.data
        review.last_name = update_form.last_name.data
        review.email = update_form.email.data
        review.product_service = update_form.product_service.data
        review.review_text = update_form.review_text.data
        try:
            db.session.add(review)
            db.session.commit()
            flash(f'Your review has been successfully updated!')
            print("a review has been updated")
            return redirect(url_for('review_page', id=review.review_id))
        except:
            print("error updating review")
            return redirect(url_for('review_page', id=review.review_id))
    update_form.first_name.data = review.first_name
    update_form.last_name.data = review.last_name
    update_form.email.data = review.email
    update_form.product_service.data = review.product_service
    update_form.review_text.data = review.review_text
    return render_template('editReview.html', update_form=update_form)


@app.route('/retrieveBooking&Review')
@login_required
def retrieve_booking_review_user():
    bookings = Booking.query.order_by(Booking.booking_id)
    reviews = Reviews.query.order_by(Reviews.date_posted)
    print("Booking and reviews retrieved - user side")
    return render_template('retrieveBooking&Review.html', bookings=bookings, reviews=reviews)

#STORE
def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.route('/')
def home():
    products = AddProduct.query.filter(AddProduct.stock > 0)
    return render_template('home.html', products=products)


@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    form = Addproducts(request.form)
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    if request.method == "POST":
        try:
            image_file=photos.save(request.files.get('image_file'), name=secrets.token_hex(10)+ '.')
            addpro = AddProduct(name=form.name.data,
                             price=form.price.data,
                             discount=form.discount.data,
                             stock=form.stock.data,
                             desc=form.description.data,
                            image_file=image_file)
            db.session.add(addpro)
            db.session.commit()
            flash(f'The product {form.name.data} has been added to your database', 'success')
            print("a new review has been created")
            return redirect(url_for('addproduct'))
        except:
            print("Error creating product")
    return render_template('addproduct.html', form=form, total_reports=total_reports, reports=reports)

@app.route('/retrieveProducts')
def retrieve_products():
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    form = UpdateProduct()
    products = AddProduct.query.order_by(AddProduct.id)
    print("Inventory page retrieved - admin side")
    return render_template('retrieveProducts.html', products=products, form=form, reports=reports, total_reports=total_reports)

@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    product_to_delete = AddProduct.query.get_or_404(id)
    try:
        db.session.delete(product_to_delete)
        db.session.commit()
        flash(f'Item has been successfully deleted!', 'success')
        print("an item has been deleted")
        return redirect(url_for('retrieve_products'))
    except:
        flash(f'Error deleting item, please try again!', 'danger')
        print("error deleting item")
        return redirect(url_for('retrieve_products'))
    products = AddProduct.query.order_by(AddProduct.id)
    return render_template('retrieveProducts.html', products=products)



@app.route('/updateProduct/<int:id>', methods=['POST','GET'])
def update_product(id):
    product = AddProduct.query.get_or_404(id)
    form = UpdateProduct()
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.discount = form.discount.data
        product.desc = form.description.data
        try:
            db.session.commit()
            flash(f'Your product has been successfully updated!')
            print("a product has been updated")
            return redirect(url_for('retrieve_products',id=AddProduct.id))
        except:
            print("error updating product")
            return redirect(url_for('retrieve_products',id=AddProduct.id))
    form.name.data = product.name
    form.price.data = product.price
    form.stock.data = product.stock
    form.discount.data = product.discount
    form.description.data = product.desc
    return render_template('editProduct.html', form=form)




@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))
        product = AddProduct.query.filter_by(id=product_id).first()

        if request.method == "POST":
            DictItems = {product_id: {'name': product.name, 'price': product.price, 'discount': product.discount, 'quantity': quantity, 'stock':product.stock}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            item['quantity'] += 1
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    rawtotal=0
    totaldiscount=0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        totaldiscount+=discount
        subtotal += (float(product['price']) * int(product['quantity']))
        rawtotal += subtotal
        subtotal -= discount
        grandtotal += subtotal

    return render_template('cart.html', grandtotal=grandtotal, rawtotal=rawtotal, totaldiscount=totaldiscount)


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                flash('Item has been deleted!', 'success')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    self = request.form.get('quantity')
                    if self == item['quantity']:
                        item['quantity'] = quantity
                        flash('Quantity has not changed', 'danger')
                    else:
                        item['quantity'] = quantity
                        flash('Item is updated!', 'success')
                    return redirect(url_for('getCart'))

        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))


@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)

#ADMIN SIDE

@app.route('/dashboard')
@login_required
def dashboard():
    total_reports = db.session.query(Report).count()
    form=ReportForm()
    reports = Report.query.order_by(Report.report_id)
    if not current_user.is_admin:
        abort(403)
    return render_template('index.html',form=form,total_reports=total_reports,reports=reports)


# CHECKOUT PAGE
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/paymentPage', methods=['POST','GET'])
def payment_page():
    form=CheckoutForm()
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    rawtotal=0
    totaldiscount=0
    number_of_items=0
    names=''
    quantities=''
    for key, product in session['Shoppingcart'].items():
        discount = float(product['discount']/100) * float(product['price'])
        number_of_items+= int(product['quantity'])
        totaldiscount+=discount
        subtotal += (float(product['price']) * int(product['quantity']))

        if len(session['Shoppingcart'])>1:
            names+=product['name']+','
            quantities+=str(product['quantity'])+','
        else:
            names+=product['name']
            quantities+=str(product['quantity'])
        rawtotal += subtotal
        subtotal -= discount
        grandtotal += subtotal
    if request.method == "POST":
        receipt=id_generator()
        addsale=AddSales(product_name=names,quantities=quantities,receipt=receipt,quantity=number_of_items,total=subtotal)
        db.session.add(addsale)
        db.session.commit()
        clearcart()
        return redirect(url_for('order_placed'))
    else:
        print("error")
    return render_template('paymentPage.html',grandtotal=grandtotal, rawtotal=rawtotal, totaldiscount=totaldiscount,form=form)


@app.route('/orderPlaced')
def order_placed():
    print("order placed page retrieved - user side")
    return render_template('orderPlaced.html')

@app.route('/saleshistory')
@login_required
def sales_history():
    total_reports = db.session.query(Report).count()
    reports = Report.query.order_by(Report.report_id)
    products = AddSales.query.order_by(AddSales.id)
    print("Sales history page retrieved - admin side")
    return render_template('retrieveSales.html',products=products, reports=reports, total_reports=total_reports)

@app.route('/createReport',methods=['POST','GET'])
def create_report():
    form = ReportForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        try:
            report = Report(first_name=current_user.first_name,
                             title=form.title.data,
                             report_text=form.report_text.data)
            db.session.add(report)
            db.session.commit()
            flash(f'Your product has been successfully submitted!', 'success')
            print("a new report has been created")
            return redirect(url_for('dashboard'))
        except:
            print("error creating report")
    return render_template('index.html', form=form)



#CHATBOT
from nxthen.chatbot import chatbot

app.static_folder = 'static'

@app.route("/bot")
def bot():
    return render_template('bot.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

