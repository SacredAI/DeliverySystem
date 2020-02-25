import flask as f
import deliverysystem as d
import random, string
from ..util import OrderForm


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_order(form, ef, lf):
    oid = id_generator()
    unique = False
    while unique is False:
        da = d.db.session.query(d.db.exists().where(d.ArticleData.trackingNumber == str(oid))).scalar()
        if not da:
            unique = True
        else:
            oid = id_generator()
    data = d.User.query.filter_by(fname=form.firstName.data, lname=form.lastName.data).first()
    if data:
        sender = data.username
    else:
        sender = form.firstName.data

    article = d.ArticleData(trackingNumber=oid, sender=sender, reciever=form.recipient.data,
                            description=form.description.data, weight=form.weight.data,
                            dangerous_goods=form.dangerous.data, quadrant=form.quadrant.data)
    delivery = d.DeliveryData(trackingNumber=oid, current_status="Processing", priority=form.priority.data)
    if data:
        try:
            data.packages.append(article)
        except Exception as e:
            print(e)
    d.db.session.add(article)
    d.db.session.add(delivery)
    d.db.session.commit()
    of = OrderForm(f.request.form)
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
    return f.render_template("pages/admin.html", of=of, trackingNumber=oid, ef=ef, lf=lf)
