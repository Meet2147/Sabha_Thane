import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Add custom CSS for minimalistic look and responsiveness
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f2f6;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333;
    }
    .stTextInput label, .stRadio label {
        font-size: 16px;
        color: #333;
    }
    .stTextInput input, .stRadio input {
        font-size: 16px;
        padding: 5px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stRadio div[role="radiogroup"] {
        display: flex;
        justify-content: space-around;
    }
    .stButton button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .stDownloadButton button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 16px;
    }
    .stDownloadButton button:hover {
        background-color: #218838;
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 10px;
        }
        .stTextInput label, .stRadio label {
            font-size: 14px;
        }
        .stTextInput input, .stRadio input {
            font-size: 14px;
            padding: 3px;
        }
        .stButton button, .stDownloadButton button {
            padding: 8px 16px;
            font-size: 14px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# List of names from Thane Yuvak Mandal
names = [
    'Akshad Hiteshbhai Bhadra', 'Aryan Abhijitbhai Kulkarni', 'Dhruv Mahendrabhai Jethwa',
    'Gaurav Deepakbhai Sarvaiya', 'Krunal Chandrakantbhai Rawal', 'Pathik Mansukhbhai Soni',
    'Ronak Vishnubhai Limbachiya', 'Sahil Anilbhai Joshi', 'Vikram Uttambhai Panchal',
    'Viral Jayeshbhai Panchal', 'Yagnesh Prabhulalbhai Vegad', 'Meet Chudasama',
    'Prince Sachinbhai Padiya', 'Neel Panchal', 'Rutvikbhai Panchal', 'Vaibhavbhai (Rutvik brtr)',
    'Ashish Zala - Divyesh Zala', 'Dinesh Zala - Divyesh Zala', 'Kalp Dama',
    'Chirag Jitendrabhai Panchal', 'Keyur Rawal', 'Divyesh Zala(JigneshJ.)', 'Jignesh Jethwa',
    'Rajesh Jethwa', 'Meet Kamlesh Panchal', 'Mohit Jethwa', 'Pratik Joshi',
    'Kishan Ramanbhai Prajapati', 'Darshan Ramanbhai Prajapati', 'Sahil Rajgor',
    'Vansh Sashikant Gohil', 'Aashish Rajgor', 'Mayur Panchal', 'Mukund Wala', 'Samay Panchal',
    'Tanvesh Panchal', 'Milap Devrajbhai Bhojak', 'Arya Parmar', 'Ayush Gohil (B2y-2022)',
    'Devansh Rajgor', 'Jay Chudasama', 'Rohit Rajgor', 'Yash Thakkar', 'Sagar Panchal',
    'Vivek Devaliya', 'Smith Thakkar', 'Aditya Rajgor', 'Krishna Balkare ', 'Bhavin Chauhan',
    'Om Singh', 'Prashant Satoskar', 'Ketan Parmar', 'Manish (Mav) Bhanushali', 'Parshav Panchal',
    'Pratik  Panchal(Parshav)', 'Darshan Chandarana', 'Gaurav Mahendrabhai Jethwa', 'Heet Thakar',
    'Henil Panchal', 'Rushabh Chawda', 'Janak Darji - 11TH', 'Akshay Jethwa', 'Heet Jethwa - NEW',
    'Naitik Chudasama', 'Nishit Panchal', 'Pratham Panchal', 'Rishi Rajgor', 'Rudra Kailash Panchal',
    'Ujjwal Jaiswal', 'Hiten Panchal', 'Om Zala', 'Atharva Sakpal', 'Dev Sanket', 'Aarish Pawar',
    'Abhay Panchal', 'Abhishek Mishra', 'Akshay Panchal', 'Ayush Bhudepra Panchal', 'Bipin Rajgor',
    'Darshan Bhadra', 'Devanshu Panchal', 'Dhaval Panchal', 'Dhaval Thakkar', 'Diven Jethwa',
    'Divya ', 'Gautam Panchal (B2Y)', 'Hardik Panchal', 'Hasmukh Panchal', 'Dakshesh Panchal',
    'Mangesh Dumbre'
]

# Function to generate dates for all Saturdays in the current year starting from July
def get_all_saturdays(year):
    d = datetime(year, 7, 1)
    d += timedelta(days=(5 - d.weekday() + 7) % 7)  # Move to the first Saturday of July
    while d.year == year:
        yield d
        d += timedelta(days=7)

# Get current year
current_year = datetime.now().year

# Generate all Saturdays for the current year starting from July
saturdays = list(get_all_saturdays(current_year))

# Initialize DataFrame
attendance_df = pd.DataFrame(index=names, columns=saturdays)

# Function to get summary
def get_summary(attendance_df, period):
    summary = attendance_df.apply(lambda row: (row == "Present").sum() + (row == "W&W").sum(), axis=1)
    return summary

# Function to filter attendance data based on period
def filter_attendance(attendance_df, period):
    if period == "weekly":
        return attendance_df.iloc[:, :4]
    elif period == "monthly":
        return attendance_df.iloc[:, :4]  # Assuming 4 Saturdays in a month
    elif period == "quarterly":
        return attendance_df.iloc[:, :13]  # Assuming 13 Saturdays in a quarter
    elif period == "half-yearly":
        return attendance_df.iloc[:, :26]  # Assuming 26 Saturdays in a half-year
    elif period == "yearly":
        return attendance_df  # All data for the year

# Streamlit app with sidebar navigation
st.sidebar.title("Attendance App Navigation")
pages = ["Mark Attendance", "Week Attendance", "Month Attendance", "Quarter Attendance", "Half Year Attendance", "Yearly Attendance"]
page = st.sidebar.radio("Go to", pages)

if page == "Mark Attendance":
    st.title("Mark Attendance")
    selected_date = st.date_input("Select a Saturday", value=saturdays[0], min_value=saturdays[0], max_value=saturdays[-1])
    selected_date = pd.to_datetime(selected_date)

    if selected_date not in saturdays:
        st.error("Please select a valid Saturday.")
    else:
        st.write(f"## Mark Attendance for {selected_date.date()}")

        search_name = st.text_input("Search for a name:")
        filtered_names = [name for name in names if search_name.lower() in name.lower()]

        if search_name and filtered_names:
            name = filtered_names[0]  # Get the first matching name
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(name)
            with col2:
                attendance = st.radio(
                    f"Attendance for {name}",
                    ["Present", "W&W", "Absent", "Absent with reason"],
                    index=0 if attendance_df.at[name, selected_date] == "Present" else 1 if attendance_df.at[name, selected_date] == "W&W" else 2 if attendance_df.at[name, selected_date] == "Absent" else 3,
                    key=f"attendance_{name}_{selected_date}",
                    horizontal=True
                )
                if attendance == "Absent with reason":
                    reason = st.text_input(f"Reason for {name}", key=f"reason_{name}_{selected_date}")

            if st.button("Submit"):
                if attendance == "Absent with reason":
                    attendance_df.at[name, selected_date] = f"Absent with reason: {reason}"
                else:
                    attendance_df.at[name, selected_date] = attendance
                st.success(f"Attendance marked for {name}")

elif page == "Week Attendance":
    st.title("Weekly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "weekly"))

elif page == "Month Attendance":
    st.title("Monthly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "monthly"))

elif page == "Quarter Attendance":
    st.title("Quarterly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "quarterly"))

elif page == "Half Year Attendance":
    st.title("Half-Yearly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "half-yearly"))

elif page == "Yearly Attendance":
    st.title("Yearly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "yearly"))

# Provide a download link for the attendance data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(attendance_df)

st.download_button(
    label="Download attendance data as CSV",
    data=csv,
    file_name='attendance.csv',
    mime='text/csv',
)
