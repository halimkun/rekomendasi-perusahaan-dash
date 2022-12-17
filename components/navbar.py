import dash
from dash import html, dcc


def layout():
    # get active page
    return html.Div([
        html.Div([
            html.A('RECAP', className='btn btn-ghost normal-case text-xl text-white hover:bg-gray-700 rounded-lg', href='/'),
        ], className='flex-1'),

        html.Div([
            html.Ul(className='menu menu-horizontal px-1"', children=[
                html.Li(
                    dcc.Link(
                        f"{page['name']}", href=page["relative_path"],
                        className="block px-4 mx-1 py-2 text-white hover:bg-gray-700 rounded-lg",
                    )
                )
                for page in dash.page_registry.values()
            ])
        ], className='flex-none'),
    ], className='navbar bg-primary shadow-md w-full z-10 px-10')


render = layout()
