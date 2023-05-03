from models import User
import flask_jwt_extended
from flask import Response, request
from flask_restful import Resource
import json
from datetime import timezone, datetime, timedelta

class AccessTokenEndpoint(Resource):
    # Your Job:
    # Create a route to authenticate your users and return JWT Token. The
    # create_access_token() function is used to actually generate the JWT.
    def post(self):
        body = request.get_json() or {}
        # accepts a username and a password for the body
        username = body.get('username')
        password = body.get('password')
        
        #query database for the user
        user = User.query.filter_by(username = username).one_or_none()
        
        if user is None:
            return Response( json.dumps({
                    'message': 'bad username'
                }),
                status=401
            )
        
        if user.check_password(password):
            return Response( json.dumps({
                    'access_token': flask_jwt_extended.create_access_token(identity=user.id),
                    'refresh_token': flask_jwt_extended.create_refresh_token(identity=user.id)
                }),
                status=200
            )
        else:
            return Response(
                json.dumps({
                    'message': 'bad password'
                }),
                status=401
            )


        # check the database to make sure this particular user is valid
        # if they are return an access and refresh token
        print(body)
        '''
        if a matching user is found in the DB, encode the user's id in the JWT
        access and refresh token as follows:
        access_token = flask_jwt_extended.create_access_token(identity=user.id)
        refresh_token = flask_jwt_extended.create_refresh_token(identity=user.id)
        '''
        return 'Implement me!'


class RefreshTokenEndpoint(Resource):
    # done for you :). 
    def post(self):
        body = request.get_json() or {}
        refresh_token = body.get('refresh_token')
        if not refresh_token:
            return Response(json.dumps({ 
                    "message": "missing refresh_token"
                }), mimetype="application/json", status=400)
        try:
            decoded_token = flask_jwt_extended.decode_token(refresh_token)
            exp_timestamp = decoded_token.get("exp")
            now = datetime.timestamp(datetime.now(timezone.utc))
        except:
            return Response(json.dumps({ 
                "message": "Invalid refresh_token={0}. Could not decode.".format(refresh_token)
            }), mimetype="application/json", status=401)

        # if the refresh token is valid and hasn't expired, issue a
        # new access token:
        if exp_timestamp > now:
            identity = decoded_token.get('sub')
            access_token = flask_jwt_extended.create_access_token(identity=identity)
            return Response(json.dumps({ 
                    "access_token": access_token, 
                    "refresh_token": refresh_token
                }), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({ 
                    "message": "refresh_token has expired"
                }), mimetype="application/json", status=401)

def initialize_routes(api):
    api.add_resource(
        AccessTokenEndpoint, 
        '/api/token', '/api/token/'
    )

    api.add_resource(
        RefreshTokenEndpoint, 
        '/api/token/refresh', '/api/token/refresh/'
    )