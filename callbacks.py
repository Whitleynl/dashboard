from dash.dependencies import Input, Output, State
from dash import html
from data_processing import genderVsFinal


def register_callbacks(app, openai_client):
    @app.callback(
        Output('output-message', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('user-input', 'value'), State('project-dropdown', 'value')]
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