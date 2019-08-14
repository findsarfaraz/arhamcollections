from flask_wtf import Form, FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, BooleanField, validators


class SignupForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])
    confirm_password = PasswordField("Confirm_Password", [validators.DataRequired()])

class LoginForm(FlaskForm):
    email = StringField("Email", [validators.Email()])
    password = PasswordField("Password", [validators.DataRequired()])

class ProfileForm(FlaskForm):
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    gender = SelectField("Gender", choices=[('male', 'Male'), ('female', 'Female')])
    mobile_number = StringField("Contact No", [validators.length(10, 10)])
    dateofbirth = DateField("Date Of Birth", format='%Y-%m-%d')


class AddAddressForm(FlaskForm):
    first_name = StringField("First Name", [validators.DataRequired()])
    last_name = StringField("Last Name", [validators.DataRequired()])
    address1 = StringField("Address1", [validators.DataRequired(), validators.length(25, 150)])
    address2 = StringField("Address2")
    landmark = StringField("Land Mark", [validators.DataRequired(), validators.length(15, 150)])
    state = StringField("State", [validators.DataRequired()])
    city = StringField("City", [validators.DataRequired()])
    pincode = StringField("Pin Code", [validators.DataRequired(), validators.length(6, 6)])
    mobileno = StringField("Mobile No", [validators.DataRequired(), validators.length(10, 10)])
    default_flag = BooleanField("Default Flag")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", [validators.DataRequired()])
    new_password = PasswordField("New Password", [validators.DataRequired()])
    confirm_password = PasswordField("Confirm Password", [validators.DataRequired()])


class ForgotPasswordForm(FlaskForm):
    email = StringField("Registered Email", [validators.DataRequired(), validators.Email()])


class PasswordResetForm(FlaskForm):
    new_password = PasswordField("New Password", [validators.DataRequired()])
    confirm_password = PasswordField("Confirm Password", [validators.DataRequired()])        


    