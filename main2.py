import io
import numpy as np
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Student Grade & Exam Performance Analyzer",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_default_data():
  """Generates sample student roster and exam scores."""
  np.random.seed(42)
  num_students = 50
  student_ids = [f"STU{1001 + i}" for i in range(num_students)]

  first_names = [
      "Aarav",
      "Vivaan",
      "Aditya",
      "Vihaan",
      "Arjun",
      "Sai",
      "Reyansh",
      "Ayaan",
      "Krishna",
      "Ishaan",
      "Diya",
      "Sanya",
      "Ananya",
      "Priya",
      "Kavya",
      "Neha",
      "Aadhya",
      "Pooja",
      "Rhea",
      "Tanvi",
  ]
  last_names = [
      "Sharma",
      "Verma",
      "Gupta",
      "Malhotra",
      "Mehra",
      "Joshi",
      "Kumar",
      "Singh",
      "Patel",
      "Reddy",
      "Nair",
      "Iyer",
      "Chopra",
      "Bose",
      "Sen",
  ]

  names = [
      f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
      for _ in range(num_students)
  ]

  data = {
      "Student ID": student_ids,
      "Student Name": names,
      "Mathematics": np.random.randint(40, 100, size=num_students),
      "Science": np.random.randint(35, 100, size=num_students),
      "English": np.random.randint(45, 100, size=num_students),
      "History": np.random.randint(40, 98, size=num_students),
  }
  return pd.DataFrame(data)


# App Header
st.markdown(
    '<p class="main-header">🎓 Student Grade & Exam Performance Analyzer</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-header">Analyze test scores, review subject distributions,'
    " and inspect student performance thresholds.</p>",
    unsafe_allow_html=True,
)

# Sidebar Controls
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload Student CSV File", type=["csv"]
)

if uploaded_file is not None:
  try:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Custom dataset loaded successfully!")
  except Exception as e:
    st.sidebar.error(f"Error loading file: {e}")
    df = load_default_data()
else:
  df = load_default_data()
  st.sidebar.info("Using sample dataset. Upload a CSV to use custom data.")

# Sidebar Configurations & Filters
st.sidebar.header("⚙️ Analysis Settings")
passing_threshold = st.sidebar.slider(
    "Passing Score Threshold (%)", min_value=30, max_value=80, value=50, step=5
)

# Identify Subject Columns (Exclude ID and Name)
subject_cols = [
    col
    for col in df.columns
    if col not in ["Student ID", "Student Name", "Total", "Average", "Grade"]
]

# --- Pandas & NumPy Data Processing ---
# Calculate Total and Average Scores
df["Total Score"] = df[subject_cols].sum(axis=1)
df["Average Score"] = df[subject_cols].mean(axis=1)


# Assign Letter Grades using NumPy conditions
def assign_grade(avg):
  if avg >= 90:
    return "A+"
  elif avg >= 80:
    return "A"
  elif avg >= 70:
    return "B"
  elif avg >= 60:
    return "C"
  elif avg >= passing_threshold:
    return "D"
  else:
    return "F"


df["Letter Grade"] = df["Average Score"].apply(assign_grade)

# Determine Pass/Fail based on average threshold
df["Status"] = np.where(
    df["Average Score"] >= passing_threshold, "Passed", "Needs Improvement"
)

# --- Top Metrics Row ---
col1, col2, col3, col4 = st.columns(4)

class_avg_score = np.mean(df["Average Score"])
class_median_score = np.median(df["Average Score"])
class_variance = np.var(df["Average Score"])
pass_rate = (
    (df["Status"] == "Passed").sum() / len(df)
) * 100  # Percentage passing

with col1:
  st.metric(
      label="Class Average Score",
      value=f"{class_avg_score:.2f}",
      delta=f"{class_avg_score - passing_threshold:.1f} vs Passing Line",
  )
with col2:
  st.metric(label="Class Median Score", value=f"{class_median_score:.2f}")
with col3:
  st.metric(label="Overall Pass Rate", value=f"{pass_rate:.1f}%")
with col4:
  st.metric(label="Score Variance (NumPy)", value=f"{class_variance:.2f}")

st.markdown("---")

# --- Tabs for Layout ---
tab1, tab2, tab3 = st.tabs(
    ["📊 Class Overview", "🔍 Individual Student Scorecard", "📋 Complete Roster"]
)

with tab1:
  st.subheader("Subject-wise Performance Breakdown")

  # Calculate subject-level statistics using NumPy/Pandas
  subject_stats = []
  for sub in subject_cols:
    sub_scores = df[sub].values
    subject_stats.append({
        "Subject": sub,
        "Average": np.mean(sub_scores),
        "Highest": np.max(sub_scores),
        "Lowest": np.min(sub_scores),
        "Pass Rate (%)": np.mean(sub_scores >= passing_threshold) * 100,
    })

  sub_df = pd.DataFrame(subject_stats)
  st.dataframe(sub_df.style.format({
      "Average": "{:.2f}",
      "Highest": "{:.0f}",
      "Lowest": "{:.0f}",
      "Pass Rate (%)": "{:.1f}%",
  }), use_container_width=True)

  st.subheader("Grade Distribution")
  grade_counts = df["Letter Grade"].value_counts().reindex(
      ["A+", "A", "B", "C", "D", "F"], fill_value=0
  )
  st.bar_chart(grade_counts)

with tab2:
  st.subheader("Individual Student Scorecard Lookup")

  # Search / Select Student
  selected_student = st.selectbox(
      "Search or Select Student:", df["Student Name"].unique()
  )

  # Filter info for selected student
  student_record = df[df["Student Name"] == selected_student].iloc[0]

  sc_col1, sc_col2 = st.columns([1, 2])

  with sc_col1:
    st.markdown(f"### **{student_record['Student Name']}**")
    st.write(f"**Student ID:** {student_record['Student ID']}")
    st.write(f"**Overall Grade:** {student_record['Letter Grade']}")
    st.write(f"**Average Score:** {student_record['Average Score']:.2f}")

    status_color = (
        "green" if student_record["Status"] == "Passed" else "orange"
    )
    st.markdown(
        f"**Status:** <span style='color:{status_color}; font-weight:bold;'>{student_record['Status']}</span>",
        unsafe_allow_html=True,
    )

  with sc_col2:
    st.markdown("#### Subject Scores breakdown")
    individual_scores = {
        sub: student_record[sub] for sub in subject_cols
    }
    ind_df = pd.DataFrame(
        list(individual_scores.items()), columns=["Subject", "Score"]
    )
    st.bar_chart(ind_df.set_index("Subject"))

with tab3:
  st.subheader("Complete Class Roster & Filter")

  # Filter Options
  status_filter = st.selectbox(
      "Filter by Status:", ["All", "Passed", "Needs Improvement"]
  )

  filtered_df = df.copy()
  if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

  st.dataframe(filtered_df, use_container_width=True)

  # Download Button for Processed Report
  csv_buffer = io.StringIO()
  filtered_df.to_csv(csv_buffer, index=False)
  st.download_button(
      label="📥 Download Filtered Report as CSV",
      data=csv_buffer.getvalue(),
      file_name="student_performance_report.csv",
      mime="text/csv",
  )
