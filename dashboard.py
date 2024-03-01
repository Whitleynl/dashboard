import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from openai import OpenAI
import os
import pandas as pd
import matplotlib.pyplot as plt

# Reading in the csv
studentCsv = 'data\student_math_clean.csv'

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
    
def genderVsFinal(studentCsv):
    # Bar Chart
    df = pd.read_csv(studentCsv)

    genderAvgFinalGrade = df.groupby('sex')['final_grade'].mean().reset_index()

    plt.figure(figsize=(8,6))
    plt.bar(genderAvgFinalGrade['sex'], genderAvgFinalGrade['final_grade'], color=['pink', 'blue'])
    plt.title('Gender vs. Average Final Grade')
    plt.xlabel('Gender')
    plt.ylabel('Average Final Grade')
    plt.show()

def schoolSupportvsFamilySupport(studentCsv):
    # Stacked Bar Chart
    df = pd.read_csv(studentCsv)

    supportAvg = df.groupby('school_support')['final_grade'].mean().reset_index()

    supportAvg.plot(x='school_support', kind='bar', stacked=True, figsize=(10, 6), color=['green', 'orange'])
    plt.title('School Support vs. Family Support')
    plt.xlabel('Support Type')
    plt.ylabel('Average Final Grade')
    plt.show()
    

def weekdayAlcoholVsWeekendAlcohol(studentCsv):
    # Boxplot
    df = pd.read_csv(studentCsv)

    alcohol_avg = df.groupby('weekday_alcohol')['final_grade'].mean().reset_index()

    alcohol_avg.plot(x='weekday_alcohol', kind='bar', figsize=(10, 6), color=['purple', 'yellow'])
    plt.title('Weekday Alcohol vs. Weekend Alcohol')
    plt.xlabel('Alcohol Consumption')
    plt.ylabel('Average Final Grade')
    plt.show()

def freetimeVsSocial(studentCsv):
    # Scatter Plot
    df = pd.read_csv(studentCsv)

    plt.figure(figsize=(8, 6))
    plt.scatter(df['free_time'], df['social'])
    plt.title('Free_time vs. Social Activity')
    plt.xlabel('Freetime')
    plt.ylabel('Social Activity')
    plt.show() 

def firstGradeVsFinal(studentCsv):
    # Scatter Plot
    df = pd.read_csv(studentCsv)

    plt.figure(figsize=(8, 6))
    plt.scatter(df['grade_1'], df['final_grade'])
    plt.title('First Grade vs. Final Grade')
    plt.xlabel('First Grade')
    plt.ylabel('Final Grade')
    plt.show() 

# Additional Functions
def schoolDistribution(studentCsv):
    # School Distribution
    df = pd.read_csv(studentCsv)
    school_counts = df['school'].value_counts()
    plt.figure(figsize=(8, 6))
    school_counts.plot(kind='bar', color=['skyblue', 'lightcoral'])
    plt.title('Distribution of Students by School')
    plt.xlabel('School')
    plt.ylabel('Number of Students')
    plt.show()

def ageDistribution(studentCsv):
    # Age Distribution
    df = pd.read_csv(studentCsv)
    plt.figure(figsize=(8, 6))
    plt.hist(df['age'], bins=15, color='lightgreen', edgecolor='black')
    plt.title('Age Distribution of Students')
    plt.xlabel('Age')
    plt.ylabel('Number of Students')
    plt.show()

def internetAccessDistribution(studentCsv):
    # Internet Access
    df = pd.read_csv(studentCsv)
    internet_counts = df['internet_access'].value_counts()
    plt.figure(figsize=(8, 6))
    internet_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightcoral'])
    plt.title('Internet Access of Students')
    plt.ylabel('')
    plt.show()

def familyRomanticRelationship(studentCsv):
    # Family Relationship vs. Romantic Relationship
    df = pd.read_csv(studentCsv)
    relationship_counts = df.groupby(['family_relationship', 'romantic_relationship']).size().unstack()
    plt.figure(figsize=(10, 6))
    relationship_counts.plot(kind='bar', stacked=True, color=['lightgreen', 'lightcoral'])
    plt.title('Family Relationship vs. Romantic Relationship')
    plt.xlabel('Family Relationship')
    plt.ylabel('Number of Students')
    plt.show()


if __name__ == '__main__':
    app.run_server(debug=True)
