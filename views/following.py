from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import access_utils
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # return all of the "following" records that the current user is following
        following = Following.query.filter_by(user_id=self.current_user.id).all()
        #print(followers.to_dict())
        return Response(json.dumps([follow.to_dict_following() for follow in following]), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        body = request.get_json()
        #(body)
        try:
            followID = int(body.get("user_id"))
            print(self.current_user.id)
            print(followID)
        except:
            return Response(json.dumps({'error': 'The user ID is not in a valad format'}), status=400)
        post = User.query.filter_by(id = followID).scalar() 
        if post == None:
            return Response(json.dumps({'error': 'The user does not exist'}), status=404)
        if Following.query.filter_by(id = followID).scalar() != None :
            return Response(json.dumps({'error': 'You are already following this user'}), status=400)
        #friends_list = access_utils.get_list_of_user_ids_in_my_network(self.current_user.id)
        # print(friends_list)
        # if followID in friends_list:
        #     return Response(json.dumps({'error': 'You are already following this user'}), status=40)
        new_follow = Following(
            user_id = self.current_user.id,
            following_id = followID
        )
        db.session.add(new_follow)    # issues the insert statement
        db.session.commit()   
        return Response(json.dumps(new_follow.to_dict_following()), mimetype="application/json", status=201)

class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
         # delete "bookmark" record where "id"=id
        try:
            newId = int(id)
        except:
            return Response(json.dumps({'error': 'id not in correct format'}), mimetype="application/json", status=404)
        
        following = Following.query.filter_by(id = newId).scalar() 
        if following == None:
            return Response(json.dumps({'error': 'you are not following the user'}), status=404)
        if following.user_id != self.current_user.id:
            return Response(json.dumps({'error': 'You are not authorized to delete this bookmark'}), status=404)
        Following.query.filter_by(id=newId).delete()
        db.session.commit()
        print(id)
        return Response(json.dumps((None)), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<int:id>', 
        '/api/following/<int:id>/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
