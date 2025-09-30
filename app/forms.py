

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from app.models.user import User


class RegistrationForm(FlaskForm):
    name = StringField('ПІБ', validators=[DataRequired(), Length(min=2, max=100)])
    login = StringField('Логін', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердити пароль', validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Завантажити своє фото', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Зареєструватися')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError('Цей логін уже використовується')


class LoginForm(FlaskForm):
    login = StringField('Логін', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField('Зареєструватися')



class StudentForm(FlaskForm):
    student = SelectField('student', choices=[], render_kw={'class':'form-control'})


class TeacherForm(FlaskForm):
    teacher = SelectField('teacher', choices=[], render_kw={'class':'form-control'})