import dash
from dash import html, dcc

dash.register_page(__name__, path='/', order=1)

layout = html.Div(children=[
    html.H1(children='Halaman Home', className='text-3xl font-bold'),
])
