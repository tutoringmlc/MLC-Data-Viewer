import pandas as pd
import base64
from github import Github
import streamlit as st
from datetime import datetime
from io import StringIO
import re
import pytz

#Import GitHub Data --> sign_in_sheet
def initialize_app():
    st.session_state['repo'] = git_repo()
    repo = st.session_state.get("repo", None)
    git_df(repo).to_csv('sign_in_sheet.csv',index=False)
    git_database(repo).to_csv('students.csv',index=False)
    
    st.session_state['initialized'] = True  # Set a flag in session state


# Function to create the sign-in entry
def MLC_sign_in(name, course_number, reason, csv_file):

    timestamp = set_timezone('America/Los_Angeles')
    # Extract weekday, date, and time
    weekday = timestamp.strftime('%A')
    date = timestamp.strftime('%Y-%m-%d')
    time = timestamp.strftime('%H:%M:%S')

    # Create the entry in the form of a dictionary
    entry = {
        "Timestamp": timestamp,
        "Name": name,
        "Course Number": course_number,
        "Reason": reason,
        "Weekday": weekday,
        "Date": date,
        "Time": time
    }

    try:
        # Load the existing CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        new_entry_df = pd.DataFrame([entry])
        df = pd.concat([df, new_entry_df], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        df = pd.DataFrame([entry])
    
    #Deletes all rows with less than 3 real values
    df = df.dropna(axis=0, thresh = 3)
    
    # Save the updated DataFrame back to the CSV
    df.to_csv(csv_file, index=False)
    
    #Example Usage:
    #MLC_sign_in(selected_student,student_data.iloc[0]['Course Number'],"Tutoring Only", 'sign_in_sheet.csv')  
    
def MLC_late_sign_in(name, course_number, reason,timestamp, csv_file):
    
    # Extract weekday, date, and time
    weekday = timestamp.strftime('%A')
    date = timestamp.strftime('%Y-%m-%d')
    time = timestamp.strftime('%H:%M:%S')

    # Create the entry in the form of a dictionary
    entry = {
        "Timestamp": timestamp,
        "Name": name,
        "Course Number": course_number,
        "Reason": reason,
        "Weekday": weekday,
        "Date": date,
        "Time": time
    }

    try:
        # Load the existing CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        new_entry_df = pd.DataFrame([entry])
        df = pd.concat([df, new_entry_df], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        df = pd.DataFrame([entry])
    
    #Deletes all rows with less than 3 real values
    df = df.dropna(axis=0, thresh = 3)
    
    # Save the updated DataFrame back to the CSV
    df.to_csv(csv_file, index=False)
    
 


def data_preprocessing(df):
    # Preprocessing
    df['Student'] = df['Student'].str.upper()
    df[['Course Name', 'Course Number', 'Course Ticket', 'Term']] = df['Course Ticket'].str.split('-', expand=True)
    # Apply the function to create a new column
    df['Student'] = df['Student'].apply(reformat_name)
    return df

def reformat_name(name):
    last_name, first_name = name.split(', ')
    return f"{first_name.capitalize()} {last_name.capitalize()}"

def set_timezone(location):
    tz = pytz.timezone(location)

    # Get the current UTC timestamp and convert it to Pacific Time
    timestamp_utc = datetime.now(pytz.utc)  # Get current time in UTC
    timestamp = timestamp_utc.astimezone(tz)  # Convert to Pacific Time
    return timestamp


