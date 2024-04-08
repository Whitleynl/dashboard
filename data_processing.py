'''
Using plolty, create 4 graphs using a data frame named 'df' that we are going to give you. 
Here is some examples of python code that I wrote in order to help generate your response,
keep in mind that these are only example. I want you to make 4: 

    import plotly.graph_objects as go

    def scatter_plot(df):
        """
        This function generates a scatter plot using the first two numerical columns of the DataFrame.
        """
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) < 2:
            raise ValueError("DataFrame must contain at least two numerical columns for a scatter plot.")
        
        fig = go.Figure(data=go.Scatter(x=df[numeric_cols[0]], y=df[numeric_cols[1]], mode='markers'))
        fig.update_layout(title='Scatter Plot', xaxis_title='X Axis', yaxis_title='Y Axis')
        return fig

    def bar_chart(df):
        """
        This function generates a bar chart using the first numerical column of the DataFrame.
        """
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) < 1:
            raise ValueError("DataFrame must contain at least one numerical column for a bar chart.")
        
        fig = go.Figure(data=go.Bar(x=df[numeric_cols[0]], y=df.index))
        fig.update_layout(title='Bar Chart', xaxis_title='X Axis', yaxis_title='Y Axis')
        return fig

    def line_chart(df):
        """
        This function generates a line chart using all numerical columns of the DataFrame.
        """
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            raise ValueError("DataFrame must contain at least one numerical column for a line chart.")
        
        fig = go.Figure()
        for col in numeric_cols:
            fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines', name=col))
        fig.update_layout(title='Line Chart', xaxis_title='X Axis', yaxis_title='Y Axis')
        return fig


Please ensure that the graph effectively represents something of meaning revolving around the data frame.
Along with this make sure that you are importing all of the neccessary packages as the code provided is just an example. 






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
            Also Make sure to not use plt.show() in your code and have a line of code at the end that actually executes the function.
            You do not need to try to create a df, assume we already have one named df for you.
            When running the function pass a dataframe called df as your paramater rather than a file.

'''