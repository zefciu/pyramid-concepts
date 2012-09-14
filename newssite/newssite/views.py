from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    NewsCollection,
    News,
    )

@view_config(
    context=NewsCollection, renderer='newssite:templates/news_index.mako'
)
def display_news_index(context, request):
    return {'news': context.get_index()}

@view_config(context=News, renderer='newssite:templates/single_news.mako')
def display_single_news(context, request):
    return {'news':context}
