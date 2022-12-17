import dash
from dash import html, dcc

dash.register_page(__name__, path='/bantuan', order=3)

layout = html.Div(children=[
    html.H1(children='Halaman Bantuan', className='text-3xl font-bold'),
])
