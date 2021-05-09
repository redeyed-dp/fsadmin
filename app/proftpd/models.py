from app import db

class Users(db.Model):
    userid = db.Column(db.String(30), primary_key=True, nullable=False)
    passwd = db.Column(db.String(30), nullable=False)
    uid = db.Column(db.Integer, nullable=False, unique=True)
    gid = db.Column(db.Integer, nullable=False)
    homedir = db.Column(db.String(255))
    shell = db.Column(db.String(255))

class Groups(db.Model):
    groupname = db.Column(db.String(30), primary_key=True, nullable=False)
    gid = db.Column(db.Integer, nullable=False, unique=True)
    members = db.Column(db.String(255))