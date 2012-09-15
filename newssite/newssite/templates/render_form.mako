<%inherit file="base.mako" />
<%def name="scripts()">
    <script type="text/javascript" src="/deform/scripts/jquery-1.4.2.min.js">
    </script>
    <script type="text/javascript" src="/deform/scripts/deform.js">
    </script>
    <style type="text/css" >
    @import url(/deform/css/form.css);
    @import url(/deform/css/jquery-ui-timepicker-addon.css);
    @import url(/deform/css/ui-lightness/jquery-ui-1.8.11.custom.css);
    </style>
    <script type="text/javascript" src="/deform/scripts/jquery-ui-1.8.11.custom.min.js">
    </script>
    <script type="text/javascript" src="/deform/scripts/jquery-ui-timepicker-addon.js">
    </script>
    <script type="text/javascript">
    $(function() {
        deform.load();
    });
    </script>
</%def>
${form.render()|n}

