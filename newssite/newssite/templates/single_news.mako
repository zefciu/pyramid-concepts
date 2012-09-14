<%def name="scripts()">
</%def>
<%inherit file="base.mako" />
<h1>${news.title}</h1>
<p>${news.published.strftime('%d-%m-%Y')}</p>
${news.content}
