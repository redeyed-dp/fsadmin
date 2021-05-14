from app import db
from app.proftpd import bp
from app.proftpd.models import Users, Groups
from app.proftpd.forms import UserForm, GroupForm
from sqlalchemy.sql import func
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required
from os import listdir, path
import random

@bp.route("/")
@bp.route("/users")
@login_required
def users():
    users = db.session.query(Users).all()
    return render_template("proftpd_users.html", users=users)

@bp.route("/users/add", methods=['GET', 'POST'])
@login_required
def users_add():
    form = UserForm()
    form.gid.choices = db.session.query(Groups.gid, Groups.groupname).all()
    if form.validate_on_submit():
        exists = db.session.query(Users).filter(Users.userid==form.userid.data).count()
        if exists > 0:
            flash("Пользователь {} уже существует".format(form.userid.data))
            return render_template("proftpd_user_edit.html", form=form)
        exists = db.session.query(Users).filter(Users.uid == form.uid.data).count()
        if exists > 0:
            flash("Пользователь с UID {} уже существует".format(form.uid.data))
            return render_template("proftpd_user_edit.html", form=form)
        user = Users(userid=form.userid.data, passwd=form.passwd.data, uid=form.uid.data, gid=form.gid.data,
                     homedir=form.homedir.data, shell=form.shell.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('proftpd.users'))
    form.uid.data = db.session.query(func.max(Users.uid)).scalar() + 1
    form.homedir.data = '/ftp'
    form.shell.data = '/sbin/nologin'
    return render_template("proftpd_user_edit.html", form=form)

@bp.route("/users/del/<userid>")
@login_required
def users_del(userid):
    try:
        user = db.session.query(Users).filter(Users.userid==userid).one()
        db.session.delete(user)
        db.session.commit()
        flash("Аккаунт {} удален".format(userid))
    except:
        flash("Аккаунта {} не существует".format(userid))
    return redirect(url_for("proftpd.users"))

@bp.route("/users/edit/<userid>", methods=['GET', 'POST'])
@login_required
def users_edit(userid):
    form = UserForm()
    form.gid.choices = db.session.query(Groups.gid, Groups.groupname).all()
    try:
        user = db.session.query(Users).filter(Users.userid==userid).one()
    except:
        flash("Аккаунта {} не существует".format(userid))
        return redirect(url_for("proftpd.users"))
    if form.validate_on_submit():
        user.userid = form.userid.data
        user.passwd = form.passwd.data
        user.uid = form.uid.data
        user.gid = form.gid.data
        user.homedir = form.homedir.data
        user.shell = form.shell.data
        db.session.commit()
        flash("Аккаунт {} изменен".format(userid))
        return redirect(url_for("proftpd.users"))
    form.userid.data = userid
    form.passwd.data = user.passwd
    form.uid.data = user.uid
    form.gid.default = user.gid
    form.homedir.data = user.homedir
    form.shell.data = user.shell
    return render_template("proftpd_user_edit.html", form=form)

@bp.route("/groups")
@login_required
def groups():
    groups = db.session.query(Groups).all()
    return render_template("proftpd_groups.html", groups=groups)

@bp.route("/groups/add", methods=['GET', 'POST'])
@login_required
def groups_add():
    form = GroupForm()
    if form.validate_on_submit():
        exists = db.session.query(Groups).filter(Groups.gid==form.gid.data).count()
        if exists > 0:
            flash("Группа с GID {} уже существует".format(form.gid.data))
            return render_template("proftpd_group_edit.html", form=form)
        exists = db.session.query(Groups).filter(Groups.groupname==form.groupname.data).count()
        if exists > 0:
            flash("Группа {} уже существует".format(form.groupname.data))
            return render_template("proftpd_group_edit.html", form=form)
        group = Groups(groupname=form.groupname.data, gid=form.gid.data, members=form.members.data)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('proftpd.groups'))
    return render_template("proftpd_group_edit.html", form=form)

@bp.route("/groups/del/<int:gid>")
@login_required
def groups_del(gid):
    users = db.session.query(Users).filter(Users.gid==gid).count()
    if users > 0:
        flash("В группе {} есть пользователи".format(gid))
        return redirect(url_for('proftpd.groups'))
    try:
        group = db.session.query(Groups).filter(Groups.gid==gid).one()
        db.session.delete(group)
        db.session.commit()
        flash("Группа {} удалена".format(gid))
    except:
        flash("Группы {} не существует".format(gid))
    return redirect(url_for('proftpd.groups'))

@bp.route("/groups/edit/<int:gid>", methods=['GET', 'POST'])
@login_required
def groups_edit(gid):
    try:
        group = db.session.query(Groups).filter(Groups.gid==gid).one()
    except:
        flash("Группы {} не существует".format(gid))
        return redirect(url_for('proftpd.groups'))
    form = GroupForm()
    if form.validate_on_submit():
        group.groupname = form.groupname.data
        group.members = form.members.data
        db.session.commit()
        flash("Группа {} изменена".format(gid))
        return redirect(url_for('proftpd.groups'))
    form.gid.data = gid
    form.gid.render_kw = {'readonly': True}
    form.groupname.data = group.groupname
    form.members.data = group.members
    return render_template("proftpd_group_edit.html", form=form)

@bp.route("/randompassword")
@login_required
def randompassword():
    password=str()
    for i in range(0,10):
        password+=str(random.randrange(10))
    return password

@bp.route("/homedir", methods=['POST'])
@login_required
def homedir():
    directories = []
    directory = request.form['homedir']
    exists = True
    if not path.isdir(directory):
        exists = False
        directory = '/'
    names = listdir(directory)
    for name in names:
        if path.isdir(path.join(directory, name)):
            directories.append(name)
    return jsonify({'exists': exists, 'parent': directory, 'directories': directories})