from flask import Blueprint, render_template, flash, redirect, url_for, request
from applications.auth.forms import RegisterForm, LoginForm
from app import bcrypt, db
from db_models.user import User
from flask_login import login_user

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Thank You For Your Interest {form.username.data}', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page.landing_page'))
        else:
            flash('Wrong Email or Password', 'danger')
    return render_template('signin.html', form=form)