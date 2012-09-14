<%def name="scripts()">
</%def>
<%inherit file="base.mako" />
<ul>
% for news_item in news:
<li><a href="${news_item.get_link()}">${news_item.title}</a></li>
% endfor
</ul>
