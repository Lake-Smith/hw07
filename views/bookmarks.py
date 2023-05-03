from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db, Post
import access_utils
import json
import flask_jwt_extended

class BookmarksListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def get(self):
        # get all bookmarks owned by the current user
        bookmarks = Bookmark.query.filter_by(user_id = self.current_user.id).all()
        print(bookmarks)
        return Response(json.dumps([bookmark.to_dict() for bookmark in bookmarks]), mimetype="application/json", status=200)

    @flask_jwt_extended.jwt_required()
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
            return Response(json.dumps({'error': 'You are not authorized to bookmark this post'}), status=404)
        new_bookmark = Bookmark(
            user_id = self.current_user.id,
            post_id = postID
        )
        if Bookmark.query.filter_by(user_id = self.current_user.id, post_id = body.get("post_id")).scalar() != None:
            return Response(json.dumps({'error': 'This post is already bookmarked'}), status=400)
        db.session.add(new_bookmark)    # issues the insert statement
        db.session.commit()   
        return Response(json.dumps(new_bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @flask_jwt_extended.jwt_required()
    def delete(self, id):
        # delete "bookmark" record where "id"=id
        try:
            newId = int(id)
        except:
            return Response(json.dumps({'error': 'id not in correct format'}), mimetype="application/json", status=404)
        
        bookmark = Bookmark.query.filter_by(id = newId).scalar() 
        if bookmark == None:
            return Response(json.dumps({'error': 'The bookmark does not exist'}), status=404)
        friends_list = access_utils.get_list_of_user_ids_in_my_network(self.current_user.id)
        if bookmark.user_id not in friends_list:
            return Response(json.dumps({'error': 'You are not authorized to delete this bookmark'}), status=404)
        Bookmark.query.filter_by(id=newId).delete()
        db.session.commit()
        print(id)
        return Response(json.dumps((None)), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<int:id>', 
        '/api/bookmarks/<int:id>',
        resource_class_kwargs={'current_user': flask_jwt_extended.current_user}
    )
