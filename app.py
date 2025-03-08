from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField
from wtforms.validators import InputRequired, Email, Length, NumberRange, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Iwilldothis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/OneDrive/Documents/Library_Management_System/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    phn = db.Column(db.Integer,  unique=True)
    username = db.Column(db.String(15) , unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Books(UserMixin, db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    title = db.Column(db.String(15))
    author = db.Column(db.String(15))
    genre = db.Column(db.String(50))
    rating = db.Column(db.Float)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class FilterForm(FlaskForm):
    page = IntegerField('Page Number', validators=[InputRequired(), NumberRange(min=1)])
    limit = IntegerField('Items per Page', validators=[InputRequired(), NumberRange(min=1)], render_kw={"id":"limit"})
    genre = StringField('Filter by Genre', validators=[Optional()], render_kw={"id":"genre"})
    rating = FloatField('Filter by Rating', validators=[Optional(), NumberRange(min=1,max=5)], render_kw={"id":"rating"})

class ForgotForm(FlaskForm):
    email = StringField('Email' , validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    phn = IntegerField('Phone Number', validators=[InputRequired(), NumberRange(min=1000000000, max=9999999999, message='Phone number must be of 10 digits')])
    password = StringField('Password', validators = [InputRequired(), Length(min=8, max=80)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [Length(min=4, max=15)])
    password = StringField('Password', validators = [Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    forgot_password = BooleanField('Forgot your password? Click Here')

class RegisterForm(FlaskForm):
    email = StringField('Email' , validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    username = StringField('Username', validators = [InputRequired(), Length(min=4, max=15)])
    password = StringField('Password', validators = [InputRequired(), Length(min=8, max=80)])
    phn = IntegerField('Phone Number', validators=[InputRequired(), NumberRange(min=1000000000, max=9999999999, message='Phone number must be of 10 digits')])
    admin = BooleanField('Want to be an admin? Click here')

class BooksForm(FlaskForm):
    title = StringField('Title' , validators=[InputRequired(), Length(max=50)])
    author = StringField('Author', validators = [InputRequired()])
    genre = StringField('Genre', validators = [InputRequired()])
    rating = FloatField('Rating', validators=[Optional(), NumberRange(min=1, max=5, message='Rating must be between 1-5')])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login' , methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.forgot_password.data == True:
        form.username.validators = [Optional()]
        form.password.validators = [Optional()]
    else:
        form.username.validators = [InputRequired()]
        form.password.validators = [InputRequired()]
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if form.forgot_password.data == True:
            return redirect(url_for('forgot'))
        elif user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember = form.remember.data)
                return redirect(url_for("dashboard"))
    return render_template('login.html' , form=form)

@app.route('/forgot', methods=['GET','POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phn = form.phn.data).first()
        print(user.email)
        print(form.email.data)
        if user.email == form.email.data:
            if any(c.islower() for c in form.password.data) and any(c.isupper() for c in form.password.data) and any(c.isdigit() for c in form.password.data) and not form.password.data.isalnum():
                new_hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
                user = User.query.filter_by(phn = user.phn).first()
                user.password = new_hashed_password        
                db.session.commit()
                flash (f"Please login again!","info")
                return redirect(url_for('login')) 
            else:
                flash (f"Password does not meet the required criteria!")
                return redirect(url_for('forgot'))
        else:
            flash(f"Wrong Email entered!")
            return redirect(url_for('forgot'))
    return render_template('forgot.html', form=form) 

@app.route('/browse/<int:book_id>')
@login_required
def get_book_id(book_id):
    book = Books.query.get(book_id)
    return render_template('get_book_id.html', title=book.title, author=book.author, genre=book.genre, rating=book.rating, id = book_id)

@app.route('/browse', methods=['GET','POST'] )
@login_required
def browse():
    form = FilterForm()
    books = []
    total_pages = 0
    current_page = 1
    if  form.validate_on_submit:
        page = form.page.data
        limit = form.limit.data
        genre = form.genre.data
        rating = form.rating.data

        if genre != "" and rating is not(None):
            books_query = Books.query.filter(Books.rating>=rating, Books.genre==genre)
        elif genre != "":
            books_query = Books.query.filter_by(genre = genre)
        elif rating is not(None):
            books_query = Books.query.filter(Books.rating>=rating)
        else:
            books_query = Books.query

        books_query = books_query.paginate(page=page, per_page=limit, error_out=False)
        return render_template('browse.html', form=form, books_query=books_query, limit = limit)


    return render_template('browse.html', form=form, books_query=books_query, limit = limit)

@app.route('/books', methods=['GET','POST'] )
@login_required
def books():
    form = BooksForm()
    if form.validate_on_submit():
        new_user = Books(title = form.title.data, author = form.author.data, genre = form.genre.data, rating = form.rating.data )
        db.session.add(new_user)
        db.session.commit()
        flash("New book has been added!")
        return redirect(url_for('dashboard'))
    return render_template('books.html' , form=form)

@app.route('/signup' , methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if any(c.islower() for c in form.password.data) and any(c.isupper() for c in form.password.data) and any(c.isdigit() for c in form.password.data) and not form.password.data.isalnum():
            hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
            print(form.admin.data)
            new_user = User(username = form.username.data, email = form.email.data, phn = form.phn.data, password = hashed_password, admin = form.admin.data)
            db.session.add(new_user)
            db.session.commit()
            flash("New user has been created!")
            login_user(new_user)
            return redirect(url_for("dashboard"))
        else:
            flash (f"Password does not meet the required criteria!")
            return redirect(url_for('signup'))
    return render_template('signup.html' , form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html' , name= current_user.username, admin= current_user.admin)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)