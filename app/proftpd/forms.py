from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Regexp, Length, NumberRange

class UserForm(FlaskForm):
    userid = StringField('Логин', validators=[InputRequired(message='Поле Логин пустое')])
    passwd = StringField('Пароль', validators=[InputRequired(message='Поле Пароль пустое')])
    uid = IntegerField('UID', validators=[NumberRange(min=5000, max=6000, message='Недопустимое значение UID')])
    gid = SelectField('GID', coerce=int)
    homedir = StringField('Домашний каталог', validators=[Length(max=255, message='Слишком длинный путь к домашнему каталогу')])
    shell = StringField('shell')
    submit = SubmitField('Сохранить')

class GroupForm(FlaskForm):
    groupname = StringField('Имя группы', validators=[InputRequired(message='Введите имя группы')])
    gid = IntegerField('GID', validators=[NumberRange(min=5000, max=6000, message='Недопустимое значение')])
    members = StringField('Члены группы', validators=[Length(max=255, message='Недопустимая длина')])
    submit = SubmitField('Сохранить')