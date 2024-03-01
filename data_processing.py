import pandas as pd
import plotly.express as px

studentCsv = 'data/student_math_clean.csv'

def genderVsFinal():
    df = pd.read_csv(studentCsv)
    # Convert Matplotlib plotting to Plotly here
    genderAvgFinalGrade = df.groupby('sex')['final_grade'].mean().reset_index()
    fig = px.bar(genderAvgFinalGrade, x='sex', y='final_grade')
    fig.update_layout(title='Final Grade by Gender')
    fig.update_xaxes(title='Gender')
    fig.update_yaxes(title='Final Grade')
    return fig

def add_new_project(n_clicks, new_project_name, current_options):
    if n_clicks > 0 and new_project_name:
        new_project_option = {'label': new_project_name, 'value': new_project_name}
        updated_options = current_options + [new_project_option]
        return updated_options
    return current_options


def schoolSupportVsFamilySupport(studentCsv):
    df = pd.read_csv(studentCsv)
    
    # Assuming 'school_support' is a column indicating whether students received school support.
    # If you also have a 'family_support' column and want to compare, you'd need to adjust the DataFrame grouping/aggregation accordingly.
    supportAvg = df.groupby('school_support')['final_grade'].mean().reset_index()

    # Create a bar chart using Plotly Express
    fig = px.bar(supportAvg, x='school_support', y='final_grade',
                 title='School Support vs. Average Final Grade',
                 labels={'school_support': 'School Support', 'final_grade': 'Average Final Grade'},
                 color='school_support',  # This will color bars differently based on 'school_support' value
                 barmode='group')  # Use 'group' for grouped bar chart, remove or set to 'stack' for stacked

    # Optionally, customize the layout further
    fig.update_layout(xaxis_title='School Support', yaxis_title='Average Final Grade')
    return fig
    

def weekdayAlcoholVsWeekendAlcohol(studentCsv):
    df = pd.read_csv(studentCsv)
    
    # Assuming 'weekday_alcohol' is a column indicating levels of alcohol consumption during weekdays
    alcohol_avg = df.groupby('weekday_alcohol')['final_grade'].mean().reset_index()

    # Create a bar chart using Plotly Express
    fig = px.bar(alcohol_avg, x='weekday_alcohol', y='final_grade',
                 title='Weekday Alcohol Consumption vs. Average Final Grade',
                 labels={'weekday_alcohol': 'Weekday Alcohol Consumption', 'final_grade': 'Average Final Grade'},
                 color='weekday_alcohol',  # This will color bars differently based on 'weekday_alcohol' value
                 barmode='group')  # Use 'group' for grouped bar chart, remove or set to 'stack' for stacked

    # Optionally, customize the layout further
    fig.update_layout(xaxis_title='Weekday Alcohol Consumption', yaxis_title='Average Final Grade')
    return fig
    

def freetimeVsSocial(studentCsv):
    df = pd.read_csv(studentCsv)
    
    # Create a scatter plot using Plotly Express
    fig = px.scatter(df, x='free_time', y='social', 
                     title='Free Time vs. Social Activity',
                     labels={'free_time': 'Free Time', 'social': 'Social Activity'},
                     hover_data=['free_time', 'social'])  # Customize hover data if needed

    # Optionally, customize the layout further
    fig.update_layout(xaxis_title='Free Time', yaxis_title='Social Activity')
    return fig


def firstGradeVsFinal(studentCsv):
    df = pd.read_csv(studentCsv)
    
    # Create a scatter plot using Plotly Express
    fig = px.scatter(df, x='grade_1', y='final_grade', 
                     title='First Grade vs. Final Grade',
                     labels={'grade_1': 'First Grade', 'final_grade': 'Final Grade'},
                     hover_data=['grade_1', 'final_grade'])  # Customize hover data if needed

    # Optionally, customize the layout further
    fig.update_layout(xaxis_title='First Grade', yaxis_title='Final Grade')
    return fig

# Additional Functions

def schoolDistribution(studentCsv):
    df = pd.read_csv(studentCsv)
    
    # Convert school counts to a DataFrame for better compatibility with Plotly Express
    school_counts = df['school'].value_counts().reset_index()
    school_counts.columns = ['School', 'Number of Students']
    
    # Create a bar chart using Plotly Express
    fig = px.bar(school_counts, x='School', y='Number of Students', 
                 title='Distribution of Students by School',
                 color='School',  # Optional: color bars by school
                 color_discrete_sequence=['skyblue', 'lightcoral'])  # Custom colors

    return fig

def ageDistribution(studentCsv):
    df = pd.read_csv(studentCsv)
    fig = px.histogram(df, x='age', nbins=15, title='Age Distribution of Students')
    fig.update_xaxes(title='Age')
    fig.update_yaxes(title='Number of Students')
    return fig

def internetAccessDistribution(studentCsv):
    df = pd.read_csv(studentCsv)
    
    # Convert internet access counts to a DataFrame for Plotly Express compatibility
    internet_counts = df['internet_access'].value_counts().reset_index()
    internet_counts.columns = ['Internet Access', 'Number of Students']
    
    # Create a pie chart using Plotly Express
    fig = px.pie(internet_counts, names='Internet Access', values='Number of Students',
                 title='Internet Access of Students',
                 color='Internet Access',  # Optional: color segments by internet access
                 color_discrete_sequence=['lightblue', 'lightcoral'])  # Custom colors

    # Optionally, customize the layout further
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(showlegend=True)

    return fig

def familyRomanticRelationship(studentCsv):
    df = pd.read_csv(studentCsv)
    
    # Preparing data for stacked bar chart visualization
    relationship_df = df.groupby(['family_relationship', 'romantic_relationship']).size().reset_index(name='Number of Students')
    
    # Create a stacked bar chart using Plotly Express
    fig = px.bar(relationship_df, x='family_relationship', y='Number of Students',
                 color='romantic_relationship',  # This will create stacks for romantic_relationship within each family_relationship bar
                 title='Family Relationship vs. Romantic Relationship',
                 labels={'family_relationship': 'Family Relationship', 'romantic_relationship': 'Romantic Relationship', 'Number of Students': 'Number of Students'},
                 color_discrete_sequence=['lightgreen', 'lightcoral'])  # Custom colors

    # Optionally, customize the layout further
    fig.update_layout(xaxis_title='Family Relationship', yaxis_title='Number of Students', barmode='stack')
    return fig

