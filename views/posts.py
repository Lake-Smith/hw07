from flask import Response, request
from flask_restful import Resource
from models import Post, Following, db
from views import get_authorized_user_ids
import access_utils
import json
import flask_jwt_extended

def get_path():
    return request.host_url + 'api/posts/'

class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    @flask_jwt_extended.jwt_required()
    def get(self):
        me_and_my_friend_ids = access_utils.get_list_of_user_ids_in_my_network(self.current_user.id)
        try:
            limit = request.args.get('limit') or 20
            limit = int(limit)
        except:
            return Response(
                json.dumps({'error': 'No string for limit.'}), status=400
            )
        if limit > 50:
            return Response(
                json.dumps({'error': 'Bad data. Limit cannot exceed 20.'}), status=400
            )
        posts = Post.query.filter(Post.user_id.in_(me_and_my_friend_ids)).limit(limit)
        return Response(json.dumps([post.to_dict() for post in posts]), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    def post(self):
        # request.get_json() is holding the data that the user
        # just sent over the network. Stored as a python dictionary
        body = request.get_json()
        if not body.get('image_url'):
            return Response(json.dumps({'error': 'image_url required'}), status=400)
        # convert the data that the user sent over HTTP to a SQLAlchemy object
        new_post = Post(
            image_url=body.get('image_url'),
            user_id=self.current_user.id, # must be a valid user_id or will throw an error
            caption=body.get('caption'),
            alt_text=body.get('alt_text')
        )
        # save it to the database
        db.session.add(new_post)    # issues the insert statement
        db.session.commit()   

        # send the new data object to the user
        return Response(json.dumps(new_post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        
    @flask_jwt_extended.jwt_required()
    @access_utils.can_modify_or_404
    def patch(self, id):
        '''
        If I want to update a post, what do I do?
        1. Go get the current post. And check if they're authorized.
        2. Update only the items that the user changed
        3. Save to the DB
        4. Return the final representation to the user
        '''
        # update post based on the data posted in the body 
        body = request.get_json()

        post = Post.query.get(id)

        # only update the data fields that the user wants to change:
        if body.get('image_url'):
            post.image_url = body.get('image_url') 
        if body.get('caption'):
            post.caption = body.get('caption')  
        if body.get('alt_text'):
            post.alt_text = body.get('alt_text')  

        # save back to database:
        db.session.commit() 

        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    @access_utils.can_modify_or_404
    def delete(self, id):
        Post.query.filter_by(id=id).delete()
        db.session.commit()
        return Response(json.dumps(None), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
    @access_utils.can_view_or_404
    def get(self, id):
        # get the post based on the id
        # yourself and your friends
        post = Post.query.get(id)
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

def initialize_routes(api):
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<int:id>', '/api/posts/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )