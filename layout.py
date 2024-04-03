from dash import dcc, html
from dash.dependencies import Input, Output


initial_projects = ['Project A']

def app_layout():
    layout = html.Div([
        html.Div([
            html.Img(src="https://querri.com/hubfs/Querri%20Logo.svg", 
            style={
                'width': '80%', 
                'display': 'block', 
                'margin': '20px auto'
                }),
            dcc.Dropdown(
                options=[{'label': project, 'value': project} for project in initial_projects],
                value=initial_projects[0],
                id='project-dropdown',
                searchable=False,
                clearable=False
            ),
            
        ], style={
            'position': 'fixed', 
            'top': '0', 
            'left': '0', 
            'bottom': '0', 
            'backgroundColor': '#1D2025', 
            'color': 'black', 
            'padding': '20px',
            'textAlign': 'center',
            'width': '250px',
            'height': '100vh',
            }),

        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Button('Select Files', className='btn-primary', 
                                style={'color': 'white', 
                                       'fontSize': '20px', 
                                       'backgroundColor': '#1D2025', 
                                       'border': 'none', 
                                       'padding': '10px 20px', 
                                       'borderRadius': '5px', 
                                       'outline': 'none', 
                                       'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.2)'
                                    }), 
                    html.P('Or Drag and Drop Anywhere', style={'color': 'white', 'fontSize': '20px'}),
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'backgroundColor': 'white',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '15px',
                    'cursor': 'pointer',
                },
                multiple=True
            ),
            html.Div(id='output-data-upload', 
                    style={
                        'margin': '20px',
                        'padding': '20px',  # Add padding
                        'overflowX': 'auto',
                        'maxHeight': '700px',
                        'overflowY': 'auto',
                        'fontSize': '14px',
                        'width': '1000px'
                    }),
        ]),

        html.Div([
            dcc.Input(
                id='user-input',
                placeholder='How can Querri help you today?',                    
                style={
                    'fontSize': '18px',
                    'width': 'calc(100% - 290px)',
                    'height': '70px',
                    'borderRadius': '25px', 
                    'paddingLeft': '20px', 
                    'border': '1px solid #ccc', 
                    'outline': 'none', 
                    'margin': '20px auto 0 auto', 
                    'display': 'block', 
                    'boxSizing': 'border-box', 
                    'position': 'absolute', 
                    'bottom': '20px', 
                    'left': '50%', 
                    'transform': 'translateX(-50%)',
                    'lineHeight': '60px', 
                    'zIndex': 1
                }
            ),
            html.Img(
                src = 'assets/enter_arrow.png',
                id='submit-button',
                n_clicks=0,
                style={
                    'height': '60px', 
                    'width': '60px', 
                    'borderRadius': '25px', 
                    'cursor': 'pointer', 
                    'position': 'absolute', 
                    'right': '144px', 
                    'bottom': '20px',
                    'display': 'flex',
                    'alignItems': 'center', 
                    'zIndex': 1
                }
            )
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
        
        dcc.Loading(id="loading", children=[
            #Graph Styling
            html.Div(id='output-plots', style={
                'marginTop': '50px',
                'marginBottom': '100px',
                'zIndex': 0,
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))',
                'gridGap': '20px',
                'maxWidth': '1200px',
                'margin': '0 auto',
                'padding': '20px'
            })
        ]),
    ], style={
        'display': 'flex', 
        'flexDirection': 'column',
        'fontFamily': 'Open Sans, sans-serif',
        'alignItems': 'center', 
        'position': 'fixed',
        'top': '0',
        'bottom': '0',
        'left': '292px', 
        'right': '0', 
        'backgroundColor': '#394349',
        'minHeight': '100vh',
    })

    return layout