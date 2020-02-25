from functools import wraps
import flask as f
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from random import uniform


# Prevents Accessing the drive unless they are logged in as an admin/user with permissions
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if f.session['admin'] is None:
            return f.redirect(f.url_for('index'))
        return func(*args, **kwargs)

    return decorated_function


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
