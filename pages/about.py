import dash
from dash import html, dcc

dash.register_page(__name__, path='/about', order=4)

layout = html.Div(children=[
    html.H1(children='Halaman About', className='text-3xl font-bold'),
])
