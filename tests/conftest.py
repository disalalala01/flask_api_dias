import pytest
import sys
#from sqlalchemy.orm.session import close_all_sessions #FIXME

sys.path.append('..')

from videoblog import app, Base, engine
from videoblog.models import User, session_db, Video


@pytest.yield_fixture(scope='function')
def testapp():
    _app = app

    Base.metadata.create_all(bind=engine)
    _app.connection = engine.connect()

    yield app

    Base.metadata.drop_all(bind=engine)
    _app.connection.close()


@pytest.fixture(scope='function')
def session(testapp):
    ctx = testapp.app_context()
    ctx.push()

    yield session_db

    session_db.close_all()
    ctx.pop()


@pytest.fixture(scope='function')
def user(session):
    user = User(
        name='Testuser',
        email='test@test.ru',
        password='password'
    )
    session.add(user)
    session.commit()

    return user


@pytest.fixture
def client(testapp):
    return testapp.test_client()


@pytest.fixture
def user_token(user, client):
    res = client.post('/login', json={
        'email': user.email,
        'password': 'password'
    })
    return res.get_json()['access_token']


@pytest.fixture
def user_headers(user_token):
    headers = {
        'Authorization': user_token
    }
    return headers


@pytest.fixture
def video(user, session):
    video = Video(
        user_id=user.id,
        name='Video 1',
        description='Description'
    )
    session.add(video)
    session.commit()

    return video
