from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, IntegerField, StringField, FileField, SelectField, PasswordField, BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, NumberRange, ValidationError, EqualTo, Email, Optional, Length
from app.models import User
from app import db
from flask_login import current_user
from werkzeug.security import check_password_hash


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_username(form, field):
        q = db.select(User).where(User.username==field.data)
        if db.session.scalar(q):
            raise ValidationError("Username already taken, please choose another")

    @staticmethod
    def validate_email(form, field):
        q = db.select(User).where(User.email==field.data)
        if db.session.scalar(q):
            raise ValidationError("Email address already taken, please choose another")


class ReviewForm(FlaskForm):
    edit = HiddenField(default='')
    feature = SelectField(choices=[('Chatbot','Chatbot'),('Trend Report','Trend Report'),('Review System','Review System'),
                                   ('General','General')])
    stars = SelectField(choices=[(-1,'Select rating'),(0,'0'),(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], default=-1,
                        validators=[DataRequired()])
    text = TextAreaField('Review Text', validators=[Optional(), Length(max=1024)] )
    submit = SubmitField('Add Review')
    update = SubmitField('Update Review')

    @staticmethod
    def validate_stars(form, field):
        if not (0 <= int(field.data) <= 5):
            raise ValidationError("You must choose a number of stars")


class FeedbackForm(FlaskForm):
    feedback = TextAreaField(
        'Your Feedback',
        validators=[DataRequired(message='Feedback cannot be empty.')],
        render_kw={"rows": 5, "placeholder": "Write your feedback here..."}
    )
    submit = SubmitField('Submit Feedback')


class ChangeEmailForm(FlaskForm):
    new_email = StringField("New e-mail address", validators=[DataRequired(), Email()])
    password = PasswordField("Current password", validators=[DataRequired()])
    submit = SubmitField("Update e-mail")

    @staticmethod
    def validate_password(self, field):
        if not check_password_hash(current_user.password_hash, field.data):
            raise ValidationError("Password is incorrect.")


class ResetPasswordForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired()])
    confirm = PasswordField("Confirm new password", validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Reset password")

    @staticmethod
    def validate_current_password(self, field):
        if not check_password_hash(current_user.password_hash, field.data):
            raise ValidationError("Password is incorrect.")