import os
import re
import ast
import matplotlib
matplotlib.use('Agg') # interactive display
import pandas as pd
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash import html, dcc

# file path for the ai
file_path = os.path.join(os.getcwd(), 'data', 'student_math_clean.csv')


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
        
        # Display basic information about the DataFrame
        # print("DataFrame information:")
        # print(df.info())
        
        # Display the first few rows of the DataFrame
        # print("\nFirst few rows of the DataFrame:")
        # print(df.head())
        
        # Check for any missing values in the DataFrame
        # print("\nMissing values:")
        # print(df.isnull().sum())
        
        # Check for unique values in categorical columns
        # print("\nUnique values in categorical columns:")
        # for column in df.select_dtypes(include=['object']).columns:
            # print(f"{column}: {df[column].unique()}")
        
        # Display descriptive statistics for numerical columns
        # print("\nDescriptive statistics for numerical columns:")
        # print(df.describe())
        
        # Clean the 'studytime' column
        # print("\nCleaning 'studytime' column...")
        studytime_mapping = {
            '0 to 2 hours': 1.0,
            '2 to 5 hours': 3.5,
            '5 to 10 hours': 7.5,
            '10 or more hours': 10.0
        }
        df['studytime'] = df['studytime'].map(studytime_mapping)
        
        # print("\nProcessed 'studytime' column:")
        # print(df['studytime'].unique())
        
        print("\nData inspection completed.")
        
    except Exception as e:
        print(f"Error loading or inspecting the CSV file: {e}")

# Example usage:
file_path = 'data/student_math_clean.csv'
load_and_inspect_csv(file_path)

def register_callbacks(app, openai_client):
    @app.callback(
        Output('output-plots', 'children'),
        [Input('submit-button', 'n_clicks')],
        [State('user-input', 'value'), State('project-dropdown', 'value')]
    )

    def generate_response(n_clicks, user_input, selected_project):
        if n_clicks > 0:
            # Append the desired string to the user input
            # Ask to not use plt.show()
            # ask for functions 
            user_input = f"""{user_input}
              Write your code in python and describe what you did. 
              You MUST use 'What this code does:' format when describing the steps you did.
              Here is an example of what I want,
                 What this code does:
                    1. It loads the dataset from the specified file path.

                    2. It selects the necessary columns from the DataFrame.

                    3. It converts all categorical variables into numerical values using `LabelEncoder`.

                    4. It standardizes the dataset to have mean=0 and variance=1 which is a requirement
                    for many machine learning algorithms.

                    5. It performs t-SNE on the processed dataset to reduce its dimensionality to 2, 
                    suitable for graphical representation.

                    6. It converts the result into a new DataFrame dedicated for t-SNE result, then
                    generates a scatterplot from the DataFrame to visualize the distribution of 
                    student data in the 2D t-SNE space.
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
            exec_global = {}
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
            plots = []
            for plot_name, plot_function in plot_functions.items():
                # call the plot function to generate plot
                plot_figure = plot_function()

                # Update the figure property of the graph component
                graph_id = f'plot-{plot_name}'
                app.layout.children.append(dcc.Graph(id=graph_id, figure=plot_figure))
                plots.append(html.Div([
                    html.H4(f"Here is your plot for ({plot_name}): "),
                    dcc.Graph(id=graph_id)  # Embed the plot as dcc.Graph
                ]))

            return plots
            '''
            return html.Div([
                html.H4(f"Code Executed Successfully!"),
                html.P("Check the dashboard for the output.")
            ])
            '''

    """@app.callback(
        Output('project-dropdown', 'options'),
        Input('submit-new-project-button', 'n_clicks'),
        State('new-project-input', 'value'),
        State('project-dropdown', 'options')
    )"""
    def add_new_project(n_clicks, new_project_name, current_options):
        if n_clicks > 0 and new_project_name:
            new_project_option = {'label': new_project_name, 'value': new_project_name}
            updated_options = current_options + [new_project_option]
            return updated_options
        return current_options
    