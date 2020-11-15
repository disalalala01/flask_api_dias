from flask import Blueprint, jsonify
from videoblog import logger, session_db, docs
from videoblog.schemas_flask import AuthSchema, UserSchema
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from videoblog.models import User
from videoblog.base_view import BaseView

users = Blueprint('users', __name__)


@users.route('/register', methods=['POST'])
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
    try:
        user = User(**kwargs)
        session_db.add(user)
        token = user.get_token()
    except Exception as e:
        logger.exception(e)
        return {'message': str(e)}, 400
    finally:
        session_db.commit()
    return jsonify({'access_token': f"Bearer {token}"})


@users.route('/login', methods=['POST'])
@use_kwargs(UserSchema(only=('email', 'password'), partial=True))
@marshal_with(AuthSchema)
def login(**kwargs):
    try:
        user = User.authenticate(**kwargs)
        token = user.get_token()
    except Exception as e:
        logger.exception(e)
        return jsonify({'message': str(e)}), 400
    return jsonify({'access_token': f"Bearer {token}"})


class ProfileView(BaseView):
    @jwt_required
    @marshal_with(UserSchema)
    def get(self):
        user_id = get_jwt_identity()
        try:
            user = User.query.get(user_id)
            if not user:
                raise Exception('User not found')
        except Exception as e:
            logger.exception(e)
        return user


@users.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(login, blueprint='users')
docs.register(register, blueprint='users')
ProfileView.register(users, docs, '/profile', 'profileview')