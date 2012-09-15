from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm.exc import NoResultFound
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from newssite.models import DBSession, Root, User

def auth_callback(login, request):
    try:
        user = DBSession.query(User).filter(User.login==login).one()
        request.user_object = user
    except NoResultFound:
        return False
    return (
        ['user:{0}'.format(login)] +
        ['group:{0}'.format(group) for group in user.groups.split(',')]
    )

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings, root_factory=Root,
        authentication_policy = AuthTktAuthenticationPolicy(
            secret=settings['auth.secret'],
            callback=auth_callback,
        ), authorization_policy=ACLAuthorizationPolicy()
    )
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform', 'deform:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

