import dash
from dash import html, dcc

def uploaded_file():
    return html.Div([
        html.P(
            id='uploaded-file-name',
            className='text-gray-600',
        ),
        html.Button(
            id='btn-close-uploaded-file', children=html.I(className='bi bi-x text-xl'), n_clicks=0,
            className='btn btn-circle btn-outline btn-sm btn-error'
        )
    ],
        id='uploaded-file',
        className='flex flex-row w-full gap-3 justify-between items-center bg-gray-200 p-3 rounded-lg mt-5',
        style={'visibility': 'hidden', 'display': 'none'}
    )