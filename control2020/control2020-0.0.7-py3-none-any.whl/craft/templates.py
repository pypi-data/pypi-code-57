index_template = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script type="application/javascript">
            let ep = document.getElementById("_dash-app-content");
            function watcher() {
                if (ep.firstElementChild.childElementCount > 0) {
                    feather.replace();
                } else {
                    setTimeout(watcher, 10);
                }
            }
            watcher();
        </script>
    </body>
</html>

'''

renderer = '''
var renderer = new DashRenderer({
    request_pre: (payload) => {
        // print out payload parameter
        console.log("pre:", payload);
    },
    request_post: (payload, response) => {
        // print out payload and response parameter
        console.log("post_a:", payload);
        console.log("post_b:", response);
    }
})
'''