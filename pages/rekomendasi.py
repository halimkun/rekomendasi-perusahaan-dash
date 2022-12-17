import dash 
import base64, io
import pandas as pd
import plotly.express as px
import components.text as tc
import components.card as card

from dash import dash_table, dcc, html, ctx
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ALL
from components.uploaded_file import uploaded_file

dash.register_page(__name__, path='/rekomendasi', order=2)

# === TAB STYLE === #
tab_style = {'padding': '0px',}
tab_selected_style = {'padding': '0px','borderTop': '2px solid #65c3c8',}
# === END OF TAB STYLE === #

# === LAYOUT FOR THIS PAGE === #
def layout():
    return [
        html.Div([
            html.Div([
                card.rounded_full([
                    tc.text_4xl('Sistem Rekomendasi'),
                    tc.text_base(
                        'Sebelum melakukan perhitungan rekomendasi, diharuskan untuk mengupload dataset terlebih dahulu!'
                    ),

                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Upload Data Acuan'
                        ]),
                        accept='.csv, .xlsx, .xls',
                        multiple=False,
                        className='w-full h-16 border-2 border-dashed border-gray-400 rounded-lg flex justify-center items-center hover:bg-gray-100 hover:border-gray-500 duration-300 ease-in-out'
                    ),

                    uploaded_file(),
                ])
            ], className='w-full md:w-[30%]'),
            
            html.Div([
                dcc.Tabs(id="tab-menu", value='spoiler-data', children=[
                    dcc.Tab(
                        label='Spoiler Data', 
                        value='spoiler-data',
                        style=tab_style, selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        label='Rekomendasi', 
                        value='rekomendasi',
                        style=tab_style, selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        label='Mass Rekomendasi', 
                        value='mass-rekomendasi',
                        style=tab_style, selected_style=tab_selected_style
                    ),
                ], className='sm:text-sm font-medium text-center text-gray-500 border-0', parent_className='shadow-md'),
                dcc.Loading(children=[
                    html.Div(
                        id='tabs-content',
                    )
                ], id='loading-datasets', type='default')
            ], className='w-full md:w-[70%]'),
        
        ], className='flex flex-col md:flex-row w-full gap-5'),
        
        # store data and file name
        dcc.Store(id='store-data', storage_type='memory'),
        dcc.Store(id='store-filename', storage_type='memory'),
    ]
# === END OF LAYOUT === #


# === CALLBACKS TAB MENU === #
@dash.callback(
    Output('tabs-content', 'children'),
    
    Input('tab-menu', 'value'),
    Input('store-data', 'data'),
    Input('store-filename', 'data'),
)
def render_content(tab, data, dataname):
    if data is None :
        out = card.rounded_bottom([
            html.Div(className='alert alert-error shadow-lg', children=[
                html.Div(className='flex items-center', children=[
                    html.I(className='bi bi-x-circle text-lg mr-2'),
                    html.P('Data Masih Belum Diupload!')
                ])
            ])
        ])

    else:
        if tab == 'spoiler-data':
            status, dff = to_dataframe(data)

            fig = px.bar(dff[dff.columns[-1]].value_counts())
            fig.update_layout(showlegend=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(title_text='Jumlah Data')

            out = html.Div([
                card.rounded_bottom([
                    html.Div(className='mb-3', children=[
                        tc.text_xl('Spoiler Data'),
                        tc.text_base('Berikut adalah data yang telah diupload'),
                    ]),
                    build_datatable(data)
                ]),
                html.Div(className='mt-5', children=[
                    card.rounded_full([
                        html.Div(className='mb-3', children=[
                            tc.text_xl('Visualisasi Data'),
                            tc.text_base('Visualisasi jumlah data dari record data yang diupload'),
                        ]),
                        html.Div(className='mt-5', children=[
                            dcc.Graph(figure=fig)
                        ]),
                    ])
                ])
            ])
            
        elif tab == 'rekomendasi':
            out = html.Div([
                card.rounded_bottom([
                    html.Div([
                        html.Div(children="Rekomendasi")
                    ], className='w-full')
                ])
            ])
            
        elif tab == 'mass-rekomendasi':
            out = html.Div([
                card.rounded_bottom([
                    html.Div([
                        html.Div(children="Mass Rekomendasi")
                    ], className='w-full')
                ])
            ])
    
    return out
# === END OF CALLBACKS TAB MENU === #


# === CALLBACKS STORE DATA === #
@dash.callback(
    Output('store-data', 'data'),
    Output('store-filename', 'data'),
    
    Input('upload-data', 'contents'),
    
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),

    prevent_initial_call=True
)
def store_data(contents, filename, last_modified):
    if contents is None:
        raise PreventUpdate
    else:
        # convert content to dataframe
        status, data = to_dataframe(contents)
        return data.to_dict('records'), filename
        
# === END OF CALLBACKS STORE DATA === #

# === CALLBACKS UPLOADED FILE === #
# === SHOW UPLOADED FILE UNDER UPLOAD BUTTON === #
@dash.callback(
    Output('uploaded-file-name', 'children'),
    Output('uploaded-file', 'style'),

    Input('store-data', 'data'),
    Input('store-filename', 'data'),
    
    prevent_initial_call=True
)
def show_uploaded_file(data, filename):
    if data is None:
        structure = '', {'visibility': 'hidden', 'display': 'none'}
    else:
        structure = filename, {'visibility': 'visible', 'display': 'flex'}

    return structure
# === END OF CALLBACK UPLOADED FILE === #


# === CONVERT TO DATAFRAME === #
def to_dataframe(contents):
    if isinstance(contents, pd.DataFrame):
        status = True
        df = contents

    elif isinstance(contents, list):
        status = True
        df = pd.DataFrame(contents)
    
    elif isinstance(contents, str):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        try:
            if 'csv' in content_type:
                status = True
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8'))
                )
            elif 'xls' in content_type:
                status = True
                df = pd.read_excel(
                    io.BytesIO(decoded)
                )
            elif 'xlsx' in content_type:
                status = True
                df = pd.read_excel(
                    io.BytesIO(decoded)
                )

        except Exception as e:
            status = False
            df = pd.DataFrame()
            
            
    return status, df
# === END CONVERT TO DATAFRAME === #

# === BUILD DATATABLE === #
def build_datatable(data):
    if isinstance(data, pd.DataFrame):
        dff = data
    else:
        dff = pd.DataFrame(data)

    return html.Div(className='overflow-x-auto rounded-lg', children=[
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dff.columns],
            data=dff.to_dict('records'),
            page_size=10,
            style_table={
                'border': '1px solid #ddd',
                'borderCollapse': 'collapse',
                'borderSpacing': '0',
                'textAlign': 'left',
                'width': 'auto',
                'color': '#6B7280',
            },
            style_cell={
                'padding': '5px',
                'border': '1px solid #ddd',
                'textAlign': 'left',
                'fontFamily': 'sans-serif',
                'fontSize': '14px',
                'width': 'auto',
                "padding-top": "0.2rem",
                "padding-bottom": "0.2rem",
                "padding-left": "1rem",
                "padding-right": "1rem",
            },
            style_header={
                'color': '#1F2937',
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'padding': '20px',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                {
                    'if': {'column_id': dff.columns[0]},
                    'width': '50px !important',
                    'text-align': 'center',
                },
                {
                    'if': {'column_id': dff.columns[-1]},
                    'whiteSpace': 'nowrap',
                    'height': 'auto',
                },
            ],
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
        )
    ])
# === END OF BUILD DATATABLE === #