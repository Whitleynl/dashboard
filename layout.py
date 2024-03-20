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

            #Add Project Button
            #html.Button('Add Project', id='add-project-button', n_clicks=0),

            #New project input
            #dcc.Input(id='new-project-input', type='text', placeholder='Enter new project name'),

            #Submit Project Button
            #html.Button('Submit New Project', id='submit-new-project-button', n_clicks=0),
            
        ], style={
            'width': '15%', 
            'position': 'fixed', 
            'top': '0', 
            'left': '0', 
            'bottom': '0', 
            'overflowY': 'auto', 
            'backgroundColor': '#2D3339', 
            'color': 'white', 
            'padding': '20px'
            }),

        # Bottom section for chat box
        html.Div([
            dcc.Input(
                id='user-input',
                type='text',
                placeholder='How can Querri help you today?',
                style={
                    'width': 'calc(120% - 40px)', 
                    'height': '60px', 
                    'borderRadius': '25px', 
                    'paddingLeft': '20px', 
                    'border': '1px solid #ccc', 
                    'outline': 'none', 
                    'margin': '20px auto 0 auto', 
                    'display': 'block', 
                    'boxSizing': 'border-box', 
                    'position': 'fixed', 
                    'bottom': '20px', 
                    'left': '50%', 
                    'transform': 'translateX(-50%)'
                    }
            ),

            # Output to display model response
            html.Div(id='output-plots', style={'marginTop': '20px'})  # Chat response
        ], style={
            'display': 'flex', 
            'alignItems': 'center', 
            'position': 'fixed', 
            'bottom': '0', 
            'left': '50%', 
            'transform': 'translateX(-50%)', 
            'width': '70%', 
            'maxWidth': '800px', 
            'backgroundColor': 'white'
            }),
    ])

    return layout
