import flask as f
import deliverysystem as d
from ..util import OrderForm, EmployeeForm, ListForm
from .orders import create_order
from .employees import register_employee
from .lists import create_lists
import datetime

admin_bp = f.Blueprint('admin', __name__)


@admin_bp.route('main')
def main():
    of = OrderForm(f.request.form)
    ef = EmployeeForm(f.request.form)
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


@admin_bp.route('create', methods=['POST'])
def create():
    of = OrderForm(f.request.form)
    ef = EmployeeForm(f.request.form)
    lf = ListForm(f.request.form)
    if f.request.method == 'POST' and of.validate():
        return create_order(of, ef, lf)
    return f.render_template("pages/admin.html", of=of, ef=ef, lf=lf)


@admin_bp.route('register', methods=['POST'])
def register():
    of = OrderForm(f.request.form)
    ef = EmployeeForm(f.request.form)
    lf = ListForm(f.request.form)
    if f.request.method == 'POST' and ef.validate():
        return register_employee(ef, of, lf)
    return f.render_template("pages/admin.html", of=of, ef=ef, lf=lf)


@admin_bp.route('createlist', methods=['POST'])
def createlist():
    of = OrderForm(f.request.form)
    ef = EmployeeForm(f.request.form)
    lf = ListForm(f.request.form)
    if f.request.method == 'POST' and lf.validate():
        return create_lists(lf, ef, of)
    return f.render_template("pages/admin.html", of=of, ef=ef, lf=lf)


@admin_bp.route('accept', methods=['POST'])
def accept():
    data = d.Employees.query.filter_by(username=f.session['user']).first()
    data = d.ECouriers.query.filter_by(employee_ID=data.employeeid).first()
    if data:
        for package in data.packages:
            package.date_completed = datetime.datetime.today()
            package.current_status = 'Completed'
        d.db.session.commit()
    return f.redirect(f.url_for('admin.main'))

