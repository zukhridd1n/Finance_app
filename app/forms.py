from flask_wtf import FlaskForm
from sqlalchemy.testing.pickleable import User
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField("Phone", validators=[DataRequired(), ])
    email = EmailField("Email", validators=[DataRequired(), ])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register", validators=[DataRequired()])


class AddBalancesForm(FlaskForm):
    amount = FloatField('Amount add money', validators=[DataRequired()])
    submit = SubmitField("Add", validators=[DataRequired()])


class DeleteAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField("Phone", validators=[DataRequired(), ])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Delete Account", validators=[DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("Username not found.")


class TransferHistoryForm(FlaskForm):
    submit = SubmitField('Show Transfer History')


class TransferMoneyForm(FlaskForm):
    amount = StringField('Amount')
    submit = SubmitField('Transfer Money')


class ProfileForm(FlaskForm):
    name = StringField('Name')
    email = StringField('Email')
    submit = SubmitField('Update Profile')

