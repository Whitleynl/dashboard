import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from layout import app_layout, about_layout  # Import your layout functions
from openai import OpenAI
import os
from callbacks import register_callbacks

# Initialize Dash app
app = dash.Dash(__name__, prevent_initial_callbacks=True, suppress_callback_exceptions=True) 

# Define main layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Retrieve API key from environment variable
OPENAI_API_KEY = os.getenv('API_KEY')

# Check if API key is set
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable.")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Register callbacks
register_callbacks(app, openai_client)

# Define callback to always show the about page initially
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    # Always return the about layout when the pathname is empty or "/"
    if not pathname or pathname == "/":
        return about_layout()  # Show the about page layout
    elif pathname == "/home":
            return app_layout()  # Show the main layout
    elif pathname == "/about":
        return about_layout()

if __name__ == '__main__':
    app.run_server(debug=False)
