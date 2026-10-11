"""
Distraction Detector — Study Focus Score
A Modern Streamlit Web Application for Study Focus Tracking & Analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

import data_manager
from focus_calculator import (
    DISTRACTION_TYPES,
    CATEGORY_CONFIG,
    MOTIVATIONAL_QUOTES,
    validate_session_inputs,
    calculate_focus_metrics,
    get_recommendations,
    get_random_quote
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Distraction Detector — Study Focus Score",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Dark Theme & Glassmorphism)
# ---------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Main app background */
.stApp {
    background-color: #0F172A;
    color: #FFFFFF;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0B1120;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #FFFFFF;
}

/* Custom Metric Card */
.metric-card {
    background: #1E293B;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(59, 130, 246, 0.5);
}

.metric-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94A3B8;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 4px;
}

.metric-sub {
    font-size: 0.8rem;
    color: #64748B;
}

/* Quote banner */
.quote-banner {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%);
    border-left: 4px solid #3B82F6;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 15px 0 25px 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.quote-text {
    font-size: 1.05rem;
    font-style: italic;
    color: #E2E8F0;
    margin-bottom: 6px;
}
.quote-author {
    font-size: 0.85rem;
    font-weight: 600;
    color: #60A5FA;
}

/* Badges */
.badge-category {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 12px;
}

/* Recommendation Card */
.rec-card {
    background: #1E293B;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.rec-card h4 {
    margin: 0 0 8px 0;
    font-size: 1rem;
    color: #60A5FA;
    display: flex;
    align-items: center;
    gap: 8px;
}
.rec-card p {
    margin: 0;
    font-size: 0.9rem;
    color: #CBD5E1;
    line-height: 1.5;
}

/* Empty State Card */
.empty-state {
    background: #1E293B;
    border: 2px dashed rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    padding: 40px 20px;
    text-align: center;
    color: #94A3B8;
    margin: 20px 0;
}
.empty-state h3 {
    color: #E2E8F0;
    margin-bottom: 8px;
}

/* Sub-cards and helpers */
.card-box {
    background: #1E293B;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 20px;
}

/* Streamlit button tweaks */
div.stButton > button:first-child {
    background-color: #3B82F6;
    color: #FFFFFF;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    padding: 8px 20px;
    transition: all 0.2s ease;
}
div.stButton > button:first-child:hover {
    background-color: #2563EB;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

/* Disclaimer text */
.disclaimer-box {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 0.78rem;
    color: #94A3B8;
    margin-top: 15px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def render_metric_card(title: str, value: str, sub: str = "", accent_color: str = "#3B82F6"):
    """Render a styled metric card."""
    html = f"""
    <div class="metric-card" style="border-left: 4px solid {accent_color};">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def get_plotly_layout(title: str = "") -> dict:
    """Standard Plotly dark layout template."""
    return dict(
        title=dict(text=title, font=dict(color="#FFFFFF", size=16)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(font=dict(color="#CBD5E1")),
        xaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            tickfont=dict(color="#94A3B8")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            tickfont=dict(color="#94A3B8")
        )
    )


# ---------------------------------------------------------
# Sidebar Navigation & Controls
# ---------------------------------------------------------
df_sessions = data_manager.load_sessions()

with st.sidebar:
    st.markdown("## 🎯 Focus Radar")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.85rem; margin-top: -10px;'>"
        "Study Session Tracker & Focus Analytics"
        "</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    menu_choice = st.radio(
        "Navigation",
        options=[
            "📊 Dashboard & Metrics",
            "⏱️ Log Study Session",
            "📈 Distraction Analysis",
            "📜 Study History",
            "💡 Focus Tips & Strategies"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("### 📌 Quick Overview")
    total_sessions_count = len(df_sessions)
    if total_sessions_count > 0:
        avg_score = df_sessions["focus_score"].mean()
        tot_study_mins = df_sessions["study_duration"].sum()
        st.markdown(f"**Sessions Recorded:** `{total_sessions_count}`")
        st.markdown(f"**Total Tracked:** `{tot_study_mins:g} mins`")
        st.markdown(f"**Average Score:** `{avg_score:.1f}%`")
    else:
        st.markdown("*No sessions logged yet.*")

    st.markdown("---")
    st.markdown("### 🧪 Demo Tools")
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        if st.button("Load Demo", use_container_width=True, help="Populate sample study sessions"):
            data_manager.load_demo_data()
            st.success("Demo data loaded!")
            st.rerun()

    with col_demo2:
        if st.button("Clear Data", use_container_width=True, help="Clear all stored study sessions"):
            st.session_state["show_clear_confirm"] = True

    if st.session_state.get("show_clear_confirm", False):
        st.warning("Are you sure you want to clear all history?")
        confirm_col1, confirm_col2 = st.columns(2)
        with confirm_col1:
            if st.button("Yes, Clear", use_container_width=True):
                data_manager.clear_sessions()
                st.session_state["show_clear_confirm"] = False
                st.success("History cleared!")
                st.rerun()
        with confirm_col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state["show_clear_confirm"] = False
                st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style='font-size: 0.75rem; color: #64748B; line-height: 1.4;'>
        <strong>Distraction Detector v1.0</strong><br>
        College Mini-Project Demonstration<br>
        100% Local Prototype • No external APIs
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# Top Header Banner
# ---------------------------------------------------------
st.markdown(
    """
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
        <div>
            <h1 style='margin: 0; font-size: 2.2rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;'>
                Distraction Detector <span style='color: #3B82F6;'>— Study Focus Score</span>
            </h1>
            <p style='margin: 4px 0 0 0; color: #94A3B8; font-size: 0.95rem;'>
                Quantify your attention, identify study interruptions, and optimize concentration.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Motivational Quote Card
quote_text, quote_author = get_random_quote()
st.markdown(
    f"""
    <div class="quote-banner">
        <div class="quote-text">"{quote_text}"</div>
        <div class="quote-author">— {quote_author}</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TAB 1: MAIN DASHBOARD & METRICS
# =========================================================
if menu_choice == "📊 Dashboard & Metrics":
    st.markdown("### 📊 Session Summary & High-Level Metrics")

    if df_sessions.empty:
        st.markdown(
            """
            <div class="empty-state">
                <div style="font-size: 3rem; margin-bottom: 10px;">📋</div>
                <h3>No Study Sessions Recorded Yet</h3>
                <p>Track your first study session to unlock deep focus analytics and concentration metrics.</p>
                <div style="margin-top: 15px;">
                    <em>Tip: Head to <strong>⏱️ Log Study Session</strong> or click <strong>Load Demo</strong> in the sidebar to view sample data.</em>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Check if demo data notice is needed
        demo_count = df_sessions["is_demo"].sum() if "is_demo" in df_sessions.columns else 0
        if demo_count > 0:
            st.info(f"ℹ️ Currently viewing dataset containing {demo_count} sample demonstration records.")

        # Aggregate Metrics
        total_study = df_sessions["study_duration"].sum()
        total_distraction = df_sessions["distraction_duration"].sum()
        total_focused = df_sessions["focused_time"].sum()
        avg_focus_score = df_sessions["focus_score"].mean()

        # Display Top Metric Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            render_metric_card(
                title="Total Study Time",
                value=f"{total_study:g} min",
                sub=f"~{total_study / 60:.1f} hours logged",
                accent_color="#3B82F6"
            )

        with col2:
            render_metric_card(
                title="Total Distraction Time",
                value=f"{total_distraction:g} min",
                sub=f"{(total_distraction / total_study * 100) if total_study > 0 else 0:.1f}% of total session time",
                accent_color="#EF4444"
            )

        with col3:
            render_metric_card(
                title="Total Focused Time",
                value=f"{total_focused:g} min",
                sub=f"~{total_focused / 60:.1f} hours of pure concentration",
                accent_color="#22C55E"
            )

        with col4:
            # Determine color for average score
            if avg_focus_score >= 80:
                score_color = "#22C55E"
                score_label = "🌟 Excellent Tier"
            elif avg_focus_score >= 60:
                score_color = "#3B82F6"
                score_label = "🎯 Good Tier"
            elif avg_focus_score >= 40:
                score_color = "#F59E0B"
                score_label = "⚠️ Needs Improvement"
            else:
                score_color = "#EF4444"
                score_label = "🚨 High Distraction"

            render_metric_card(
                title="Average Focus Score",
                value=f"{avg_focus_score:.1f}%",
                sub=score_label,
                accent_color=score_color
            )

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # Quick charts in 2 columns
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("#### ⏳ Focus vs Distraction Proportion")
            pie_data = pd.DataFrame({
                "Category": ["Focused Time", "Distraction Time"],
                "Minutes": [total_focused, total_distraction]
            })
            fig_donut = px.pie(
                pie_data,
                values="Minutes",
                names="Category",
                hole=0.55,
                color="Category",
                color_discrete_map={
                    "Focused Time": "#22C55E",
                    "Distraction Time": "#EF4444"
                }
            )
            fig_donut.update_layout(get_plotly_layout())
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#0F172A', width=2))
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        with chart_col2:
            st.markdown("#### 🚫 Distraction Triggers Breakdown")
            dist_counts = df_sessions.groupby("distraction_type")["distraction_duration"].sum().reset_index()
            dist_counts = dist_counts.sort_values(by="distraction_duration", ascending=False)
            fig_bar = px.bar(
                dist_counts,
                x="distraction_duration",
                y="distraction_type",
                orientation="h",
                labels={"distraction_duration": "Total Lost Minutes", "distraction_type": "Distraction Type"},
                color="distraction_duration",
                color_continuous_scale=["#3B82F6", "#EF4444"]
            )
            fig_bar.update_layout(get_plotly_layout())
            fig_bar.update_coloraxes(showscale=False)
            fig_bar.update_traces(marker_line_color="#0F172A", marker_line_width=1.5)
            st.plotly_chart(fig_bar, use_container_width=True)

        # Recent Session Highlight
        st.markdown("#### ⏱️ Most Recent Study Session")
        recent = df_sessions.iloc[-1]
        rec_metrics = calculate_focus_metrics(recent["study_duration"], recent["distraction_duration"])
        st.markdown(
            f"""
            <div class="card-box" style="border-left: 5px solid {rec_metrics['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <span style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF;">
                            {recent['subject']}
                        </span>
                        <span style="margin-left: 10px; color: #94A3B8; font-size: 0.85rem;">
                            ({recent['timestamp']})
                        </span>
                    </div>
                    <div class="badge-category" style="background: {rec_metrics['badge_bg']}; border: 1px solid {rec_metrics['badge_border']}; color: {rec_metrics['color']}; margin: 0;">
                        {rec_metrics['icon']} {rec_metrics['category']} — {recent['focus_score']:.1f}%
                    </div>
                </div>
                <div style="margin-top: 12px; display: flex; gap: 24px; font-size: 0.9rem; color: #CBD5E1; flex-wrap: wrap;">
                    <div><strong>Study Duration:</strong> {recent['study_duration']:g} min</div>
                    <div><strong>Focused:</strong> {recent['focused_time']:g} min</div>
                    <div><strong>Distraction:</strong> {recent['distraction_duration']:g} min ({recent['distraction_type']})</div>
                    <div><strong>Student:</strong> {recent['student_name'] if recent['student_name'] else 'Anonymous'}</div>
                </div>
                {f'<div style="margin-top: 10px; font-size: 0.85rem; color: #94A3B8; font-style: italic;">Notes: {recent["notes"]}</div>' if recent.get("notes") else ''}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# TAB 2: LOG STUDY SESSION
# =========================================================
elif menu_choice == "⏱️ Log Study Session":
    st.markdown("### ⏱️ Record Study Session & Calculate Focus Score")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.9rem;'>"
        "Enter the details of your study session below. The application will compute your focus metrics and provide instant recommendations."
        "</p>",
        unsafe_allow_html=True
    )

    form_col1, form_col2 = st.columns([1.1, 0.9])

    with form_col1:
        with st.form("study_session_form"):
            st.markdown("#### 📝 Session Details")

            student_name = st.text_input(
                "Student Name or Nickname (Optional)",
                placeholder="e.g., Alex, Priya, Chris...",
                help="Optional name to associate with this session."
            )

            subject = st.text_input(
                "Subject / Topic Being Studied *",
                value="Python",
                placeholder="e.g., Python, Data Structures, Mathematics, Calculus...",
                help="What subject did you focus on during this session?"
            )

            dur_col1, dur_col2 = st.columns(2)
            with dur_col1:
                study_duration = st.number_input(
                    "Total Study Duration (minutes) *",
                    min_value=0.0,
                    max_value=720.0,
                    value=60.0,
                    step=5.0,
                    help="Total time planned or spent at your study desk."
                )

            with dur_col2:
                distraction_duration = st.number_input(
                    "Distraction Duration (minutes) *",
                    min_value=0.0,
                    max_value=720.0,
                    value=15.0,
                    step=5.0,
                    help="Estimated minutes lost to phone, chatting, browsing, or daydreaming."
                )

            distraction_type = st.selectbox(
                "Main Distraction Type *",
                options=DISTRACTION_TYPES,
                index=0,
                help="Select the primary disruption you encountered."
            )

            notes = st.text_area(
                "Optional Session Notes",
                placeholder="e.g., Reviewed Chapter 4 recursion. Phone rang twice during problem 3.",
                height=70
            )

            submit_btn = st.form_submit_button("Analyze My Focus 🚀", use_container_width=True)

    # Process Form Submission
    with form_col2:
        if submit_btn:
            is_valid, err_msg = validate_session_inputs(
                study_duration=study_duration,
                distraction_duration=distraction_duration,
                subject=subject
            )

            if not is_valid:
                st.error(f"❌ Input Validation Error: {err_msg}")
            else:
                # Compute metrics
                res = calculate_focus_metrics(study_duration, distraction_duration)

                # Save record to persistence layer
                session_payload = {
                    "student_name": student_name.strip() if student_name else "Anonymous",
                    "subject": subject.strip(),
                    "study_duration": float(study_duration),
                    "distraction_duration": float(distraction_duration),
                    "focused_time": float(res["focused_time"]),
                    "focus_score": float(res["focus_score"]),
                    "category": res["category"],
                    "distraction_type": distraction_type,
                    "notes": notes.strip(),
                    "is_demo": False
                }
                data_manager.save_session(session_payload)

                # Visual celebration if score is high
                if res["focus_score"] >= 80:
                    st.balloons()

                st.success("✅ Session successfully analyzed and saved to local history!")

                # Result Card
                st.markdown(
                    f"""
                    <div class="card-box" style="border: 2px solid {res['color']};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #94A3B8;">
                                Computed Focus Score
                            </span>
                            <span class="badge-category" style="background: {res['badge_bg']}; border: 1px solid {res['badge_border']}; color: {res['color']}; margin: 0;">
                                {res['icon']} {res['category']}
                            </span>
                        </div>
                        <div style="font-size: 3.2rem; font-weight: 800; color: {res['color']}; margin: 8px 0;">
                            {res['focus_score']:.1f}%
                        </div>
                        <div style="font-size: 0.95rem; color: #E2E8F0; line-height: 1.5; margin-bottom: 16px;">
                            {res['summary']}
                        </div>
                        <div style="background: #0F172A; border-radius: 8px; padding: 14px; display: flex; justify-content: space-around; text-align: center;">
                            <div>
                                <div style="font-size: 0.75rem; color: #94A3B8;">Focused Time</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #22C55E;">{res['focused_time']:g} min</div>
                            </div>
                            <div style="border-left: 1px solid rgba(255,255,255,0.1);"></div>
                            <div>
                                <div style="font-size: 0.75rem; color: #94A3B8;">Distracted Time</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #EF4444;">{res['distraction_duration']:g} min</div>
                            </div>
                            <div style="border-left: 1px solid rgba(255,255,255,0.1);"></div>
                            <div>
                                <div style="font-size: 0.75rem; color: #94A3B8;">Total Duration</div>
                                <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF;">{res['study_duration']:g} min</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Instant Tailored Recommendations
                st.markdown("#### 💡 Tailored Session Advice")
                recs = get_recommendations(distraction_type, res["focus_score"])
                for r in recs[:2]:  # Show top 2 in this quick panel
                    st.markdown(
                        f"""
                        <div class="rec-card">
                            <h4><span>{r['icon']}</span> {r['title']}</h4>
                            <p>{r['text']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    """
                    <div class="disclaimer-box">
                        ⚠️ <strong>Estimation Notice:</strong> Focus Score is calculated strictly from self-reported session duration inputs. It represents a behavioral self-reflection model, not an automated biometric or neurological attention measurement.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            # Default helper state before analysis
            st.markdown(
                """
                <div class="card-box" style="text-align: center; padding: 35px 20px;">
                    <div style="font-size: 2.8rem; margin-bottom: 12px;">🎯</div>
                    <h3 style="color: #FFFFFF; margin-bottom: 8px;">Ready for Analysis</h3>
                    <p style="color: #94A3B8; font-size: 0.9rem; line-height: 1.6;">
                        Fill in your study session details on the left and click <strong>Analyze My Focus</strong>.
                    </p>
                    <div style="background: #0F172A; border-radius: 8px; padding: 14px; text-align: left; margin-top: 20px;">
                        <span style="font-size: 0.8rem; font-weight: 600; color: #3B82F6;">SCORING THRESHOLDS:</span>
                        <ul style="font-size: 0.82rem; color: #CBD5E1; margin: 8px 0 0 16px; padding: 0;">
                            <li><strong style="color: #22C55E;">80–100%:</strong> Excellent Focus (Minimal interruption)</li>
                            <li><strong style="color: #3B82F6;">60–79%:</strong> Good Focus (Healthy concentration)</li>
                            <li><strong style="color: #F59E0B;">40–59%:</strong> Needs Improvement (Frequent drift)</li>
                            <li><strong style="color: #EF4444;">&lt; 40%:</strong> High Distraction (Heavy disruption)</li>
                        </ul>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# TAB 3: DISTRACTION ANALYSIS & CHARTS
# =========================================================
elif menu_choice == "📈 Distraction Analysis":
    st.markdown("### 📈 In-Depth Attention & Distraction Analytics")

    if df_sessions.empty:
        st.markdown(
            """
            <div class="empty-state">
                <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
                <h3>No Analytics Available Yet</h3>
                <p>Record your study sessions or load demo data to view rich interactive charts.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<p style='color: #94A3B8; font-size: 0.9rem; margin-bottom: 20px;'>"
            "Explore session trends, primary distraction bottlenecks, and subject-level focus efficiency."
            "</p>",
            unsafe_allow_html=True
        )

        col_a1, col_a2 = st.columns(2)

        with col_a1:
            st.markdown("#### 1. Focus Score Trend Across Recorded Sessions")
            # Session-by-session trend line
            df_trend = df_sessions.copy().reset_index()
            df_trend["Session #"] = df_trend.index + 1

            fig_trend = go.Figure()
            # Reference threshold bands
            fig_trend.add_hrect(
                y0=80, y1=100, fillcolor="#22C55E", opacity=0.08, line_width=0,
                annotation_text="Excellent (80-100%)", annotation_position="top left",
                annotation_font=dict(color="#22C55E", size=10)
            )
            fig_trend.add_hrect(
                y0=60, y1=80, fillcolor="#3B82F6", opacity=0.08, line_width=0,
                annotation_text="Good (60-80%)", annotation_position="top left",
                annotation_font=dict(color="#3B82F6", size=10)
            )
            fig_trend.add_hrect(
                y0=0, y1=60, fillcolor="#EF4444", opacity=0.08, line_width=0,
                annotation_text="Attention Drift (<60%)", annotation_position="top left",
                annotation_font=dict(color="#EF4444", size=10)
            )

            # Trend line
            fig_trend.add_trace(go.Scatter(
                x=df_trend["Session #"],
                y=df_trend["focus_score"],
                mode="lines+markers",
                name="Focus Score (%)",
                line=dict(color="#3B82F6", width=3),
                marker=dict(size=9, color="#60A5FA", line=dict(color="#FFFFFF", width=2)),
                text=df_trend.apply(lambda r: f"Subject: {r['subject']}<br>Score: {r['focus_score']:.1f}%", axis=1),
                hoverinfo="text"
            ))

            fig_trend.update_layout(
                get_plotly_layout(),
                xaxis_title="Session Number",
                yaxis_title="Focus Score (%)",
                yaxis=dict(range=[0, 105], gridcolor="rgba(255, 255, 255, 0.08)")
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with col_a2:
            st.markdown("#### 2. Distraction Breakdown by Trigger")
            # Distraction distribution
            dist_summary = df_sessions.groupby("distraction_type").agg(
                lost_minutes=("distraction_duration", "sum"),
                session_count=("session_id", "count")
            ).reset_index()

            color_palette = ["#EF4444", "#F59E0B", "#3B82F6", "#8B5CF6", "#EC4899", "#10B981"]

            fig_pie = px.pie(
                dist_summary,
                values="lost_minutes",
                names="distraction_type",
                hole=0.45,
                color_discrete_sequence=color_palette
            )
            fig_pie.update_layout(get_plotly_layout())
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#0F172A', width=2))
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        col_b1, col_b2 = st.columns(2)

        with col_b1:
            st.markdown("#### 3. Subject-Wise Average Focus Score")
            subj_summary = df_sessions.groupby("subject").agg(
                avg_score=("focus_score", "mean"),
                total_time=("study_duration", "sum")
            ).reset_index().sort_values(by="avg_score", ascending=True)

            fig_subj = px.bar(
                subj_summary,
                x="avg_score",
                y="subject",
                orientation="h",
                labels={"avg_score": "Average Focus Score (%)", "subject": "Subject"},
                text=subj_summary["avg_score"].apply(lambda v: f"{v:.1f}%"),
                color="avg_score",
                color_continuous_scale=["#EF4444", "#F59E0B", "#22C55E"]
            )
            fig_subj.update_layout(
                get_plotly_layout(),
                xaxis=dict(range=[0, 105], gridcolor="rgba(255, 255, 255, 0.08)")
            )
            fig_subj.update_coloraxes(showscale=False)
            fig_subj.update_traces(textposition="outside")
            st.plotly_chart(fig_subj, use_container_width=True)

        with col_b2:
            st.markdown("#### 4. Cumulative Time Composition")
            tot_foc = df_sessions["focused_time"].sum()
            tot_dis = df_sessions["distraction_duration"].sum()
            bar_df = pd.DataFrame([
                {"Metric": "Study Hours", "Segment": "Focused Time", "Hours": round(tot_foc / 60, 2)},
                {"Metric": "Study Hours", "Segment": "Distracted Time", "Hours": round(tot_dis / 60, 2)}
            ])
            fig_stacked = px.bar(
                bar_df,
                x="Hours",
                y="Metric",
                color="Segment",
                orientation="h",
                color_discrete_map={
                    "Focused Time": "#22C55E",
                    "Distracted Time": "#EF4444"
                },
                text="Hours"
            )
            fig_stacked.update_layout(get_plotly_layout(), barmode="stack")
            fig_stacked.update_traces(texttemplate='%{text}h', textposition='inside')
            st.plotly_chart(fig_stacked, use_container_width=True)


# =========================================================
# TAB 4: STUDY HISTORY
# =========================================================
elif menu_choice == "📜 Study History":
    st.markdown("### 📜 Recorded Study Sessions History")

    if df_sessions.empty:
        st.markdown(
            """
            <div class="empty-state">
                <div style="font-size: 3rem; margin-bottom: 10px;">📂</div>
                <h3>No Saved Sessions Found</h3>
                <p>Your recorded sessions will appear here with detailed breakdown metrics.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Filter options
        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            all_subjects = ["All Subjects"] + sorted(list(df_sessions["subject"].dropna().unique()))
            sel_subject = st.selectbox("Filter by Subject", options=all_subjects)

        with col_f2:
            all_dist_types = ["All Types"] + sorted(list(df_sessions["distraction_type"].dropna().unique()))
            sel_dist_type = st.selectbox("Filter by Distraction Type", options=all_dist_types)

        filtered_df = df_sessions.copy()
        if sel_subject != "All Subjects":
            filtered_df = filtered_df[filtered_df["subject"] == sel_subject]
        if sel_dist_type != "All Types":
            filtered_df = filtered_df[filtered_df["distraction_type"] == sel_dist_type]

        st.markdown(f"**Showing {len(filtered_df)} session(s):**")

        # Format dataframe for display
        display_df = filtered_df[[
            "timestamp",
            "subject",
            "study_duration",
            "distraction_duration",
            "focused_time",
            "focus_score",
            "category",
            "distraction_type",
            "student_name"
        ]].copy()

        display_df.rename(columns={
            "timestamp": "Date & Time",
            "subject": "Subject",
            "study_duration": "Study (min)",
            "distraction_duration": "Distracted (min)",
            "focused_time": "Focused (min)",
            "focus_score": "Focus Score (%)",
            "category": "Classification",
            "distraction_type": "Primary Distraction",
            "student_name": "Student"
        }, inplace=True)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # Download CSV button
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Sessions as CSV",
            data=csv_data,
            file_name=f"study_focus_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        st.markdown("---")
        # History Danger Zone
        with st.expander("⚠️ Danger Zone: Clear History"):
            st.markdown(
                "<p style='color: #EF4444; font-size: 0.9rem;'>"
                "This action will permanently delete all logged study session records from the local file."
                "</p>",
                unsafe_allow_html=True
            )
            confirm_check = st.checkbox("I understand that this action cannot be undone.")
            if st.button("Permanently Delete All History", disabled=not confirm_check):
                data_manager.clear_sessions()
                st.success("All session records have been deleted.")
                st.rerun()

        st.markdown(
            """
            <div class="disclaimer-box">
                📁 <strong>Local Prototype Storage Notice:</strong> Records are saved locally in <code>data/study_sessions.csv</code> on this machine. This prototype is configured for single-student demonstration and does not use a cloud database.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# TAB 5: FOCUS TIPS & STRATEGIES
# =========================================================
elif menu_choice == "💡 Focus Tips & Strategies":
    st.markdown("### 💡 Concentration Strategies & Habit Science")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.9rem;'>"
        "Evidence-backed focus protocols based on cognitive science, attention management, and study ergonomics."
        "</p>",
        unsafe_allow_html=True
    )

    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown(
            """
            <div class="rec-card">
                <h4><span>📱</span> Phone & Digital Dopamine Detox</h4>
                <p>
                    <strong>The 20-Foot Rule:</strong> Research indicates that merely having your smartphone visible on your desk drains cognitive capacity. Place it in a bag or outside your room during deep study blocks.
                </p>
            </div>
            <div class="rec-card">
                <h4><span>🍅</span> The 25/5 Pomodoro Cadence</h4>
                <p>
                    <strong>Interval Training for the Brain:</strong> Commit to 25 minutes of unbroken work, followed by a strict 5-minute break away from screens. Repeat 4 cycles, then take a longer 20-minute restorative break.
                </p>
            </div>
            <div class="rec-card">
                <h4><span>🎧</span> Soundscapes & Acoustic Masking</h4>
                <p>
                    <strong>Brown Noise & Binaural Beats:</strong> Vocal music triggers language processing centers in the brain. Switch to low-frequency brown noise, rain sounds, or video game soundtracks engineered for focus.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with t_col2:
        st.markdown(
            """
            <div class="rec-card">
                <h4><span>📝</span> The Distraction Scratchpad</h4>
                <p>
                    <strong>Defeating Urgent Random Thoughts:</strong> Keep a blank paper beside you. When random thoughts like "I need to reply to that email" arise, write them down immediately and return to studying without tab switching.
                </p>
            </div>
            <div class="rec-card">
                <h4><span>⚡</span> Friction Engineering</h4>
                <p>
                    <strong>Increase Friction on Distractions:</strong> Log out of social apps, install website blockers (Cold Turkey, Freedom), and keep your study materials pre-opened so starting has zero resistance.
                </p>
            </div>
            <div class="rec-card">
                <h4><span>🌅</span> Chronotype Synchronization</h4>
                <p>
                    <strong>Protect Your Golden Hours:</strong> Match your most conceptually difficult topics (e.g. math proofs, complex algorithms) to your peak alertness time, reserving routine tasks for low-energy hours.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("#### 🎯 Focus Score Interpretation Guide")
    st.markdown(
        """
        | Focus Score | Category | Recommended Action |
        |---|---|---|
        | **80% – 100%** | **🌟 Excellent Focus** | Exceptional cognitive flow. Maintain current environment and rest adequately to prevent burnout. |
        | **60% – 79%** | **🎯 Good Focus** | Solid study productivity. Minor tweaks to notification hygiene can propel you above 80%. |
        | **40% – 59%** | **⚠️ Needs Improvement** | Frequent interruptions observed. Shorten session length to 25 minutes to rebuild stamina. |
        | **Below 40%** | **🚨 High Distraction** | Critical cognitive drag. Remove external triggers, change location, and start with a 15-minute sprint. |
        """
    )
