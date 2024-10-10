import pandas as pd
import os

# Get the base directory of your project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the file path
file_path = os.path.join(BASE_DIR, 'chatapp', 'dataset', 'answers.xlsx')

# Check if the file exists before loading
if os.path.exists(file_path):
    excel_data = pd.read_excel(file_path)
else:
    print(f"File not found: {file_path}")
    excel_data = None  # Handle the case when the file is not found
