import dash
from dash import Dash, dcc, html

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        {
            "href": "https://cdn.jsdelivr.net/npm/daisyui@2.43.2/dist/full.css",
            "rel": "stylesheet",
            "type": "text/css"
        },
        {
            "href": "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css",
            "rel": "stylesheet",
        },
    ],
    external_scripts=[
        "https://cdn.tailwindcss.com",
    ],
    suppress_callback_exceptions=True,
    serve_locally=True,
    index_string='''
        <!DOCTYPE html>
        <html data-theme="light">
            <head>
                <title>{%title%}</title>
                
                {%metas%}
                
                {%favicon%}
                {%css%}
            </head>
            <body>
            <!--[if IE]>
                <script>
                    alert("Dash v2.7+ does not support Internet Explorer. Please use a newer browser."
                </script>
            <![endif]-->

                {%app_entry%}
                
                <footer></footer>
                
                {%config%}
                {%scripts%}
                {%renderer%}
            </body>
        </html>
    '''
)


server = app.server

from components import navbar


app.layout = html.Div([
    navbar.render,
    html.Div([
        dash.page_container
    ], id='page-container', className='w-full mt-5 mb-10 px-3 md:px-10')
], id='main')

if __name__ == '__main__':
    app.run_server(debug=True)
