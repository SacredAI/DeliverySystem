from deliverysystem import db
import datetime


class ArticleData(db.Model):
    trackingNumber = db.Column(db.String(255), primary_key=True)
    u_id = db.Column(db.String(255), db.ForeignKey('user.userID'))
    sender = db.Column(db.String(255))
    reciever = db.Column(db.String(255))
    description = db.Column(db.String(255))
    weight = db.Column(db.Float)
    dangerous_goods = db.Column(db.Boolean)
    quadrant = db.Column(db.String(255))

    def __repr__(self):
        return '<Driver ID %r>' % self.trackingNumber


class Employees(db.Model):
    employeeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), unique=True)
    lname = db.Column(db.String(50))
    address = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    emergency_contact = db.Column(db.String(50))
    TFN = db.Column(db.String(255))
    position = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)
    phonenumber = db.Column(db.String(50))

    def __repr__(self):
        return '<First Name {}>'.format(self.fname)


class ECouriers(db.Model):
    driverid = db.Column(db.String(50), primary_key=True)
    employee_ID = db.Column(db.Integer, db.ForeignKey('employees.employeeid'))

    current_long = db.Column(db.String(255))
    current_lat = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)
    phonenumber = db.Column(db.String(50))
    packages = db.relationship('DeliveryData', backref="ECouriers", lazy=True)

    def __repr__(self):
        return '<Driver ID %r>' % self.driverID


class DeliveryData(db.Model):
    trackingNumber = db.Column(db.String(255), db.ForeignKey('article_data.trackingNumber'), primary_key=True)
    driver_ID = db.Column(db.String(50), db.ForeignKey('e_couriers.driverid'))

    date_approved = db.Column(db.DateTime)
    date_completed = db.Column(db.DateTime)
    current_status = db.Column(db.String(50))
    priority = db.Column(db.Boolean)

    def __repr__(self):
        return '<Driver ID %r>' % self.trackingNumber


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(120), unique=True)
    phonenumber = db.Column(db.String(50))
    packages = db.relationship('ArticleData', backref="User", lazy=True)

    def __repr__(self):
        return '<First Name %r>' % self.fname
