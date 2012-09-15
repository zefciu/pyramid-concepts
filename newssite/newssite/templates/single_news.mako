<%def name="scripts()">
</%def>
<%inherit file="base.mako" />
<h1>${news.title}</h1>
<p>${news.published.strftime('%d-%m-%Y')}</p>
<p>By: ${news.author.login}</p>
${news.content}
% if can_accept:
    <form action="${accept_path}" method="POST" />
    <button type="submit">Zaakceptuj</button>
    </form>
% endif
