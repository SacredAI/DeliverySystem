import flask as f
import deliverysystem as d
from ..util import ListForm
import datetime
from random import uniform
maxweight = 500


def create_lists(form, ef, of):
    weight = 0
    driver = d.Employees.query.filter_by(username=form.driverName.data).first()
    driver = d.ECouriers.query.filter_by(employee_ID=driver.employeeid).first()
    quad = form.quadrant.data
    packages = d.ArticleData.query.filter_by(quadrant=quad).all()
    non_priority = []
    for package in packages:
        data = d.DeliveryData.query.get(package.trackingNumber)
        if data.current_status == 'Completed':
            continue
        if data.priority:
            if weight + package.weight <= maxweight:
                weight += package.weight
                data.driver_ID = driver.driverid
                data.current_status = 'Shipping'
                data.date_approved = datetime.datetime.today()
                d.db.session.commit()
        else:
            non_priority.append(package)
    for package in non_priority:
        data = d.DeliveryData.query.get(package.trackingNumber)
        if weight + package.weight <= maxweight:
            weight += package.weight
            data.driver_ID = driver.driverid
            data.current_status = 'Shipping'
            data.date_approved = datetime.datetime.today()
            d.db.session.commit()
    driver.current_lat = uniform(-180, 180)
    driver.current_long = uniform(-90, 90)
    d.db.session.commit()
    lf = ListForm(f.request.form)
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
