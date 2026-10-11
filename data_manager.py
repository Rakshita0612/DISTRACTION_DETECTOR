"""
Local Data Persistence Manager
Distraction Detector — Study Focus Score
"""

import os
import uuid
from datetime import datetime, timedelta
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = os.path.join(DATA_DIR, "study_sessions.csv")

COLUMNS = [
    "session_id",
    "timestamp",
    "student_name",
    "subject",
    "study_duration",
    "distraction_duration",
    "focused_time",
    "focus_score",
    "category",
    "distraction_type",
    "notes",
    "is_demo"
]


def ensure_data_dir() -> None:
    """Ensure data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def get_empty_dataframe() -> pd.DataFrame:
    """Return an empty DataFrame with standard schema and data types."""
    df = pd.DataFrame(columns=COLUMNS)
    df = df.astype({
        "session_id": "str",
        "timestamp": "str",
        "student_name": "str",
        "subject": "str",
        "study_duration": "float64",
        "distraction_duration": "float64",
        "focused_time": "float64",
        "focus_score": "float64",
        "category": "str",
        "distraction_type": "str",
        "notes": "str",
        "is_demo": "bool"
    })
    return df


def load_sessions() -> pd.DataFrame:
    """
    Load saved study sessions from local CSV file.
    Returns empty DataFrame with schema if file does not exist or is empty.
    """
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return get_empty_dataframe()

    try:
        df = pd.read_csv(DATA_FILE)
        # Ensure all required columns exist
        for col in COLUMNS:
            if col not in df.columns:
                if col in ["study_duration", "distraction_duration", "focused_time", "focus_score"]:
                    df[col] = 0.0
                elif col == "is_demo":
                    df[col] = False
                else:
                    df[col] = ""
        # Convert numeric types
        df["study_duration"] = pd.to_numeric(df["study_duration"], errors="coerce").fillna(0.0)
        df["distraction_duration"] = pd.to_numeric(df["distraction_duration"], errors="coerce").fillna(0.0)
        df["focused_time"] = pd.to_numeric(df["focused_time"], errors="coerce").fillna(0.0)
        df["focus_score"] = pd.to_numeric(df["focus_score"], errors="coerce").fillna(0.0)
        df["is_demo"] = df["is_demo"].astype(bool)
        return df
    except Exception:
        return get_empty_dataframe()


def save_session(session_data: dict) -> pd.DataFrame:
    """
    Append a new session record to local CSV file.
    Returns updated DataFrame.
    """
    ensure_data_dir()
    df = load_sessions()

    # Generate session ID and timestamp if not provided
    if "session_id" not in session_data or not session_data["session_id"]:
        session_data["session_id"] = str(uuid.uuid4())[:8]

    if "timestamp" not in session_data or not session_data["timestamp"]:
        session_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "is_demo" not in session_data:
        session_data["is_demo"] = False

    new_row = pd.DataFrame([session_data])
    # Ensure column order
    new_row = new_row.reindex(columns=COLUMNS, fill_value="")

    if df.empty:
        df = new_row
    else:
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(DATA_FILE, index=False)
    return df


def clear_sessions() -> bool:
    """
    Clear all session history records.
    """
    ensure_data_dir()
    empty_df = get_empty_dataframe()
    empty_df.to_csv(DATA_FILE, index=False)
    return True


def delete_session(session_id: str) -> pd.DataFrame:
    """Delete a specific session by its ID."""
    df = load_sessions()
    if not df.empty:
        df = df[df["session_id"] != session_id]
        df.to_csv(DATA_FILE, index=False)
    return df


def load_demo_data() -> pd.DataFrame:
    """
    Populate realistic demo records clearly marked as demo data.
    Useful for college presentations.
    """
    base_time = datetime.now() - timedelta(days=5)
    sample_records = [
        {
            "session_id": "demo-01",
            "timestamp": (base_time + timedelta(days=0, hours=9)).strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": "Alex",
            "subject": "Data Structures & Algorithms",
            "study_duration": 90.0,
            "distraction_duration": 10.0,
            "focused_time": 80.0,
            "focus_score": 88.9,
            "category": "Excellent Focus",
            "distraction_type": "Mobile Phone",
            "notes": "Morning session on Binary Search Trees. Phone was put on silent.",
            "is_demo": True
        },
        {
            "session_id": "demo-02",
            "timestamp": (base_time + timedelta(days=1, hours=14)).strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": "Alex",
            "subject": "Operating Systems",
            "study_duration": 60.0,
            "distraction_duration": 15.0,
            "focused_time": 45.0,
            "focus_score": 75.0,
            "category": "Good Focus",
            "distraction_type": "Social Media",
            "notes": "Reviewed CPU scheduling algorithms. Checked Instagram twice.",
            "is_demo": True
        },
        {
            "session_id": "demo-03",
            "timestamp": (base_time + timedelta(days=2, hours=16)).strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": "Alex",
            "subject": "Computer Networks",
            "study_duration": 45.0,
            "distraction_duration": 22.0,
            "focused_time": 23.0,
            "focus_score": 51.1,
            "category": "Needs Improvement",
            "distraction_type": "Noise",
            "notes": "Studied in a noisy cafeteria. Found it hard to maintain train of thought.",
            "is_demo": True
        },
        {
            "session_id": "demo-04",
            "timestamp": (base_time + timedelta(days=3, hours=11)).strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": "Alex",
            "subject": "Database Management",
            "study_duration": 75.0,
            "distraction_duration": 8.0,
            "focused_time": 67.0,
            "focus_score": 89.3,
            "category": "Excellent Focus",
            "distraction_type": "Notifications",
            "notes": "SQL normalization problem sets. Great concentration using headphones.",
            "is_demo": True
        },
        {
            "session_id": "demo-05",
            "timestamp": (base_time + timedelta(days=4, hours=20)).strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": "Alex",
            "subject": "Web Technologies",
            "study_duration": 50.0,
            "distraction_duration": 32.0,
            "focused_time": 18.0,
            "focus_score": 36.0,
            "category": "High Distraction",
            "distraction_type": "Talking",
            "notes": "Attempted to study in the dorm lounge while friends were chatting.",
            "is_demo": True
        }
    ]

    ensure_data_dir()
    df = pd.DataFrame(sample_records)
    df.to_csv(DATA_FILE, index=False)
    return df
