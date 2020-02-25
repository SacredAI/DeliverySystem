import os
import flask as f
from .util import *
from deliverysystem import auth, delivery, admin
from passlib.hash import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from .util import RegistrationForm
import flask_googlemaps as fg

app = f.Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config["SECRET_KEY"]

app.register_blueprint(auth.auth_bp, url_prefix='/auth')
app.register_blueprint(delivery.d_bp, url_prefix='/delivery')
app.register_blueprint(admin.admin_bp, url_prefix="/admin")

fg.GoogleMaps(app)

db = SQLAlchemy(app)
from .util.Models import Employees, User, ECouriers, DeliveryData, ArticleData

db.create_all()

admin = Employees.query.filter_by(username='admin').first()  # Checks if the admin account exists creates one if it
# doesn't.
if admin is None:
    e = Employees(fname="admin", username="admin", position="admin", password=sha256_crypt.hash("password"),
                  email="admin@example.com", )
    db.session.add(e)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    return f.render_template("pages/index.html", Failed=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return f.render_template("pages/auth.html", register=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(f.request.form)
    return f.render_template("pages/auth.html", register=True, form=form)


@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    try:
        if f.session['user']:
            data = []
            d = User.query.filter_by(username=f.session['user']).first()
            if d:
                if d.packages:
                    for k in d.packages:
                        da = DeliveryData.query.get(k.trackingNumber)
                        dit = {"trackingNumber": k.trackingNumber, "Sender": k.sender, "Reciever": k.reciever,
                               "Description": k.description, "Weight": k.weight, "Dangerous": k.dangerous_goods,
                               "Priority": da.priority, "Status": da.current_status}
                        data.append(dit)
                    return f.render_template("pages/tracking.html", orders=data)
    except KeyError:
        return f.render_template("pages/tracking.html")
    return f.render_template("pages/tracking.html")


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


# adds a timestamp to then end of a url to prevent caching
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return f.url_for(endpoint, **values)


@app.errorhandler(404)
def page_not_found(error):
    return f.render_template("codes/404.html"), 404
