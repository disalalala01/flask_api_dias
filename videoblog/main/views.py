from flask import Blueprint, jsonify
from videoblog import logger, docs
from videoblog.schemas_flask import VideoSchema
from flask_apispec import use_kwargs, marshal_with
from videoblog.models import Video
from flask_jwt_extended import jwt_required, get_jwt_identity
from videoblog.base_view import BaseView


videos = Blueprint('videos', __name__)


class ListView(BaseView):

    @marshal_with(VideoSchema(many=True))
    def get(self):
        try:
            videos = Video.get_list()
            print(videos)
        except Exception as e:
            print(e)
            logger.exception(e)
            return {'message': str(e)}, 400
        return videos


@videos.route('/tutorials', methods=['GET'])
@jwt_required
@marshal_with(VideoSchema(many=True))
def get_list():
    try:
        user_id = get_jwt_identity()
        videos = Video.get_user_list(user_id=user_id)
    except Exception as e:
        logger.exception(e)
        return {'message': str(e)}, 400
    return videos


@videos.route('/tutorials', methods=['POST'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def add_list(**kwargs):
    try:
        user_id = get_jwt_identity()
        new_one = Video(user_id=user_id, **kwargs)
        new_one.save()
    except Exception as e:
        logger.exception(e)
        return {'message': str(e)}, 400
    return new_one


@videos.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(tutorial_id: int, **kwargs):
    try:
        user_id = get_jwt_identity()
        item = Video.get(tutorial_id, user_id)
        item.update(**kwargs)
    except Exception as e:
        logger.exception(e)
        return {'message': str(e)}, 400
    return item


@videos.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
@jwt_required
@marshal_with(VideoSchema)
def delete_list(tutorial_id):
    try:
        user_id = get_jwt_identity()
        item = Video.get(tutorial_id=tutorial_id, user_id=user_id)
        item.delete()
    except Exception as e:
        logger.exception(e)
        return {'message': str(e)}, 400
    return '', 204


@videos.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_list, blueprint='videos')
docs.register(add_list, blueprint='videos')
docs.register(update_list, blueprint='videos')
docs.register(delete_list, blueprint='videos')
ListView.register(videos, docs, '/main', 'listview')