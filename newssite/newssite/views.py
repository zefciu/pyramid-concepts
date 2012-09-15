import colander
import deform

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import resource_path
from pyramid.security import remember

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    NewsCollection,
    News,
    UsersCollection,
    User,
    )

class RegisterSchema(colander.MappingSchema):
    login = colander.SchemaNode(colander.String())
    passwd = colander.SchemaNode(
        colander.String(), widget=deform.widget.CheckedPasswordWidget(),
    )
    groups = colander.SchemaNode(colander.String())

@view_config(
    context=UsersCollection, renderer='newssite:templates/render_form.mako',
    name='register'
)
def register_user(context, request):
    form = deform.Form(RegisterSchema(), buttons=('submit',))
    if 'submit' in request.POST:
        data = request.POST.items()
        try:
            data = form.validate(data)
        except deform.ValidationFailure:
            pass
        else:
            user = User(**data)
            user.__parent__ = context
            DBSession.add(user)
            return HTTPFound(location=resource_path(user))
    return {'form': form}

class LoginSchema(colander.MappingSchema):
    login = colander.SchemaNode(colander.String())
    passwd = colander.SchemaNode(
        colander.String(), widget=deform.widget.PasswordWidget(),
    )

def _validate_password(form, value):
    MSG = 'Invalid login or password'
    try:
        user = DBSession.query(User).filter(User.login == value['login']).one()
    except NoResultFound:
        raise colander.Invalid(MSG)
    if not user.check_passwd(value['passwd']):
        raise colander.Invalid(MSG)

@view_config(
    context=User, renderer='newssite:templates/single_user.mako',
)
def view_user(context, request):
    return {'user': context}


@view_config(context=UsersCollection, name='login',
        renderer='newssite:templates/render_form.mako')
def login(context, request):
    form = deform.Form(
        LoginSchema(validator=_validate_password), buttons=('submit',)
    )
    if 'submit' in request.POST:
        data = request.POST.items()
        try:
            data = form.validate(data)
        except deform.ValidationFailure:
            pass
        else:
            response = HTTPFound(location='/news')
            response.headerlist += remember(request, data['login'])
            return response
    return {'form': form}

class NewsSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    content = colander.SchemaNode(
        colander.String(), widget=deform.widget.TextAreaWidget(
            rows=25, cols=80
        )
    )
    published = colander.SchemaNode(colander.DateTime())

@view_config(context=NewsCollection, name='add',
        renderer='newssite:templates/render_form.mako', permission='add')
def add_news(context, request):
    form = deform.Form(NewsSchema(), buttons=('submit',))
    if 'submit' in request.POST:
        data = request.POST.items()
        try:
            data = form.validate(data)
        except deform.ValidationFailure:
            pass
        else:
            news = News(**data)
            news.__parent__ = context
            news.author = request.user_object
            DBSession.add(news)
            return HTTPFound(location=resource_path(news))
    return {'form': form}

@view_config(
    context=NewsCollection, renderer='newssite:templates/news_index.mako'
)
def display_news_index(context, request):
    return {'news': context.get_index()}

@view_config(context=News, renderer='newssite:templates/single_news.mako')
def display_single_news(context, request):
    return {'news':context}
