from models import Following, Post
from flask import Response, request
import json

def get_list_of_user_ids_in_my_network(user_id):
    following = Following.query.filter_by(user_id=user_id).all()
    me_and_my_friend_ids = [rec.following_id for rec in following]
    me_and_my_friend_ids.append(user_id)
    return me_and_my_friend_ids

def can_view_or_404(view_function):
    def wrapper(self, id):
        post = Post.query.get(id)
        me_and_my_friend_ids = get_list_of_user_ids_in_my_network(self.current_user.id)
        if  post is None or post.user_id not in me_and_my_friend_ids:
            error_message = {
                'error': 'post {0} does not exist.'.format(id)
            }
            return Response(json.dumps(error_message), mimetype="application/json", status=404)
        else:
           return view_function(self, id) 
    return wrapper

def can_modify_or_404(view_function):
    def wrapper(self, id):
        post = Post.query.get(id)
        # check if exists:
        if post is None:
            error_message = {
                'error': 'Post={0} not found.'.format(id)
            }
            return Response(json.dumps(error_message), mimetype="application/json", status=404)
        # check if owner:
        elif post.user_id != self.current_user.id:
            error_message = {
                'error': 'You aren\'t allowed to modify a post you don\'t own (post={0}).'.format(id)
            }
            return Response(json.dumps(error_message), mimetype="application/json", status=404)
        else:
            return view_function(self, id) 
            
    return wrapper