import datetime
import os
import re
import ast
import matplotlib
matplotlib.use('TkAgg') # interactive display
import pandas as pd
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table
import base64
import io



# Define the extract_steps function to parse the model response
def extract_message(response): 
    # Define regular expression pattern to match the message format
    pattern = r'What this code does:(.*?)\d+\.'

    # Extract the message using regular expression
    match = re.search(pattern, response, re.DOTALL) 

    if match:
        message = match.group(1).strip() 
        return message
    else:
        return "Message not found in response."

# The big code cleaning function
def clean_code_string(code_string):
    # Trim leading and trailing whitespace to simplify detection
    trimmed_string = code_string.strip()

    # Attempt to remove any non printable or otherwise invalid characters. This pattern keeps:
    #   - \x20-\x7E: The range of printable ASCII characters.
    #   - \xA0-\uFFFF: The range of printable characters in the UTF-8 character set.
    #   - \t: Horizontal tab.
    #   - \n: Newline.
    trimmed_string = re.sub(r'[^\x20-\x7E\xA0-\uFFFF\t\n]', '', trimmed_string)

    # Initialize cleaned_code with None to check later if we've extracted any code
    cleaned_code = None

    # 1. Check for full backtick blocks (```code```) and extract
    # This regex accounts for optional language specifiers, like ```python
    full_backtick_match = re.search(r'```(?:[a-zA-Z]+\s)?([\s\S]+?)```', trimmed_string)
    if full_backtick_match:
        cleaned_code = full_backtick_match.group(1)

    # 2. If no full backtick block is found, check for leading backticks (```code)
    # This also handles potential language specifiers after the backticks
    if cleaned_code is None:
        leading_backtick_match = re.match(r'```(?:[a-zA-Z]+\s)?([\s\S]+)', trimmed_string)
        if leading_backtick_match:
            cleaned_code = leading_backtick_match.group(1)

    # 3. Check for trailing backticks (code```) and extract if no leading or full backtick was found
    if cleaned_code is None:
        trailing_backtick_match = re.match(r'([\s\S]+)```', trimmed_string)
        if trailing_backtick_match:
            cleaned_code = trailing_backtick_match.group(1)

    # 4. Check for code wrapped in quotes and extract if no variations of backticks were found
    if cleaned_code is None:
        quote_match = re.fullmatch(r'^[\'"]([\s\S]+)[\'"]$', trimmed_string)
        if quote_match:
            cleaned_code = quote_match.group(1)

    # If no patterns matched, consider the trimmed string as the code.
    if cleaned_code is None:
        cleaned_code = trimmed_string

    # Remove any remaining leading/trailing whitespace
    cleaned_code = cleaned_code.strip()

    # Syntax validation (optional but recommended)
    try:
        ast.parse(cleaned_code) 

        # Printing the parsed code in order to see what we are getting from the AI
        print(cleaned_code)

    except SyntaxError as e:
        print(f"Code cleanup failed. Extracted code block is not valid Python syntax. Error: {e}")
        return None  # or handle as appropriate for your application

    return cleaned_code


def load_and_inspect_csv(file_path):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        studytime_mapping = {
            '0 to 2 hours': 1.0,
            '2 to 5 hours': 3.5,
            '5 to 10 hours': 7.5,
            '10 or more hours': 10.0
        }
        df['studytime'] = df['studytime'].map(studytime_mapping)
        
        print("\nData inspection completed.")
        
    except Exception as e:
        print(f"Error loading or inspecting the CSV file: {e}")

df = None

def register_callbacks(app, openai_client): 
    @app.callback(
        Output('output-plots', 'children', allow_duplicate=True),
        [Input('submit-button', 'n_clicks')],
        [State('user-input', 'value'), State('project-dropdown', 'value')]
    )

    def generate_response(n_clicks, user_input, selected_project):
        global df

        if n_clicks > 0:
            # Append the desired string to the user input
            user_input = f"""{user_input}
                Please generate Python code that creates three different types
                of graphs (scatter plot, bar chart, and line chart) using Plotly.
                Assume that a DataFrame named 'df' is already available, 
                containing the necessary data for plotting. Ensure that the code
                is executable and does not rely on plt.show() to display the graphs.
                    DataFrame 'df' structure:
                        - student_id: A unique identifier assigned to each student.
                        - school: Indicates the school the student attends, such as "GP".
                        - sex: Represents the gender of the student, either "F" for female or "M" for male.
                        - age: Denotes the age of the student in years.
                        - address_type: Describes the type of address the student resides in, categorized as "Urban" or "Rural".
                        - family_size: Indicates the size of the student's family.
                        - parent_status: Describes the living arrangement of the student's parents, such as "Living together" or "Apart".
                        - mother_education: Represents the educational level attained by the student's mother.
                        - father_education: Represents the educational level attained by the student's father.
                        - mother_job: Indicates the occupation of the student's mother.
                        - father_job: Indicates the occupation of the student's father.
                        - school_choice_reason: Describes the reason behind the student's choice of school or educational institution.
                        - guardian: Indicates the guardian responsible for the student's welfare.
                        - travel_time: Represents the time taken by the student to travel to school, categorized into time intervals.
                        - class_failures: Indicates the number of past class failures experienced by the student.
                        - school_support: Indicates whether the school provides additional support to the student.
                        - family_support: Indicates whether the student receives support from their family.
                        - extra_paid_classes: Indicates whether the student participates in extra paid classes.
                        - activities: Indicates whether the student participates in extracurricular activities.
                        - nursery_school: Indicates whether the student attended nursery school.
                        - higher_ed: Indicates the student's aspiration for higher education.
                        - internet_access: Indicates whether the student has access to the internet.
                        - romantic_relationship: Indicates whether the student is involved in a romantic relationship.
                        - family_relationship: Represents the quality of relationships within the student's family.
                        - free_time: Indicates the amount of free time the student has after school.
                        - social: Represents the student's level of social interaction with peers.
                        - weekday_alcohol: Indicates the level of alcohol consumption by the student on weekdays.
                        - weekend_alcohol: Indicates the level of alcohol consumption by the student on weekends.
                        - health: Indicates the self-reported health status of the student.
                        - absences: Indicates the number of absences recorded for the student.
                        - grade_1: Represents the student's grade or performance in a certain subject or assessment.
                        - grade_2: Represents another grade or performance measure for the student.
                        - final_grade: Represents the final grade or overall performance of the student.

                    Your generated code should include:
                        1. Function definitions for generating each type of graph.
                        2. Incorporation of the DataFrame 'df' into each function
                           as a parameter.
                        3. Do not use df.show()/fig.show() to display the graphs, as these
                           will be used in a dashboard.
                        4. Descriptions of what the code is doing.
                        5. You must make sure that your code is writen in valid
                           python syntax.
                        6. Check to see if columns are numerical or not.
                        7. Your code is in valid python syntax. 
                        8. Make sure to execute the functions at the end so the graphs will display.
                        9. Make sure to only pass 'df' as a parameter.
            """

            # print(user_input)

            user_message = {"role": "user", "content": user_input}

            completion_response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[user_message],
            )
            model_response = completion_response.choices[0].message.content

            # extract the code to run from this response
            extracted_code = model_response

            # Printing the steps 
            message = extract_message(extracted_code)
            print(message) 

            # clean the code 
            cleaned_code = clean_code_string(extracted_code) 

            if cleaned_code is None: 
                raise PreventUpdate # Don't update the app if the code cleanup fails  

            # run the cleaned code using the exec function
            exec_global = {'df': df}
            try: 
                exec(cleaned_code, exec_global) 
            except Exception as e:
                print(f"Error in execution: {e}")
                raise PreventUpdate

            # use the outputs of the executed code to update the app
            # Check if any plot functions are defined
            plot_functions = {name: func for name, func in exec_global.items() if callable(func)}

            if not plot_functions:
                raise PreventUpdate
            
            # Generate Plots
            plot_figures = []
            for name, plot_function in plot_functions.items():
                try:
                    # Call the plot function with the global df
                    plot_figure = plot_function(df)
                    graph_id = f'plot-{name}'
                    app.layout.children.append(dcc.Graph(id=graph_id, figure=plot_figure))
                    plot_figures.append(html.Div([
                        html.H4(f"Here is your plot for {name}: "),
                        dcc.Graph(id=graph_id)  # Embed the plot as dcc.Graph
                ]))
                except Exception as e:
                    print(f"Error generating plot: {e}")
                    continue

            return plot_figures

    def add_new_project(n_clicks, new_project_name, current_options):
        if n_clicks > 0 and new_project_name:
            new_project_option = {'label': new_project_name, 'value': new_project_name}
            updated_options = current_options + [new_project_option]
            return updated_options
        return current_options
    
    #parse_contents function. Maybe it doesn't belong in this file but I'm just trying to get it to work. 
    def parse_contents(contents, filename, data):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                global df
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
            
        '''    
        return html.Div([
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                style_table={
                    'overflowX': 'auto',  # Horizontal scroll
                    'border': '1px solid #e0e0e0',  # Add border
                    'borderRadius': '5px',  # Add rounded corners
                    'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.05)',  # Add shadow
                    'fontFamily': 'Arial, sans-serif',  # Change font
                },
                style_header={
                    'backgroundColor': '#f2f2f2',  # Header background color
                    'fontWeight': 'bold',  # Header font weight
                },
                style_cell={
                    'textAlign': 'left',  # Cell text alignment
                    'fontFamily': 'Arial, sans-serif',  # Change font
                    'padding': '8px',  # Add padding
                },
                # Add more styling as needed
            ),
            html.Hr(),
        ], style={'margin': '20px'})  # Add margin around the div
            '''
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified') 
    )
    def update_output(list_of_contents, list_of_names, list_of_dates): # i think the new parameters will be: (contents, filename)
        if list_of_contents is not None:         
            global df                      
            children = [                                               
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)
            ]
            return children

    #callback for loading component:
    @app.callback(
        Output('output-plots', 'children'),
        Input('submit-button', 'n_clicks'),
        State('user-input', 'value'),
    )
    def update_output_plots(n_clicks, input_value):
        if not n_clicks:
            raise PreventUpdate
        return html.Div([
            html.H4(f"Processing Complete"),
            html.P(f"Received input: {input_value}"),
            ]) 