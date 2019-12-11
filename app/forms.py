from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Game
from flask_login import current_user

class SignupForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Student email', validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])

    phoneNo = StringField('Phone number', validators=[DataRequired()])
    
    nokName = StringField('Next of kin name', validators=[DataRequired(), Length(min=2, max=50)])
    nokNumber = StringField('Next of kin phone number', validators=[DataRequired()])

    stripNo = IntegerField('Strip number', validators=[DataRequired()])
    submit = SubmitField('Create account')
    
    #validation that the user with same email doesn't exist
    def validate_email(self, email):
        thisUser = User.query.filter_by(email=email.data).first()
        if thisUser:
            raise ValidationError('User with this email address already exits. Please use another email address.')


class LoginForm(FlaskForm):
    email = StringField('Student email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    
    remember = BooleanField('Remember me')            
    submit = SubmitField('Log in')


class UpdateForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Student email', validators=[DataRequired(), Email()])

    phoneNo = StringField('Phone number', validators=[DataRequired()])

    nokName = StringField('Next of kin name', validators=[DataRequired(), Length(min=2, max=50)])
    nokNumber = StringField('Next of kin phone number', validators=[DataRequired()])

    stripNo = IntegerField('Strip number')

    submit = SubmitField('Update account')

    #validation that the user with same email doesn't exist
    def validate_email(self, email):
        if email.data != current_user.email:
            thisUser = User.query.filter_by(email=email.data).first()
            if thisUser:
                raise ValidationError('User with this email address already exits. Please use another email address.')

class NewGameForm(FlaskForm):
    date = StringField('Date and time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    opposition = StringField('Opposition team', validators=[DataRequired()])

    submit = SubmitField('Create game')

class UpdateGameForm(FlaskForm):
    date = StringField('Date and time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    opposition = StringField('Opposition team', validators=[DataRequired()])
    
    result = StringField('Result')

    submit = SubmitField('Update game')

