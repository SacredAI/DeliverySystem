from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, SelectField, ValidationError
import deliverysystem as d


class RegistrationForm(Form):
    firstName = StringField('First Name', [validators.InputRequired()])
    lastName = StringField('Last Name', [validators.InputRequired()])
    username = StringField('Username', [validators.Length(min=4, max=25, message='username is too short')])
    email = StringField('Email Address', [validators.Optional(), validators.Email("Please enter a valid email")])
    phonenumber = IntegerField('Phone Number', [validators.Optional()])
    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.Length(6, 20, 'Password is too Short'),
        validators.EqualTo('confirm', message='Passwords must match'),
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class OrderForm(Form):
    firstName = StringField('First Name', [validators.InputRequired()])
    lastName = StringField('Last Name', [validators.InputRequired()])
    description = StringField('Description')
    deliveryAddress = StringField('Address', [validators.InputRequired()])
    recipient = StringField('Recipient', [validators.InputRequired()])
    quadrant = SelectField('Delivery Quadrant', choices=[('NORTH', 'north'), ('SOUTH', 'south'), ('EAST', 'east'), ('WEST', 'west')])
    dangerous = BooleanField('Dangerous Goods')
    weight = StringField('Weight', [validators.InputRequired()])
    priority = BooleanField('Priority')


class EmployeeForm(Form):
    firstName = StringField('First Name', [validators.InputRequired()])
    lastName = StringField('Last Name', [validators.InputRequired()])
    address = StringField('Address', [validators.InputRequired()])
    username = StringField('UserName', [validators.InputRequired()])
    emergency_contact = StringField('Emergency Contact')
    TFN = StringField("Tax File Number", [validators.InputRequired()])
    position = SelectField('Position', choices=[('ADMIN', 'admin'), ('DRIVER', 'Courier'), ('SERVICE', 'Customer '
                                                                                                       'Service'),
                                                ('MANAGER', 'Delivery Manager')])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.Length(6, 20, 'Password is too Short'),
    ])
    email = StringField('Email Address', [validators.Optional(), validators.Email("Please enter a valid email")])
    phonenumber = IntegerField('Phone Number', [validators.Optional()])


def user_exists(form, field):
    da = d.db.session.query(d.db.exists().where(d.Employees.username == str(field.data))).scalar()
    if not da:
        print("Uhh")
        raise ValidationError('User doesn\'t exist.')


class ListForm(Form):
    driverName = StringField('Drivers UserName', [validators.InputRequired(), user_exists])
    quadrant = SelectField('Delivery Quadrant', choices=[('NORTH', 'north'), ('SOUTH', 'south'), ('EAST', 'east'), ('WEST', 'west')])

