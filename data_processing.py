# data_processing.py
from contact_id_library import CONTACT_ID_LIBRARY
import pandas as pd

def process_csv(file_path):
    df = pd.read_csv(file_path)
    # Your data processing logic here
    return df

def remove_duplicates(df):
    return df.drop_duplicates()

def handle_missing_values(df):
    return df.fillna(0)  # or df.dropna(), depending on your needs

def clean_data(df):
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    return df

def count_service_lines_by_contact_id(df):
    #Initialize a dictionary to hold the counts
    contact_id_counts = {}

    #Loop through the library and count occurrences
    for name, id in CONTACT_ID_LIBRARY.items():
        contact_id_counts[name] = df[df['AppliedByContactId'] == id].shape[0]
    return contact_id_counts