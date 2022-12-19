import dash
from dash import html, dcc

# function with dynamic content
def rounded_bottom(c=[]):
    return html.Div(children=c, className='card card-body bg-base-100 shadow-md rounded-none border border-t-0 rounded-b-xl border-gray-300 rounded-b-xl')

def rounded_full(c=[]):
    return html.Div(children=c, className='card card-body bg-base-100 shadow-md rounded-xl border border-gray-300')