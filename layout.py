from dash import dcc, html

initial_projects = ['School Data']

def app_layout():
    sidebar_style = {
        'position': 'fixed', 
        'top': 0, 
        'left': 0, 
        'bottom': 0, 
        'backgroundColor': '#1D2025', 
        'color': 'black', 
        'padding': '20px',
        'textAlign': 'center',
        'width': '250px',
        'height': '100vh',
        'fontWeight': 'bold',
        'transition': 'all 0.3s',
    }

    content_style = {
        'minHeight': '100px',
        'border': '1px solid black',
        'marginTop': '50px',
        'marginBottom': '100px',
        'zIndex': 2,
        'display': 'grid',
        'gridTemplateColumns': '1fr 1fr 1fr',
        'gridGap': '20px',
        'margin': '0 auto',
        'padding': '20px'
    }

    upload_button_style = {
        'color': '#1D2025',
        'fontSize': '22px',
        'fontWeight': 'bold',
        'backgroundColor': 'lightgray',
        'border': 'none',
        'padding': '20px',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'outline': 'none',
        'textDecoration': 'underline'
    }

    upload_box_style = {
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'width': '100%',
        'height': '120px',
        'backgroundColor': 'lightgray',
        'opacity': '0.3',
        'lineHeight': '60px',
        'borderWidth': '1.5px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '15px',
        'cursor': 'pointer',
    }

    upload_data_style = {
        'margin': '20px',
        'padding': '20px',  
        'overflowX': 'auto',
        'maxHeight': '700px',
        'overflowY': 'auto',
        'fontSize': '14px',
        'width': '1000px'
    }

    input_style = {
        'fontSize': '20px',
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

    submit_button_style = {
        'height': '60px',
        'width': '60px',
        'borderRadius': '25px',
        'cursor': 'pointer',
        'position': 'absolute',
        'right': '155px',
        'bottom': '25px',
        'display': 'flex',
        'alignItems': 'center',
        'zIndex': 1
    }
    
    # upload_success_style = {
    # 'color': '#4CAF50',  
    # 'backgroundColor': '#dff0d8',  
    # 'fontSize': '16px',  
    # 'fontWeight': 'bold',
    # 'padding': '10px 20px',  
    # 'borderRadius': '5px',  
    # 'border': '1px solid #c3e6cb',  
    # 'boxShadow': '0 2px 4px rgba(0,0,0,0.2)',  
    # 'width': 'auto',  
    # 'margin': '10px auto',  
    # 'textAlign': 'center',  
    # 'display': 'block',  
    # }

    layout = html.Div([
        html.Div([
            html.Img(src="/assets/QuerriTransLogo.svg", style={'width': '100%', 'display': 'block', 'margin': '5px auto'}),
            dcc.Dropdown(
                options=[{'label': project, 'value': project} for project in initial_projects],
                value=initial_projects[0],
                id='project-dropdown',
                searchable=False,
                clearable=False
            ),
            html.Button('Create A New Dashboard', id='add-dashboard-button', n_clicks=0, style={'marginTop': '10px', 'fontWeight': 'bold', 'backgroundColor': '#white', 'textAlign': 'center', 'fontSize': '12px', 'borderRadius': '20px'}),
        ], style=sidebar_style),

        dcc.Loading(id="loading", type='dot', color='orange', 
            children=[
            html.Div(id='output-plots', style=content_style, children='Placeholder for plots'),
            # html.Div(id='output-statistics', style=content_style, children='Placeholder for statistics'),
            # html.Div(id='output-info', style=content_style, children='Placeholder for additional information'),
        ]),

        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Button('Select Files', className='btn-primary', style=upload_button_style), 
                    html.P('Or Drag and Drop', style={'color': '#1D2025', 'fontSize': '20px'}),
                ], style={'display': 'flex', 'justifyContent': 'column', 'alignItems': 'center', 'padding': '20px', 'cursor': 'pointer'}),
                style=upload_box_style,
                multiple=True
            ),            
            html.Div(id='output-data-upload', style=upload_data_style),
            html.Div(id='upload-success-message', children=""),
        ]),


        html.Div([
            dcc.Input(id='user-input', placeholder='How can Querri help you today?', style=input_style),
            html.Img(src='assets/Q.svg', id='submit-button', n_clicks=0, style=submit_button_style)
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'fontFamily': 'Open Sans, sans-serif',
        'alignItems': 'center',
        'position': 'fixed',
        'top': 0,
        'bottom': 0,
        'left': '292px',
        'right': 0,
        'backgroundColor': '#394349',
        'minHeight': '100vh',
    })

    return layout
