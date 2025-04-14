import streamlit as st
import pandas as pd
import plotly.express as px
from mlc import set_timezone

st.title("📊 MLC Data Dashboard")

# File Upload Section
st.sidebar.header("Upload Files")
students_file = st.sidebar.file_uploader("Upload Student Database CSV", type="csv")
sign_in_file = st.sidebar.file_uploader("Upload Sign-In Sheet CSV", type="csv")

# Proceed only if both files are uploaded
if students_file and sign_in_file:
    # Read uploaded files
    df = pd.read_csv(students_file)
    sign_in_data = pd.read_csv(sign_in_file)

    with st.expander("Student Distribution by Class"):
        class_counts = df['Course Name'].value_counts()
        total_students = len(df)
        class_percentages = (class_counts / total_students) * 100

        # Convert to DataFrame for Plotly
        class_df = class_percentages.reset_index()
        class_df.columns = ['Course', 'Percentage']

        fig = px.pie(
            class_df,
            names='Course',
            values='Percentage',
            title="Student Distribution by Class",
            width=600,
            height=500
        )
        st.plotly_chart(fig)
        st.write("Class Percentage Breakdown:")
        st.dataframe(class_counts)

    with st.expander("Sign-Ins By Course", expanded=False):
        timestamp = set_timezone('America/Los_Angeles')
        current_date = timestamp.strftime('%Y-%m-%d')

        sign_in_data['Date'] = pd.to_datetime(sign_in_data['Date'])
        course_counts = sign_in_data['Course Number'].value_counts()
        total_sign_in = len(sign_in_data)
        course_percentages = (course_counts / total_sign_in) * 100

        course_df = course_percentages.reset_index()
        course_df.columns = ['Course', 'Percentage']

        fig = px.pie(
            course_df,
            names='Course',
            values='Percentage',
            title="Sign-In Distribution by Course",
            width=600,
            height=500
        )
        st.plotly_chart(fig)
        st.write("Percentage Breakdown:")
        st.dataframe(course_counts)

        # Date filter
        start_date = st.date_input("Select a start date", sign_in_data['Date'].min())
        end_date = st.date_input("Select an end date", sign_in_data['Date'].max())
        filtered_data_by_date = sign_in_data[
            (sign_in_data['Date'] >= pd.to_datetime(start_date)) &
            (sign_in_data['Date'] <= pd.to_datetime(end_date))
        ]

        # Group and plot frequency by date and course
        date_course_counts = filtered_data_by_date.groupby(['Date', 'Course Number']).size().reset_index(name='Frequency')

        fig = px.bar(
            date_course_counts,
            x='Date',
            y='Frequency',
            color='Course Number',
            title='Frequency of Visits by Date and Course Number',
            barmode='group'
        )
        st.plotly_chart(fig)

        st.write(f"Sign-in data between ({start_date}) and ({end_date}):")
        st.dataframe(date_course_counts)

        name_counts_sorted = sign_in_data['Name'].value_counts().sort_values(ascending=False)
        st.write("Most Frequent Visitors:")
        st.dataframe(name_counts_sorted)

else:
    st.info("👈 Please upload both the student database and sign-in CSV files to begin.")
