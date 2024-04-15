# IMPORTS
import datetime
import os
import re
import ast
import base64
import io
import pandas as pd
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dash import html, dcc, dash_table


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
            user_input = f"""I want you to generate a set of plotly graphs based on the user's request. 
                             In this input, the variable 'df' will be provided. That is the data you 
                             will use to generate the graphs. The user request is as follows:
                {user_input} 
                Generate Python code that creates different types
                of graphs (scatter plot, bar chart, and line chart for example) using Plotly.
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
                        10. Make sure to color the graphs are complimentary and have good looks for the dashboard. 
                        11. Make sure to have a descriptive title for the graphs.

                Here is some examples of python code that I wrote in order to help generate your response,
                keep in mind that these are only examples: 
                
                    import plotly.graph_objects as go
                        def scatter_plot(df):
                            '''
                            Generates a scatter plot using the first two numerical columns of the DataFrame.
                            
                            Args:
                            df (DataFrame): Input DataFrame
                            
                            Returns:
                            fig (plotly.graph_objs.Figure): Scatter plot figure
                            '''
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            if len(numeric_cols) < 2:
                                raise ValueError("DataFrame must contain at least two numerical columns for a scatter plot.")
                            
                            fig = go.Figure(data=go.Scatter(x=df[numeric_cols[0]], y=df[numeric_cols[1]], mode='markers'))
                            fig.update_layout(title='Scatter Plot', xaxis_title=numeric_cols[0], yaxis_title=numeric_cols[1])
                            return fig

                        def bar_chart(df):
                            '''
                            Generates a bar chart using the first numerical column of the DataFrame.
                            
                            Args:
                            df (DataFrame): Input DataFrame
                            
                            Returns:
                            fig (plotly.graph_objs.Figure): Bar chart figure
                            '''
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            if len(numeric_cols) < 1:
                                raise ValueError("DataFrame must contain at least one numerical column for a bar chart.")
                            
                            fig = go.Figure(data=go.Bar(x=df[numeric_cols[0]], y=df.index))
                            fig.update_layout(title='Bar Chart', xaxis_title=numeric_cols[0], yaxis_title='Index')
                            return fig

                        def line_chart(df):
                            '''
                            Generates a line chart using all numerical columns of the DataFrame.
                            
                            Args:
                            df (DataFrame): Input DataFrame
                            
                            Returns:
                            fig (plotly.graph_objs.Figure): Line chart figure
                            '''
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            if len(numeric_cols) == 0:
                                raise ValueError("DataFrame must contain at least one numerical column for a line chart.")
                            
                            fig = go.Figure()
                            for col in numeric_cols:
                                fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
                            fig.update_layout(title='Line Chart', xaxis_title='Index', yaxis_title='Values')
                            return fig

                Please ensure that the graph effectively represents something of meaning revolving around the data frame.
                Along with this make sure that you are importing all of the neccessary packages as the code provided is just an example. 
                remember that 'df' is a DataFrame that is supplied by the user. It is what is used to generate the graphs.
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

                    # Style the graph
                    plot_figure.update_layout(
                        plot_bgcolor='#2d2d2d',  # Dark gray background
                        paper_bgcolor='#333333',  # Slightly lighter background
                        font=dict(
                            family='Arial',  # font
                            size=14,
                            color='#d9d9d9'  # Light gray font color
                        ),
                        title=dict(
                            text=f'Graph {name}',
                            x=0.5,
                            font=dict(
                                family='Arial',
                                size=18,
                                color='#ffffff'  # White title color
                            )
                        ),
                        margin=dict(l=60, r=60, t=60, b=60),
                        xaxis=dict(
                            gridcolor='#555555',  # Subtle grid line color
                            gridwidth=0.5
                        ),
                        yaxis=dict(
                            gridcolor='#555555',
                            gridwidth=0.5
                        )
                    )

                    # Additional styling for specific plot types
                    # Not working I dont think
                    if isinstance(plot_figure, go.Scatter):
                        plot_figure.update_traces(marker=dict(color='#ff8c00'))  # Orange marker color for scatter plots

                    elif isinstance(plot_figure, go.Bar):
                        plot_figure.update_traces(marker=dict(color='#5599ff'))  # Light blue bar color for bar charts

                    # add style for other types of charts (Histogram, Pie, Heatmap, Box plot, Violin, ...., ect.)

                    # Wrap the styled plot figure in a styled container
                    plot_figures.append(
                        html.Div(style={
                            'backgroundColor': '#2d2d2d',
                            'padding': '20px',
                            'borderRadius': '5px',
                            'boxShadow': '0 0 10px rgba(0, 0, 0, 0.3)'
                    }, children=[
                        html.H4(f"Graph {name}", style={
                            'color': '#ffffff',
                            'marginBottom': '10px'
                        }),
                        dcc.Graph(figure=plot_figure, style={
                            'width': '100%',
                            'height': '400px',
                            'backgroundColor': '#333333',
                            'color': '#d9d9d9'
                        })
                    ]))
                except Exception as e:
                    print(f"Error generating plot: {e}")
                    continue

            return plot_figures
        
    @app.callback(
        Output('output-plots', 'children', allow_duplicate=True),
        [Input('generate-response', 'data')]
    )
    def update_plots(plot_figures):
        if plot_figures is None:
            return []
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
            
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified') 
    )
    def update_output(list_of_contents, list_of_names, list_of_dates):
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
    
    # Callback to display DataFrame when user types prompt
    @app.callback(
        Output('output-data-upload', 'children', allow_duplicate=True),
        Input('user-input', 'value')
    )

    def display_dataframe_while_typing(user_input):
        if df is not None and user_input:
            return html.Div([
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
                    style_table={
                        'overflowX': 'auto',  # Horizontal scroll
                        'border': '1px solid #e0e0e0',  # Add border
                        'borderRadius': '5px',  # Add rounded corners
                        'boxShadow': '0 4px 8px 0 rgba(0,0,0,0.05)',  # Add shadow
                        'fontFamily': 'Arial, sans-serif',
                    },
                    style_header={
                        'backgroundColor': '#f2f2f2',  # Header background color
                        'fontWeight': 'bold',
                    },
                    style_cell={
                        'textAlign': 'left',  # Cell text alignment
                        'fontFamily': 'Arial, sans-serif',
                        'padding': '8px',
                    },
                    # Add more styling as needed
                ),
                html.Hr(),
            ], style={'margin': '20px'})  # Add margin around the div
        else:
            return None

    # Callback to clear DataFrame when user clicks submit
    @app.callback(
        Output('output-data-upload', 'children', allow_duplicate=True),
        [Input('submit-button', 'n_clicks')]
    )
    def clear_dataframe_on_submit(n_clicks):
        if n_clicks:
            return None
        else:
            raise PreventUpdate
        

    