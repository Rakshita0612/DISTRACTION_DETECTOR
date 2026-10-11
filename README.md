# 🎯 Distraction Detector — Study Focus Score

A modern, responsive web application designed for students to track study sessions, measure distractions, calculate an intuitive **Study Focus Score**, and receive personalized recommendations to maximize deep work.

Developed as a college mini-project demonstration using **Python**, **Streamlit**, **Pandas**, and **Plotly** with zero external paid APIs, hardware, or complex machine learning models required.

---

## 🌟 Key Features

1. **📊 Real-time Dashboard & Metrics**
   - High-level metric cards: **Total Study Time**, **Total Distraction Time**, **Total Focused Time**, and **Average Focus Score**.
   - Dynamic motivational quotes to encourage sustained study habits.
   - Clean empty state with one-click **Load Demo Data** for instant demonstration.

2. **⏱️ Interactive Study Session Logging**
   - Input fields: Student Name (optional), Subject / Topic, Total Study Duration (min), Distraction Duration (min), Primary Distraction Type, and Notes.
   - Comprehensive input validation:
     - Study duration must be $> 0$.
     - Distraction duration cannot be negative.
     - Distraction duration cannot exceed total study duration.
     - Subject name is required.
   - **Analyze My Focus** action button with instant visual feedback and celebratory effects for high performance.

3. **🧮 Focus Score Calculation & Classification**
   - **Formula**:
     $$\text{Focused Time} = \text{Total Study Time} - \text{Distraction Time}$$
     $$\text{Focus Score} = \left(\frac{\text{Focused Time}}{\text{Total Study Time}}\right) \times 100$$
   - **Categories**:
     - 🌟 **80% – 100%:** Excellent Focus (Optimal flow state, minimal disruption)
     - 🎯 **60% – 79%:** Good Focus (Consistent concentration, minor interruptions)
     - ⚠️ **40% – 59%:** Needs Improvement (Noticeable attention drift)
     - 🚨 **Below 40%:** High Distraction (Heavy friction and environmental distraction)
   - Transparent disclaimer noting that scores represent behavioral estimates from user-entered data rather than biometric/EEG measurements.

4. **📈 Interactive Distraction Analytics (Plotly Charts)**
   - **Focus Score Trendline**: Chronological trajectory across past sessions with color-banded threshold targets.
   - **Distraction Triggers Breakdown**: Donut chart highlighting total minutes lost to each distraction type (Mobile Phone, Social Media, Notifications, Noise, Talking, Other).
   - **Subject-Wise Comparison**: Horizontal bar chart comparing focus efficiency across academic subjects.
   - **Cumulative Time Composition**: Proportion of focused vs. distracted hours.

5. **💡 Personalized Cognitive Recommendations**
   - Dynamic advice based on user's primary distraction source (e.g., physical distance for phones, browser blacklists for social media, acoustic masking for noise).
   - Structured pacing recommendations based on score tier (15-minute sprints, 25/5 Pomodoros, 50/10 immersion intervals).

6. **📜 Persistent Local Study History**
   - Automatically saved to `data/study_sessions.csv`.
   - Filter history by subject or distraction type.
   - Export session records as CSV.
   - Safe **Clear History** feature with double-confirmation protection.
   - Clear disclosure that data is stored locally for single-user prototype use.

---

## 🎨 Color Palette & UI Design

Built with a modern, high-contrast dark theme:
- **Background:** `#0F172A` (Deep Slate)
- **Cards & Containers:** `#1E293B` (Dark Slate Blue)
- **Primary / Focus:** `#3B82F6` (Electric Blue)
- **Success / High Flow:** `#22C55E` (Emerald Green)
- **Warning / Drift:** `#F59E0B` (Amber)
- **Danger / Distraction:** `#EF4444` (Vibrant Coral Red)
- **Text:** `#FFFFFF` (Pure White) & `#94A3B8` (Muted Slate)

---

## 📁 Project Architecture

```
Distraction Detector/
├── .streamlit/
│   └── config.toml          # Custom dark theme configuration
├── data/
│   └── study_sessions.csv   # Local persistent CSV storage
├── app.py                   # Main Streamlit web application & UI
├── focus_calculator.py      # Calculations, validations, and recommendation engine
├── data_manager.py          # CSV load, save, delete, and demo data utilities
├── test_logic.py            # Automated unit tests for logic and edge cases
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation & execution guide
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ (Python 3.12 recommended)
- `pip` package manager

### 2. Install Dependencies
Run the following command in the project directory:
```bash
pip install -r requirements.txt
```

### 3. Launch the Web Application
Start the Streamlit development server:
```bash
streamlit run app.py
```

The application will automatically open in your default web browser at:
`http://localhost:8501`

---

## 🧪 Verification & Test Cases

The application includes automated tests verifying all requirements and formulas:

```bash
python -u test_logic.py
```

### Standard Demonstration Test Case:
- **Subject:** Python
- **Total Study Duration:** 60 minutes
- **Distraction Duration:** 15 minutes
- **Primary Distraction:** Mobile Phone
- **Expected Results:**
  - Focused Time: $60 - 15 = \mathbf{45\text{ minutes}}$
  - Focus Score: $\left(\frac{45}{60}\right) \times 100 = \mathbf{75.0\%}$
  - Category: **🎯 Good Focus** (60–79%)
  - Recommendations: Physical distance protocol and focus app lock suggestions.

### Validated Edge Cases:
- **Zero / Negative Study Time:** Form displays an inline error message and prevents saving.
- **Negative Distraction Time:** Form displays an inline error message and prevents saving.
- **Distraction Exceeds Study Duration:** Form displays an inline error message and prevents saving.
- **Empty History:** Gracefully renders informative empty states without runtime errors.

---

## 🎓 College Presentation Walkthrough (3-Minute Script)

1. **Introduction (30s):** Introduce the application as a tool to tackle modern student attention fragmentation without requiring privacy-invasive webcams or hardware.
2. **Dashboard Overview (30s):** Highlight the dark theme UI, metric cards (Total Study, Total Distraction, Focused Time, Average Score), and motivational quote. Click **Load Demo** in the sidebar to showcase rich analytics.
3. **Live Session Recording (60s):**
   - Navigate to **Log Study Session**.
   - Input: Subject = "Python", Study Duration = 60 min, Distraction Duration = 15 min, Distraction Type = "Mobile Phone".
   - Click **Analyze My Focus 🚀**.
   - Point out the 75% score card, the **Good Focus** badge, the breakdown, and the tailored Mobile Phone recommendations.
4. **Distraction Analytics (45s):**
   - Navigate to **Distraction Analysis**.
   - Present the **Focus Score Trendline** showing session improvement.
   - Present the **Distraction Breakdown Donut Chart** identifying the student's biggest time thief.
5. **Session History & Export (15s):** Show the persistent CSV table, filter options, and CSV download button.
