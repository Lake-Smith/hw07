from flask import Response, request
from flask_restful import Resource
import json
from models import db, Comment, Post
import access_utils
import flask_jwt_extended

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def post(self):
        # create a new "Comment" based on the data posted in the body 
        body = request.get_json()
        print(body)
        if not body.get("text"):
            return Response(json.dumps({'error': 'Please input something next time'}), status=400)
        try:
            post_id = int(body.get('post_id'))
        except:
            return Response(json.dumps({'error': 'id must be an integer'}), status=400)
        user_id = Post.query.filter_by(id = post_id).scalar()
        if user_id == None:
            return Response(json.dumps({'error': 'Post does not exist'}), status=404)
        friend_ids = access_utils.get_list_of_user_ids_in_my_network(self.current_user.id)
        if user_id.user.id not in friend_ids:
            return Response(json.dumps({'error': 'You are not AUTHORIZED to access this post'}), status=404)

        # print("print print" , utils.get_post_that_user_cannot_access(self.current_user.id))
        new_comment = Comment(
            text = body.get('text'),
            post_id = body.get('post_id'),
            user_id = self.current_user.id
        )
        db.session.add(new_comment)    # issues the insert statement
        db.session.commit()   
        return Response(json.dumps(new_comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "Comment" record where "id"=id
        print(id)
        try:
            post_id = int(id)
        except:
            return Response(json.dumps({'error': 'id must be an integer'}), status=404)
        comment = Comment.query.filter_by(id = post_id).scalar()
        if comment == None:
            return Response(json.dumps({'error': 'Comment does not exist'}), status=404)
        if comment.user.id != self.current_user.id:
            return Response(json.dumps({'error': 'Not your comment silly'}), status=404)
        Comment.query.filter_by(id=post_id).delete()
        db.session.commit()
        return Response(json.dumps((None)), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<int:id>', 
        '/api/comments/<int:id>/',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
