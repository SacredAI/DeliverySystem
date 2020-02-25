import flask as f
import deliverysystem as d
import string, random
from passlib.hash import sha256_crypt
from ..util import EmployeeForm


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def register_employee(form, of, lf):
    employee = d.Employees(fname=form.firstName.data, lname=form.lastName.data, address=form.address.data,
                           username=form.username.data, emergency_contact=form.emergency_contact.data, TFN=form.TFN.data
                           , position=form.position.data, password=sha256_crypt.encrypt(form.password.data),
                           email=form.email.data, phonenumber=form.phonenumber.data)
    d.db.session.add(employee)
    if form.position.data == 'DRIVER':
        did = id_generator(size=6)
        unique = False
        while unique is False:
            da = d.db.session.query(d.db.exists().where(d.ECouriers.driverid == str(did))).scalar()
            if not da:
                unique = True
            else:
                did = id_generator(size=6)
        driver = d.ECouriers(driverid=did, employee_ID=employee.employeeid, password=sha256_crypt.encrypt(form.password.data),
                             email=form.email.data, phonenumber=form.phonenumber.data)
        d.db.session.add(driver)
    d.db.session.commit()
    f.flash("Successfully Created User")
    ef = EmployeeForm(f.request.form)
    data = d.Employees.query.filter_by(username=f.session['user']).first()
    data = d.ECouriers.query.filter_by(employee_ID=data.employeeid).first()
    if data:
        packages = []
        for package in data.packages:
            da = d.ArticleData.query.get(package.trackingNumber)
            dit = {"trackingNumber": da.trackingNumber, "Sender": da.sender, "Reciever": da.reciever,
                   "Description": da.description, "Weight": da.weight, "Dangerous": da.dangerous_goods,
                   "Priority": package.priority, "Status": package.current_status}
            packages.append(dit)
        return f.render_template("pages/admin.html", of=of, ef=ef, lf=lf, lists=packages)
    return f.render_template("pages/admin.html", of=of, ef=ef, lf=lf)
