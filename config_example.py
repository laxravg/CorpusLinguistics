"""
Example configuration file.
Copy this to config.py and update the paths as needed.
"""

# Base directory (this will be set automatically)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths (relative to project root)
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'input')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

# Add any other configuration variables here
# For example:
# MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')

# Example of how to use in your code:
# from config import INPUT_DIR, OUTPUT_DIR
# input_file = os.path.join(INPUT_DIR, 'your_input_file.csv')
