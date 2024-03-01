from dash import dcc, html

initial_projects = ['Project A']

def app_layout():
    layout = html.Div([
        html.Div([
        html.H1("Projects"),
        dcc.Dropdown(
            id='project-dropdown',
            options=[{'label': project, 'value': project} for project in initial_projects],
            value=initial_projects[0]
        ),
        html.Button('Add Project', id='add-project-button', n_clicks=0),
        dcc.Input(id='new-project-input', type='text', placeholder='Enter new project name'),
        html.Button('Submit New Project', id='submit-new-project-button', n_clicks=0),
    ], style={'width': '20%', 'position': 'fixed', 'top': '0', 'left': '0', 'marginBottom': '20px'}),

    # Bottom section for chat box
    html.Div([
        dcc.Input(id='user-input', 
                  type='text', 
                  placeholder='How can Querri help you today? ', 
                  style={'width': '80%', 'height': '70px'}
                  ),

        # Button to submit chat
        html.Button('Submit', 
                    id='submit-button', 
                    n_clicks=0, 
                    style={'marginTop': '10px', 'height': '70px'}),

        # Output to display model response
        html.Div(id='output-message', style={'marginTop': '20px'}),
    ], style={'position': 'absolute', 'bottom': '0', 'left': '500px', 'width': '78%', 'backgroundColor': '#f8f9fa'}),
])

    return layout
