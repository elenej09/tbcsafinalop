from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import StringField,PasswordField, SubmitField, RadioField, SelectField, DateField
from wtforms import FloatField, FileField
from wtforms.validators import Optional, NumberRange
from wtforms.validators import DataRequired, Length, Email
from wtforms.widgets import DateInput


class SignupForm(FlaskForm):
    first_name = StringField('სახელი', validators=[DataRequired(), Length(min=2, max=15)])
    last_name = StringField('გვარი', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('მომხმარებლის სახელი', validators=[DataRequired(), Length(min=6)])
    email = StringField('ელ.ფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired(), Length(min=6)])
    gender = RadioField('სქესი', choices=[('მდედრობითი', 'მდედრობითი'), ('მამრობითი', 'მამრობითი'),('სხვა', 'სხვა')], validators=[DataRequired()])
    birthday = DateField('დაბადების თარიღი', format='%Y-%m-%d', validators=[DataRequired()] )
    country = SelectField('ქვეყანა', choices=[
        ('', 'რეგიონი'),
        ('თბილისი', 'თბილისი'),
        ('სვანეთი', 'სვანეთი'),
        ('მცხეთა-მთიანეთი', 'მცხეთა-მთიანეთი'),
        ('იმერეთი', 'იმერეთი'),
        ('აჭარა', 'აჭარა'),
        ('შიდა ქართლი', 'შიდა ქართლი'),
        ('რაჭა', 'რაჭა'),('ქვემო ქართლი', 'ქვემო ქართლი'),
        ('გურია', 'გურია'),('კახეთი', 'კახეთი'),('სამეგრელო', 'სამეგრელო'),('აფხაზეთი', 'აფხაზეთი'),
        ('ლეჩხუმი', 'ლეჩხუმი'),('სამცხე-ჯავახეთი', 'სამცხე-ჯავახეთი')
    ], validators=[DataRequired()])
    submit = SubmitField('გაგრძელება')

class LoginForm(FlaskForm):
    email = StringField('ელ.ფოსტა', validators=[DataRequired(), Email()])
    password = PasswordField('პაროლი', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('გაგრძელება')

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class AdForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired()])
    description = TextAreaField('აღწერა', validators=[DataRequired()])
    contact_info = StringField('საკონტაქტო ინფორმაცია', validators=[DataRequired()])
    submit = SubmitField('განცხადების დამატება')



class CourseForm(FlaskForm):
    title = StringField('კურსის სათაური', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('მოკლე აღწერა', validators=[DataRequired(), Length(min=20)])

    image_file = FileField('კურსის ფოტო', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'მხოლოდ ფოტო ფაილები!')])
    submit = SubmitField('კურსის დამატება')

