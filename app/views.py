from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, AdminForm
from app.models import Admin

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            admin = db.session.query(Admin).filter(Admin.login == form.login.data).one()
            if admin.check_password(form.password.data):
                login_user(admin, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
            flash('Неверный логин или пароль')
        except:
            flash('Неверный логин или пароль')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    from app.proftpd.menu import menu
    mainmenu = dict()
    mainmenu.update(menu)
    return render_template("index.html", mm=mainmenu)

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    form = AdminForm()
    try:
        admin = db.session.query(Admin).filter(Admin.id==1).one()
        form.login.data = admin.login
    except:
        form.login.data = 'admin'
    if form.validate_on_submit():
        try:
            admin = db.session.query(Admin).filter(Admin.id==1).one()
            admin.login = form.login.data
            admin.set_password(form.password.data)
            db.session.commit()
        except:
            admin = Admin(login=form.login.data)
            admin.set_password(form.password.data)
            db.session.add(admin)
            db.session.commit()
        flash("Учетная запись администратора изменена")
        return redirect(url_for("index"))
    return render_template("admin.html", form=form)