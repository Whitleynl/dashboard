import base64
import io
import re
import pandas as pd
from dash import dcc, html, Input, Output, State, dash_table, exceptions
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

# Initialized dataframe
df = None

# Function to extract messages from the model response
def extract_message(response):
    pattern = r'What this code does:(.*?)\d+\.'
    match = re.search(pattern, response, re.DOTALL)
    return match.group(1).strip() if match else "Message not found in response."

# Function to clean the extracted code string
def clean_code_string(code_string):
    code_string = code_string.strip()  # Trim whitespace
    # Remove invalid characters
    code_string = re.sub(r'[^\x20-\x7E\xA0-\uFFFF\t\n]', '', code_string)
    # Extract code using regex
    patterns = [
        r'```(?:[a-zA-Z]+\s)?([\s\S]+?)```',
        r'```(?:[a-zA-Z]+\s)?([\s\S]+)',
        r'([\s\S]+)```',
        r'^[\'"]([\s\S]+)[\'"]$'
    ]
    for pattern in patterns:
        match = re.search(pattern, code_string)
        if match:
            return match.group(1).strip()
    return code_string  # Return the code string if no pattern matches

# Function to load and inspect CSV files
def load_and_inspect_csv(file_path):
    global df
    try:
        df = pd.read_csv(file_path)
        studytime_mapping = {
            '0 to 2 hours': 1.0,
            '2 to 5 hours': 3.5,
            '5 to 10 hours': 7.5,
            '10 or more hours': 10.0
        }
        df['studytime'] = df['studytime'].map(studytime_mapping)
        print("Data inspection completed.")
    except Exception as e:
        print(f"Error loading or inspecting CSV file: {e}")

# Function to parse the contents of the uploaded file
def parse_contents(contents, filename):
    global df  # Make sure to use the global df variable
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Create a StringIO object from decoded content and load into df
            csv_stringio = io.StringIO(decoded.decode('utf-8'))
            df = pd.read_csv(csv_stringio)
            # Apply the mapping after loading the CSV into df
            studytime_mapping = {
                '0 to 2 hours': 1.0,
                '2 to 5 hours': 3.5,
                '5 to 10 hours': 7.5,
                '10 or more hours': 10.0
            }
            df['studytime'] = df['studytime'].map(studytime_mapping)
            print("DataFrame created and inspection completed.")
        elif 'xls' in filename:
            # For Excel files, read directly into df
            df = pd.read_excel(io.BytesIO(decoded))
        
        print(df.head())
        return html.Div([
            html.H5(filename),
            html.Div(id='upload-success-message', children="File processed successfully."),
            dash_table.DataTable(
                data=df.head().to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            )
        ])
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

# Register the app callbacks
def register_callbacks(app, openai_client):
    @app.callback(
        [Output('output-plots', 'children', allow_duplicate=True),
         Output('output-statistics', 'children', allow_duplicate=True),
         Output('output-info', 'children', allow_duplicate=True)],
        [Input('submit-button', 'n_clicks')],
        [State('user-input', 'value'), State('project-dropdown', 'value')]
    )
    def generate_response(n_clicks, user_input, selected_project):
        if n_clicks > 0:
            user_input = f"""i want you to generate a set of plotly graphs, statistics, and additional information 
            based on the user's request. In this input, the variable 'df' will be provided. That is the data you will use 
            to generate the plots and statistics. The user request is as follows: {user_input} 
            I want you to generate python code that creates different types of graphs (scatter plot, bar chart, line chart, histogram, etc.). 
            Also, generate code to calculate relevant statistics (mean, median, standard deviation, etc.) and provide additional information
            (data descriptions, insights, etc.) based on the DataFrame 'df'. Assume that a DataFrame named 'df' is already available, containing
            the necessary data for plotting and analysis. Ensure that the code is executable and does not rely on plt.show() or similar functions
            to display the graphs.
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

            Your generated code should follow these points:
                1. Function definitions for generating each type of graph.
                2. Function definitions for calculating statistics.
                3. Function definitions for providing additional information.
                4. Incorporation of the DataFrame 'df' ONLY into each function as a parameter.
                5. Do not use df.show()/fig.show() to display the graphs, as these will be used in a dashboard.
                6. Check to see if columns are numerical or not.
                7. Make sure to execute the functions at the end so the graphs, statistics, and information will be generated.
                8. Make sure to only pass 'df' as a parameter.
                9. Make sure the graphs are color-coordinated and visually appealing for the dashboard.
                10. Make sure to have descriptive titles for the graphs, statistics, and information.

            Here are some examples of Python code to help generate your response (keep in mind that these are only examples):
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
                        categorical_cols = df.select_dtypes(include=['object']).columns
                        if len(categorical_cols) < 1:
                            raise ValueError("DataFrame must contain at least one categorical column for a bar chart.")
                        
                        category_counts = df[categorical_cols[0]].value_counts()
                        fig = go.Figure(data=go.Bar(x=category_counts.index, y=category_counts.values))
                        fig.update_layout(title='Bar Chart', xaxis_title=categorical_cols[0], yaxis_title='Count')
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



                        def dataset_info_and_stats(df):
                            info = df.info()
                            describe = df.describe()
                            return info, describe

                        scatter_plot(df)
                        bar_chart(df)
                        line_chart(df)
                        dataset_info_and_stats(df)
                
                Please ensure that the graph effectively represents something of meaning revolving around the data frame.
                Also remember that the graph functions should ONLY have 'df' as a parameter that is being passed to them.
                Remember that 'df' is a DataFrame that is supplied by the user. It is what is used to generate the graphs.
                This will be displayed in a dashboard so make sure to write the code in a maner that it can be ran to display. 
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
                raise PreventUpdate  # Don't update the app if the code cleanup fails

            # run the cleaned code using the exec function
            exec_global = {'df': df}
            try:
                exec(cleaned_code, exec_global)
            except Exception as e:
                print(f"Error in execution: {e}")
                raise PreventUpdate

            # use the outputs of the executed code to update the app
            plot_functions = {name: func for name, func in exec_global.items() if callable(func) and name.startswith('plot_')}
            stats_functions = {name: func for name, func in exec_global.items() if callable(func) and name.startswith('stats_')}
            info_functions = {name: func for name, func in exec_global.items() if callable(func) and name.startswith('info_')}

            if not plot_functions and not stats_functions and not info_functions:
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
                        paper_bgcolor='#2d2d2d',  # Dark gray border
                        font_color='white'  # White text color
                    )

                    plot_figures.append(dcc.Graph(figure=plot_figure))
                except Exception as e:
                    print(f"Error generating plot '{name}': {e}")

            # Generate Statistics
            stats_components = []
            for name, stats_function in stats_functions.items():
                try:
                    stats_output = stats_function(df)
                    if isinstance(stats_output, (tuple, list)):
                        stats_components.extend([html.Div(name), *stats_output])
                    else:
                        stats_components.append(html.Div([html.P(name), html.Pre(stats_output)]))
                except Exception as e:
                    print(f"Error generating statistics '{name}': {e}")

            # Generate Additional Information
            info_components = []
            for name, info_function in info_functions.items():
                try:
                    info_output = info_function(df)
                    if isinstance(info_output, (tuple, list)):
                        info_components.extend([html.Div(name), *info_output])
                    else:
                        info_components.append(html.Div([html.P(name), html.Pre(info_output)]))
                except Exception as e:
                    print(f"Error generating information '{name}': {e}")
            '''
            return three lists, each containing the dash components for the plots, statistics, and information, respectively.
            these components will then be displayed in the corresponding dash components output-plots, output-statistics, and output-info. 
            Make sure to replace the plot_figure1, plot_figure2, stats_output, and info_output variables with the actual outputs from your code generation logic.
            By returning the Dash components directly, they will be rendered within the designated areas in the user interface, rather than opening in new browser windows.
            '''
        
        
        return plot_figures, stats_components, info_components #not sure about this 

        raise PreventUpdate #also forgot where this should go

        
     
        
        

    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        State('upload-data', 'last_modified')
    )
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            children = [parse_contents(c, n) for c, n in zip(list_of_contents, list_of_names)]
            return children
