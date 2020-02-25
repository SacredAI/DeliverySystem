import flask as f
from passlib.hash import sha256_crypt
import deliverysystem as d


def login():
    if auth_check(f.request.form["user"], f.request.form["passw"]) is True:
        f.session['user'] = f.request.form["user"]
        return f.render_template('pages/index.html', failed=True)
    else:
        return f.render_template("pages/auth.html", Failed=True, register=False)
    # Auth Check


def auth_check(uname, pword):
    '''
    :param str uname: The username used during the login process
    :param str pword: The password used during the login process
    :return: returns a failed or passed result
    :rtype: boolean
    '''
    data = d.Employees.query.filter_by(username=uname).first()
    user = False
    if data is None:
        data = d.User.query.filter_by(username=uname).first()
        user = True
    if data is None:
        return False
    try:
        if sha256_crypt.verify(pword, data.password):
            # f.session['u-data'] = data
            if not user:
                f.session['admin'] = True
            return True
        else:
            return False
    except KeyError or TypeError:
        return False
