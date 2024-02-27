import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from openai import OpenAI
import pandas as pd
import plotly.express as px

# Reading in our csv
school = pd.read_csv('data\student_math_clean.csv')

# Creating the Dash application
app = dash.Dash(__name__)

# API Key
openai_client = OpenAI(api_key='API_KEY_HERE')

# Layout
app.layout = html.Div([
    html.H1("Querri - The OpenAI Chatbot"),
    
    # Input for user
    dcc.Input(id='user-input', type='text', placeholder='What would you like Querri to do? '),
    
    # Button to submit
    html.Button('Submit', id='submit-button', n_clicks=0),
    
    # Output to display model response
    html.Div(id='output-message'),
])

# Define callback to handle button click
@app.callback(
    Output('output-message', 'children'),
    Input('submit-button', 'n_clicks'),
    State('user-input', 'value')
)
def generate_response(n_clicks, user_input):
    if n_clicks > 0:
        user_message = {"role": "user", "content": user_input}

        completion_response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[user_message],
        )

        model_response = completion_response.choices[0].message.content

        return html.Div([
            html.H4("Model Response:"),
            html.P(model_response)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
