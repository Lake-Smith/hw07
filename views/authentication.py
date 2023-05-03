from flask import request, \
    make_response, render_template, redirect
from models import User
import flask_jwt_extended
import datetime

def logout():
    # # Uncomment these lines to delete the cookies and
    # # redirect the user to the login screen
    
    response = make_response(redirect('/login', 302))
    flask_jwt_extended.unset_jwt_cookies(response)
    return response

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).one_or_none()

        if user is None:
            return render_template(
                'login.html',
                message='User not in database'
            )
        if user and not user.check_password(password):
            return render_template(
                'login.html',
                message='Bad password'
            )
        
        #otherwise the user is authorised
        expires = datetime.timedelta(minutes=20)

        #generate the token using the Flask JWT Extended library
        access_token = flask_jwt_extended.create_access_token(
            identity=user.id,
            expires_delta=expires
        )
        response = make_response(redirect('/',302))
        flask_jwt_extended.set_access_cookies(response, access_token)
        return response
        # print('See lecture 25 video + starter files')
        # return 'See lecture 25 video + starter files'
    else:
        return render_template(
            'login.html'
        )

def initialize_routes(app):
    app.add_url_rule('/login', 
        view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)