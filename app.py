import dash
from layout import app_layout
from openai import OpenAI
import os
from callbacks import register_callbacks


# Initialize Dash app
app = dash.Dash(__name__) 
app.layout = app_layout()

OPENAI_API_KEY = os.getenv('API_KEY')

openai_client = OpenAI(api_key=OPENAI_API_KEY)

student_csv_path = 'data/student_math_clean.csv'

# Register callbacks
register_callbacks(app, openai_client) 

if __name__ == '__main__':
    app.run_server(debug=True)
