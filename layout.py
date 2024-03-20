from dash import dcc, html

initial_projects = ['Project A']

def app_layout():
    layout = html.Div([
        html.Div([
            # Querri Logo, replaced the "Projects" text at the top
            html.Img(src="https://querri.com/hubfs/Querri%20Logo.svg", 
            style={
                'width': '80%', 
                'display': 'block', 
                'margin': '20px auto'
                }),
            # Project selection dropdown
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
            'backgroundColor': '#2D3339', 
            'color': 'black', 
            'padding': '20px',
            'textAlign': 'center',
            'width': '250px'  # Adjust the width to match the darker grey container
            }),

        # Bottom section for chat box
        html.Div([
            html.Div([
                dcc.Input(
                    id='user-input',
                    type='text',
                    placeholder='How can Querri help you today?',
                    style={
                        'width': 'calc(100% - 290px)',  # Adjust width to span from left edge to right edge
                        'height': '60px',
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
                        'transform': 'translateX(-50%)'
                    }
                ),
            ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}),

            # Submit Button
            html.Button(
                'Submit',
                id='submit-button',
                n_clicks=0,
                style={
                    'height': '60px', 
                    'width': '120px', 
                    'borderRadius': '25px', 
                    'backgroundColor': '#2D3339', 
                    'color': 'white', 
                    'border': 'none', 
                    'cursor': 'pointer', 
                    'position': 'absolute', 
                    'right': '144px', 
                    'bottom': '20px',
                }
            ),
            
            # Output to display model response
            html.Div(id='output-plots', style={'marginTop': '100px'})  # Chat response
        ], style={
            'display': 'flex', 
            'flexDirection': 'column',
            'alignItems': 'center', 
            'position': 'fixed', 
            'bottom': '0', 
            'left': '292px', #Adjust if you do not like the white gap on the left 
            'right': '0', 
            'backgroundColor': '#394349',
            'height': '1500px'
        }),

    ])

    return layout
