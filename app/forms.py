from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    def validate_username(self, check_user):
        user = User.query.filter_by(username=check_user.data).first()
        if user:
            raise ValidationError('Usuario já existe! Cadastre outro nome de usuário.')
        
    def validate_email(self, check_user):
        email = User.query.filter_by(email=check_user.data).first()
        if email:
            raise ValidationError('Email já existe! Cadastre outro email.')

    def validate_senha(self,check_user):
        senha = User.query.filter_by(ppassword_hash=check_user.data).first()
        if senha:
            raise ValidationError('Senha já existe! Cadastre outra senha.')

    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=30)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirmação de Senha:',validators=[DataRequired(),EqualTo('password')])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Sign Up')


class ProductsForm(FlaskForm):
    name = StringField('Nome',validators=[DataRequired()])
    price = StringField('Preço',validators=[DataRequired()])
    description =TextAreaField('Descrição',validators=[DataRequired()])
    submit = SubmitField('Cadastrar !')