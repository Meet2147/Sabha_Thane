import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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

# Initialize DataFrame in session state if it does not exist
if "attendance_df" not in st.session_state:
    st.session_state.attendance_df = pd.DataFrame(index=names, columns=[s.date() for s in saturdays])

attendance_df = st.session_state.attendance_df

# Function to get summary
def get_summary(attendance_df, period):
    summary = attendance_df.apply(lambda row: (row == "P").sum(), axis=1)
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

# Get selected date from session state if it exists
selected_date = st.session_state.get("selected_date", saturdays[0].date())

if page == "Mark Attendance":
    st.title("Mark Attendance")
    selected_date = st.date_input("Select a Saturday", value=selected_date, min_value=saturdays[0].date(), max_value=saturdays[-1].date())
    st.session_state.selected_date = selected_date  # Save the selected date to session state

    if selected_date not in [s.date() for s in saturdays]:
        st.error("Please select a valid Saturday.")
    else:
        st.write(f"## Mark Attendance for {selected_date}")

        # Display all names in 5 columns
        cols = st.columns(5)
        for i, name in enumerate(names):
            col = cols[i % 5]
            col.write(name)

        search_name = st.text_input("Search for a name:")
        filtered_names = [name for name in names if search_name.lower() in name.lower()]

        if search_name and filtered_names:
            for name in filtered_names:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write(name)
                with col2:
                    attendance = st.radio(
                        f"Attendance for {name}",
                        ["Present", "W&W", "Absent", "Absent with reason"],
                        index=0 if attendance_df.at[name, selected_date] == "P" else 1 if attendance_df.at[name, selected_date] == "P" else 2 if attendance_df.at[name, selected_date] == "A" else 3,
                        key=f"attendance_{name}_{selected_date}",
                        horizontal=True
                    )

                    reason = ""
                    if attendance == "Absent with reason":
                        reason = st.text_input(f"Reason for {name}", key=f"reason_{name}_{selected_date}")

                    if st.button(f"Submit {name}"):
                        if attendance == "Absent with reason":
                            attendance_df.at[name, selected_date] = f"AR: {reason}"
                        elif attendance == "Present":
                            attendance_df.at[name, selected_date] = "P"
                        elif attendance == "W&W":
                            attendance_df.at[name, selected_date] = "P"
                        elif attendance == "Absent":
                            attendance_df.at[name, selected_date] = "A"
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

# Format the filename with the selected date
formatted_date = st.session_state.selected_date.strftime("%d_%m_%y")
filename = f"Attendance_{formatted_date}.csv"

st.download_button(
    label="Download attendance data as CSV",
    data=csv,
    file_name=filename,
    mime='text/csv',
)
