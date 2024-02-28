import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from openai import OpenAI
import os



# Creating the Dash application
app = dash.Dash(__name__)

# Initial projects
initial_projects = ['Project A']

# Placeholder for your OpenAI API key
api_key = os.getenv('API_KEY')
openai_client = OpenAI(api_key=api_key)
# Layout
app.layout = html.Div([
    # Top section for projects
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
    ], style={'width': '20%', 'position': 'fixed', 'top': '0', 'left': '0', 'margin-bottom': '20px'}),

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
                    style={'margin-top': '10px', 'height': '70px'}),

        # Output to display model response
        html.Div(id='output-message', style={'margin-top': '20px'}),
    ], style={'position': 'absolute', 'bottom': '0', 'left': '500px', 'width': '78%', 'background-color': '#f8f9fa'}),
])

# Callback to add a new project to the dropdown
@app.callback(
    Output('project-dropdown', 'options'),
    Input('submit-new-project-button', 'n_clicks'),
    State('new-project-input', 'value'),
    State('project-dropdown', 'options')
)
def add_new_project(n_clicks, new_project_name, current_options):
    if n_clicks > 0 and new_project_name:
        new_project_option = {'label': new_project_name, 'value': new_project_name}
        updated_options = current_options + [new_project_option]
        return updated_options
    return current_options

# Callback to handle user input and get OpenAI response
@app.callback(
    Output('output-message', 'children'),
    Input('submit-button', 'n_clicks'),
    State('user-input', 'value'),
    Input('project-dropdown', 'value')
)
def generate_response(n_clicks, user_input, selected_project):
    if n_clicks > 0:
        user_message = {"role": "user", "content": user_input}

        completion_response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[user_message],
        )

        model_response = completion_response.choices[0].message.content

        return html.Div([
            html.H4(f"Model Response for {selected_project}:"),
            html.P(model_response)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
