import flask as f
from .login import login
from ..util import RegistrationForm
from passlib.hash import sha256_crypt
import deliverysystem as d

auth_bp = f.Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()


@auth_bp.route('/register', methods=['POST'])
def register_route():
    form = RegistrationForm(f.request.form)
    if f.request.method == 'POST' and form.validate():
        data = d.Employees.query.filter_by(username=form.username.data).first()
        if data:
            f.flash("User with that Username already Exists")
            return f.redirect(f.url_for('register'))
        data = d.User.query.filter_by(username=form.username.data).first()
        if data:
            f.flash("User with that Username already Exists")
            return f.redirect(f.url_for('register'))
        try:
            u = d.User(fname=form.firstName.data, lname=form.lastName.data, username=form.username.data,
                       password=sha256_crypt.encrypt(form.password.data), email=form.email.data,
                       phonenumber=form.phonenumber.data)
            d.db.session.add(u)
            d.db.session.commit()
            # f.session['u-data'] = u
        except Exception as e:
            print(e)
            return f.render_template("pages/auth.html", register=True, form=form)
        return f.redirect(f.url_for('login'))
    return f.render_template("pages/auth.html", register=True, form=form)


@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    f.session.clear()
    return f.redirect(f.url_for('index'))
