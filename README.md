# Automated Data Visualization Dashboard

## Description
The Automated Data Visualization Dashboard is an advanced, web-based application designed to empower users to upload their data files and generate insightful data visualizations through natural language commands. Leveraging OpenAI's GPT for processing these commands, the application facilitates an intuitive interface for business analysts, data scientists, and anyone interested in exploring data through visualizations. It supports various data formats, including CSV and Excel, and allows for the dynamic execution of Python code to transform, analyze, and visualize data.

## Installation

Ensure Python 3.6 or newer is installed on your machine.

### Steps:

1. Clone the repository:
```
git clone https://github.com/Whitleynl/dashboard.git
```
3. Navigate to the project directory:
```
cd automated-data-visualization-dashboard
```

3. Install the required dependencies:
// not sure about this right now 

## Environment Setup

Set an environment variable for your OpenAI API key. Replace `your_openai_api_key_here` with your actual OpenAI API key.

### Unix/Linux/MacOS:
```
export OPENAI_API_KEY='your_openai_api_key_here'
```

### Windows:
```
set OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

To run the dashboard:

```
python app.py
```

Navigate to the URL indicated in the terminal to access the dashboard.

### Features:

- **Data Upload**: Support for CSV and Excel file formats.
- **Natural Language Commands**: Generate visualizations by describing your requirements in natural language.
- **Dynamic Python Execution**: Backend execution of Python code for data transformation and visualization, based on user commands.

## Dependencies

Key dependencies include Dash for the web framework, Pandas for data manipulation, Matplotlib and Plotly for data visualization, and the OpenAI Python client for natural language processing. A full list of dependencies is available in the `requirements.txt` file. // << we should make this

## Running Tests

Currently, this project does not include a test suite. 

## License
// not sure about this 

## Contact Information

For questions, support, or feedback, reach out to us at whitleynl@g.cofc.edu
