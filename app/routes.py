from flask import render_template, flash, redirect, url_for
from . import db
from .forms import LoginForm
from .forms import RegistrationForm
from .models import User, ActivityPost, Forum
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from flask import current_app as app
from . import login_manager

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Homepage')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # look at first result first()
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # return to page before user got asked to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/createPost',methods=['GET', 'POST'])
def createPost():
    if request.method == 'POST':
        createPost = ActivityPost(name=request.form['name'], activityTitle=request.form['activityTitle'], activityType=request.form['activityType'], activityDescription=request.form['activityDescription'])
        db.session.add(createPost)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('createPost.html')


@app.route('/viewlist')
def viewlist():
    viewMyPosts = db.session.query(ActivityPost).all()
    return render_template('viewlist.html', viewMyPosts=viewMyPosts)

@app.route('/viewcalender')
def viewcalender():
    return render_template('viewcalender.html')

@app.route('/forum')
def showBooks():
    forums = db.session.query(Forum).all()
    return render_template('forum.html', forums=forums)

@app.route('/newforumpost', methods=['GET', 'POST'])
def newPost():
    if request.method == 'POST':
        newPost = Forum(title=request.form['name'], author=request.form['author'])
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newforumpost.html')

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None
