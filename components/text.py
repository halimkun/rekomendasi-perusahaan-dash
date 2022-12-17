import dash
from dash import html

def text_xs(text):
    return html.P(text, className='text-xs font-medium leading-6 text-dark')

def text_sm(text):
    return html.P(text, className='text-sm font-medium leading-6 text-dark')

def text_base(text):
    return html.P(text, className='text-base font-medium leading-6 text-gray-500')

def text_md(text):
    return html.P(text, className='text-md font-medium leading-6 text-dark')

def text_lg(text):
    return html.P(text, className='text-lg font-medium leading-6 text-dark')

def text_xl(text):
    return html.H1(text, className='text-xl font-bold leading-8 text-dark')

def text_2xl(text):
    return html.H2(text, className='text-2xl font-bold leading-8 text-dark')

def text_3xl(text):
    return html.H3(text, className='text-3xl font-bold leading-8 text-dark')

def text_4xl(text):
    return html.H4(text, className='text-4xl font-bold leading-8 text-dark')    
