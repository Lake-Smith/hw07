import flask_jwt_extended
from flask import redirect
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt import ExpiredSignatureError

def jwt_or_login(view_function):
    def wrapper(*args, **kwargs):
        try:
            jwt_header, jwt_data = flask_jwt_extended.verify_jwt_in_request()
            print(jwt_header, jwt_data)
            return view_function(*args, **kwargs)
        except ExpiredSignatureError:
            return redirect('/login', code=302)
        except NoAuthorizationError:
            return redirect('/login', code=302)
            
    # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
    wrapper.__name__ = view_function.__name__
    return wrapper 