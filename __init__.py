import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
# from flask_uploads import configure_uploads, IMAGES, UploadSet

basedir= os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_BINDS'] ={'two': 'sqlite:///store.db',
                                'three':'sqlite:///review.db',
                                 'four':'sqlite:///message.db',
                                 'five':'sqlite:///bookings.db',
                                 'six':'sqlite:///sales.db',
                                 'seven':'sqlite:///report.db'
                                 }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')
# photos= UploadSet('photos', IMAGES)
# configure_uploads(app,(photos))

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from nxthen import routes


