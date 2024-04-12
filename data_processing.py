'''
Using plotly, create 6 graphs using a data frame named 'df' that is supplied. 










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