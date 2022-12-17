import dash
from dash import html, dcc

def uploaded_file():
    return html.Div([
        html.P(
            id='uploaded-file-name',
            className='text-gray-600',
        ),
        html.Button(
            id='btn-close-file-uploaded', children="✖", n_clicks=0,
            className='bg-red-500 text-white btn-circle w-6 h-6 ml-3 flex justify-center items-center'
        )
    ],
        id='uploaded-file',
        className='flex flex-row w-full gap-3 justify-between items-center bg-gray-200 p-3 rounded-lg mt-5',
        style={'visibility': 'hidden', 'display': 'none'}
    )