from flask import Response, request
from flask_restful import Resource
from models import LikePost, db, Post
import json
import access_utils

class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def post(self):
        # create a new "bookmark" based on the data posted in the body 
        body = request.get_json()
        print(body)
        try:
            postID = int(body.get("post_id"))
        except:
            return Response(json.dumps({'error': 'The post ID is not in a valad format'}), status=400)
        post = Post.query.filter_by(id = postID).scalar() 
        if post == None:
            return Response(json.dumps({'error': 'The post does not exist'}), status=404)
        friends_list = access_utils.get_list_of_user_ids_in_my_network(self.current_user.id)
        if post.user.id not in friends_list:
            return Response(json.dumps({'error': 'You are not authorized to like this post'}), status=404)
        new_like = LikePost(
            user_id = self.current_user.id,
            post_id = postID
        )
        if LikePost.query.filter_by(user_id = self.current_user.id, post_id = body.get("post_id")).scalar() != None:
            return Response(json.dumps({'error': 'you already liked that post'}), status=400)
        db.session.add(new_like)    # issues the insert statement
        db.session.commit()   
        return Response(json.dumps(new_like.to_dict()), mimetype="application/json", status=201)

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        try:
            newId = int(id)
        except:
            return Response(json.dumps({'error': 'id not in correct format'}), mimetype="application/json", status=404)
        
        like = LikePost.query.filter_by(id = newId).scalar() 
        if like == None:
            return Response(json.dumps({'error': 'The like does not exist'}), status=404)
        if like.user_id != self.current_user.id:
            return Response(json.dumps({'error': 'You are not authorized to unlike this post'}), status=404)
        LikePost.query.filter_by(id=newId).delete()
        db.session.commit()
        print(id)
        return Response(json.dumps((None)), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/likes', 
        '/api/posts/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/likes/<int:id>', 
        '/api/posts/likes/<int:id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
