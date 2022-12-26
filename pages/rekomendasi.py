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

from sklearn import tree
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, f1_score

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
                dcc.Tabs(id="tab-menu", value='mass-rekomendasi', children=[
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


# ==================== ==================== ==================== #
# ====================|      CALLBACK      |==================== #
# ==================== ==================== ==================== #

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
                    build_input_rekomendasi(data),
                ]), 
                html.Div(id='hasil-rekomendasi')
            ])
            
        elif tab == 'mass-rekomendasi':
            if isinstance(data, pd.DataFrame):
                dff = data

            else:
                status, dff = to_dataframe(data)

                if dff.columns[0].lower()  != 'no' or dff.columns[1].lower() != 'nama' :
                    out = card.rounded_bottom([
                        html.P(className='text-red-500 text-xl mb-1 capitalize', children="Terjadi kesalahan pada data yang diupload!"),
                        html.P(className='text-red-500 text-sm mb-1 capitalize', children="Pastikan data yang diupload sudah sesuai dengan format yang ditentukan!"),
                    ])

                else:
                    out = html.Div([
                        card.rounded_bottom([
                        html.Div([
                            tc.text_xl('Rekomendasi Masal'),
                            tc.text_base('Unggah file data baru anda yang akan dihitung untuk diberikan rekomendasi.'),
                        ], className='mb-5'),
                        
                        dcc.Upload(
                            id='upload-mass-data',
                            children=html.Div([
                                'Upload Data Baru'
                            ]),
                            accept='.csv, .xlsx, .xls',
                            multiple=False,
                            className='w-full h-16 border-2 border-dashed border-gray-400 rounded-lg flex justify-center items-center hover:bg-gray-100 hover:border-gray-500 duration-300 ease-in-out'
                        ),
                    ]),

                    html.Div(id='hasil-mass-rekomendasi', className='mt-5')
                ])
    
    return out
# === END OF CALLBACKS TAB MENU === #


# === CALLBACKS STORE DATA === #
@dash.callback(
    Output('store-data', 'data'),
    Output('store-filename', 'data'),
    Output('upload-data', 'contents'),
    Output('upload-data', 'filename'),

    Input('upload-data', 'contents'),
    Input('btn-close-uploaded-file', 'n_clicks'),
    
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),

    prevent_initial_call=True
)
def store_data(contents, n_clicks, filename, last_modified):
    if contents is None:
        raise PreventUpdate
    else:
       if ctx.triggered_id == 'upload-data':
            status, data = to_dataframe(contents)
            return data.to_dict('records'), filename, contents, filename
        
       else: 
            return None, None, None, None
        
# === END OF CALLBACKS STORE DATA === #
    

# === CALLBACK BUTTON REKOMENDASI === #
@dash.callback(
    Output('hasil-rekomendasi', 'children'),

    Input('btn-rekomendasi', 'n_clicks'),
    Input('store-data', 'data'),
    Input('store-filename', 'data'),

    State({'type': 'input-nilai', 'index': ALL}, 'value'), # list
    
    prevent_initial_call=True
)
def rekomendasi(n_clicks, data, filename, nilai):
    if n_clicks is None:
        raise PreventUpdate
    
    else:
        if data is None:
            hasil = card.rounded_bottom([
                html.Div(className='alert alert-error shadow-lg', children=[
                    html.Div(className='flex items-center', children=[
                        html.I(className='bi bi-x-circle text-lg mr-2'),
                        html.P('Data Masih Belum Diupload!')
                    ])
                ])
            ])
        
        else:
            # convert content to dataframe
            status, dff = to_dataframe(data)

            if status == False:
                hasil = card.rounded_bottom([
                    html.Div(className='alert alert-error shadow-lg', children=[
                        html.Div(className='flex items-center', children=[
                            html.I(className='bi bi-x-circle text-lg mr-2'),
                            html.P('Terjadi Kesanahan Pada Data Yang Diupload!')
                        ])
                    ])
                ])

            else :
                min_max_scaler = preprocessing.MinMaxScaler()
                model = tree.DecisionTreeClassifier(
                    criterion="gini", 
                    max_depth=3,
                    splitter="best"
                )

                df_nilai = dff.drop(dff.columns[:2], axis=1)
                df_nilai = df_nilai.drop(df_nilai.columns[-1], axis=1)
                
                X = min_max_scaler.fit_transform(df_nilai)
                y = dff[dff.columns[-1]]

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.3, random_state=2
                )

                model.fit(X, y)

                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)

                pred = model.predict([nilai])

                # get pred to html.pre
                hasil = [
                    html.Div([
                        card.rounded_full([
                            html.Div([
                                tc.text_xl('Hasil Rekomendasi'),
                                tc.text_base('Hasil rekomendasi untuk data yang diupload.'),
                            ], className='mb-5'),
                            
                            card.rounded_full([
                                html.Pre(pred)
                            ]),

                            html.Div(className='flex flex-wrap mt-3', children=[
                                html.Div(className='w-[49%]', children=[
                                    html.Div(className='flex items-center', children=[
                                        html.Pre(f'Akurasi : {acc * 100:.2f} %'),
                                    ]),
                                ]),
                                html.Div(className='w-[49%]', children=[
                                    html.Div(className='flex items-center', children=[
                                        html.Pre(f'Jumlah Data : {len(dff)}'),
                                    ]),
                                ]),
                                html.Div(className='w-[49%]', children=[
                                    html.Div(className='flex items-center', children=[
                                        html.Pre(f'Jumlah Data Uji : {len(X_test)}'),
                                    ]),
                                ]),
                                html.Div(className='w-[49%]', children=[
                                    html.Div(className='flex items-center', children=[
                                        html.Pre(f'Jumlah Data Latih {len(X_train)}'),
                                    ]),
                                ]),
                                
                            ]),
                        ]),
                    ], className='mt-5')
                ]

    
    return hasil
# === END OF CALLBACKS BUTTON REKOMENDASI === #

# === CALLBACK MASS REKOMENDASI === #
@dash.callback(
    Output('hasil-mass-rekomendasi', 'children'),

    Input('upload-mass-data', 'contents'),
    Input('upload-mass-data', 'filename'),
    Input('store-data', 'data'),
    Input('store-filename', 'data'),
    
    prevent_initial_call=True
)
def mass_rekomendasi(contents, filename, data, dataname):
    if data is None:
        hasil = card.rounded_bottom([
            html.Div(className='alert alert-error shadow-lg', children=[
                html.Div(className='flex items-center', children=[
                    html.I(className='bi bi-x-circle text-lg mr-2'),
                    html.P('Data Masih Belum Diupload!')
                ])
            ])
        ])

    else:
        status, databaru = to_dataframe(contents)
        namadatabaru = filename

        stts, dataset = to_dataframe(data)
        namadataset = dataname

        #########################################

        min_max_scaler = preprocessing.MinMaxScaler()
        model = tree.DecisionTreeClassifier(
            criterion="gini", 
            max_depth=3,
            splitter="best"
        )

        df_nilai = dataset.drop(dataset.columns[:2], axis=1)
        df_nilai = df_nilai.drop(df_nilai.columns[-1], axis=1)

        X = min_max_scaler.fit_transform(df_nilai)
        y = dataset[dataset.columns[-1]]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=2
        )

        model.fit(X, y)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        #########################################

        if status == False:
            hasil = card.rounded_bottom([
                html.Div(className='alert alert-error shadow-lg', children=[
                    html.Div(className='flex items-center', children=[
                        html.I(className='bi bi-x-circle text-lg mr-2'),
                        html.P('Terjadi Kesanahan Pada Data Yang Diupload!')
                    ])
                ])
            ])

        else:
            df = databaru.drop(databaru.columns[:2], axis=1)
            df = min_max_scaler.fit_transform(df)

            pred = model.predict(df)

            databaru['Rekomendasi'] = pred

            hasil = [
                html.Div([
                    card.rounded_full([
                        html.Div([
                            tc.text_xl('Hasil Rekomendasi'),
                            tc.text_base('Hasil rekomendasi untuk data yang diupload.'),
                        ], className='mb-5'),
                        
                        # databaru to html table
                        html.Div([
                            dash_table.DataTable(
                                id='table-mass-rekomendasi',
                                columns=[{"name": i, "id": i} for i in databaru.columns],
                                data=databaru.to_dict('records'),
                                style_table={
                                    'overflowX': 'auto',
                                    'overflowY': 'auto',
                                    'maxHeight': '300px',
                                    'maxWidth': '100%',
                                    'minWidth': '100%',
                                },
                                style_cell={
                                    'textAlign': 'center',
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'minWidth': '100px',
                                    'maxWidth': '100px',
                                    'width': '100px',
                                },
                                style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }
                                ],
                            ),
                        ], className='mb-5'),

                        # card.rounded_full([
                        #     html.Pre(pred)
                        # ]),

                        html.Div(className='flex flex-wrap mt-3', children=[
                            html.Div(className='w-[49%]', children=[
                                html.Div(className='flex items-center', children=[
                                    html.Pre(f'Akurasi : {acc * 100:.2f} %'),
                                ]),
                            ]),
                            html.Div(className='w-[49%]', children=[
                                html.Div(className='flex items-center', children=[
                                    html.Pre(f'Jumlah Data : {len(dataset)}'),
                                ]),
                            ]),
                            html.Div(className='w-[49%]', children=[
                                html.Div(className='flex items-center', children=[
                                    html.Pre(f'Jumlah Data Uji : {len(X_test)}'),
                                ]),
                            ]),
                            html.Div(className='w-[49%]', children=[
                                html.Div(className='flex items-center', children=[
                                    html.Pre(f'Jumlah Data Latih {len(X_train)}'),
                                ]),
                            ]),
                            
                        ]),
                    ]),
                ], className='mt-5')
            ]

    return hasil
# === END OF CALLBACKS MASS REKOMENDASI === #


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

# ==================== ==================== ==================== #
# ====================|     END CALLBACK   |==================== #
# ==================== ==================== ==================== #



# === REMOVE UNUSED COLUMN === #
def remove_unused_columns(data):
    if isinstance(data, pd.DataFrame):
        data.columns = data.columns.str.lower()
    else:
        data = pd.DataFrame(data)
        data.columns = data.columns.str.lower()
    
    
    if 'no' in data.columns and 'nama' in data.columns:
        status = True
        data = data.drop(['no', 'nama'], axis=1)
    else :
        status = False
        data = pd.DataFrame()

    return status, data
# === END REMOVE UNUSED COLUMN === #

# === REMOVE TARGET COLUMN === #
def remove_target_column(data):
    if isinstance(data, pd.DataFrame):
        data.columns = data.columns.str.lower()
    else:
        data = pd.DataFrame(data)
        data.columns = data.columns.str.lower()
    
    # if -1 column is categorical
    if data.iloc[:, -1].dtype == 'object':
        status = True
        data = data.drop(data.columns[-1], axis=1)
    else :
        status = False
        data = pd.DataFrame()
    
    return status, data
# === END REMOVE TARGET COLUMN === #

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

# === BUILD INPUT REKOMENDASI === #
def build_input_rekomendasi(data):
    false_data = html.Div([
        html.P(className='text-red-500 text-xl mb-1 capitalize', children="Terjadi kesalahan pada data yang diupload!"),
        html.P(className='text-red-500 text-sm mb-1 capitalize', children="Pastikan data yang diupload sudah sesuai dengan format yang ditentukan!"),
    ])

    if isinstance(data, pd.DataFrame):
        dff = data
    else:
        status, dff = to_dataframe(data)

        
    if status == False:
        return false_data
    else:
        status, dff = remove_unused_columns(dff)
        
        if status == False:
            return false_data
        else:
            status, dff = remove_target_column(dff)
            
            if status == False:
                return false_data
            else:
                return html.Div([
                    html.Div(className='flex flex-row flex-wrap', children=[
                        html.Div(className='w-[49%] mb-3 px-2', children=[
                            html.P(className='text-gray-500 text-xs mb-1 capitalize', children=i),
                            dcc.Input(
                                id={
                                    'type': 'input-nilai',
                                    'index': i.lower().replace(' ', '_')
                                },
                                type='number',
                                min=0, max=100,
                                value=0, step=1,
                                name=i,
                                className='input input-bordered w-full'
                            )
                        ]) for i in dff.columns
                    ]),

                    # button calculate
                    html.Button('Rekomendasikan', id='btn-rekomendasi', className='mx-2 mt-5 px-5 py-2 bg-primary text-white rounded-lg hover:bg-primary duration-300 ease-in-out'),
                ])
# === END OFBUILD INPUT REKOMENDASI === #


# === BUILD DATATABLE === #
def build_datatable(data):
    if isinstance(data, pd.DataFrame):
        dff = data
    else:
        status, dff = to_dataframe(data)

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