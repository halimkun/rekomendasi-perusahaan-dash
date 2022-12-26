import dash
from dash import html, dcc
from components import text as tc

dash.register_page(__name__, path='/', order=1)

# flex 2 columns
layout = html.Div([
    html.Div([
        html.Img(src=dash.get_asset_url('i.png'), className='w-[80%]'),
    ], className='flex flex-col justify-center items-center w-full md:w-[50%]'),
    html.Div([
        html.Div([
            html.Div([tc.text_4xl('Recomendation App.')], className='mb-3'),
            tc.text_base('Aplikasi rekomendasi yang memanfaatkan metode klasisifikasi dengan algoritma Decision Tree.'),
            html.Div([], className='mb-3'),
            tc.text_base('Recomendation App ini diperuntukan untuk membantu BKK SMK dalam menentukan rekomendasi perusahaan yang sesuai dengan minat dan bakat siswa.')
        ], className='w-[80%]'),
    ], className='flex flex-col justify-center items-center w-full md:w-[50%]'),
], className='flex flex-col md:flex-row w-full justify-center items-center mt-10 p-3')
