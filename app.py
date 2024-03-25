import dash
from layout import app_layout
from openai import OpenAI
import os
from callbacks import register_callbacks


# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']) 
app.layout = app_layout()

# Retrieve API key from environment variable
OPENAI_API_KEY = os.getenv('API_KEY')

# Check if API key is set
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API key not found. Please set the 'OPENAI_API_KEY' environment variable.")

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Register callbacks
register_callbacks(app, openai_client) 

if __name__ == '__main__':
    app.run_server(debug=True)
