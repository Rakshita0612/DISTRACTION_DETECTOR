"""
Focus Calculator and Recommendation Engine
Distraction Detector — Study Focus Score
"""

import random
from typing import Tuple, Dict, Any, List

MOTIVATIONAL_QUOTES = [
    ("Focus is a muscle. The more you practice, the stronger it gets.", "Cal Newport"),
    ("Starve your distractions, feed your focus.", "Unknown"),
    ("You don't have to be extreme, just consistent.", "James Clear"),
    ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
    ("Deep work is the ability to focus without distraction on a cognitively demanding task.", "Cal Newport"),
    ("One hour of deep focus is worth four hours of fragmented work.", "Anonymous"),
    ("Success is the sum of small efforts, repeated day in and day out.", "Robert Collier"),
    ("Eliminate the noise, embrace the signal.", "Naval Ravikant"),
    ("Action cures fear; disciplined focus cures distraction.", "Unknown")
]

DISTRACTION_TYPES = [
    "Mobile Phone",
    "Social Media",
    "Notifications",
    "Noise",
    "Talking",
    "Other"
]

CATEGORY_CONFIG = {
    "Excellent Focus": {
        "range": "80–100%",
        "color": "#22C55E",
        "badge_bg": "rgba(34, 197, 94, 0.15)",
        "badge_border": "#22C55E",
        "icon": "🌟",
        "summary": "Superb dedication! You maintained a strong flow state with minimal interruptions. Keep nurturing this habit."
    },
    "Good Focus": {
        "range": "60–79%",
        "color": "#3B82F6",
        "badge_bg": "rgba(59, 130, 246, 0.15)",
        "badge_border": "#3B82F6",
        "icon": "🎯",
        "summary": "Great work! You stayed locked in for the majority of your session. A small adjustment to external distractions will bring you to the top tier."
    },
    "Needs Improvement": {
        "range": "40–59%",
        "color": "#F59E0B",
        "badge_bg": "rgba(245, 158, 11, 0.15)",
        "badge_border": "#F59E0B",
        "icon": "⚠️",
        "summary": "You encountered noticeable friction and disruption. Consider breaking your study into 25-minute Pomodoro sessions with structured pauses."
    },
    "High Distraction": {
        "range": "Below 40%",
        "color": "#EF4444",
        "badge_bg": "rgba(239, 68, 68, 0.15)",
        "badge_border": "#EF4444",
        "icon": "🚨",
        "summary": "Distractions took up most of this study block. Don't be discouraged—reset your environment, hide triggers, and try a 15-minute micro-sprint."
    }
}


def validate_session_inputs(
    study_duration: float,
    distraction_duration: float,
    subject: str
) -> Tuple[bool, str]:
    """
    Validate user inputs for study session.
    
    Rules:
    - Subject cannot be empty.
    - Study duration must be greater than zero.
    - Distraction duration cannot be negative.
    - Distraction duration cannot exceed study duration.
    """
    if not subject or not subject.strip():
        return False, "Subject is required. Please specify what you are studying."
    
    if study_duration <= 0:
        return False, "Study duration must be greater than 0 minutes."
    
    if distraction_duration < 0:
        return False, "Distraction duration cannot be negative."
    
    if distraction_duration > study_duration:
        return False, (
            f"Distraction duration ({distraction_duration:g} min) cannot exceed "
            f"total study duration ({study_duration:g} min)."
        )
    
    return True, ""


def calculate_focus_metrics(
    study_duration: float,
    distraction_duration: float
) -> Dict[str, Any]:
    """
    Calculate focused time, focus score, and assign focus category.
    
    Formula:
    Focused Time = Total Study Time - Distraction Time
    Focus Score = (Focused Time / Total Study Time) * 100
    """
    focused_time = round(study_duration - distraction_duration, 1)
    if study_duration > 0:
        focus_score = round((focused_time / study_duration) * 100, 1)
    else:
        focus_score = 0.0
    
    # Classify category
    if focus_score >= 80.0:
        category = "Excellent Focus"
    elif focus_score >= 60.0:
        category = "Good Focus"
    elif focus_score >= 40.0:
        category = "Needs Improvement"
    else:
        category = "High Distraction"
        
    cfg = CATEGORY_CONFIG[category]
    
    return {
        "study_duration": study_duration,
        "distraction_duration": distraction_duration,
        "focused_time": focused_time,
        "focus_score": focus_score,
        "category": category,
        "color": cfg["color"],
        "badge_bg": cfg["badge_bg"],
        "badge_border": cfg["badge_border"],
        "icon": cfg["icon"],
        "summary": cfg["summary"],
        "range": cfg["range"]
    }


def get_recommendations(
    distraction_type: str,
    focus_score: float
) -> List[Dict[str, str]]:
    """
    Generate personalized, actionable recommendations based on distraction type
    and focus score level.
    """
    recommendations = []
    
    # 1. Type-specific advice
    if distraction_type == "Mobile Phone":
        recommendations.append({
            "title": "Physical Distance Strategy",
            "text": "Place your smartphone in another room or out of arm's reach during deep study blocks. Out of sight significantly lowers cognitive temptation.",
            "icon": "📱"
        })
        recommendations.append({
            "title": "Focus Modes & App Locks",
            "text": "Enable iOS Focus Mode / Android Digital Wellbeing or use focus apps (e.g., Forest) that restrict unlock attempts during your session.",
            "icon": "🔒"
        })
    elif distraction_type == "Social Media":
        recommendations.append({
            "title": "Browser Site Blockers",
            "text": "Use browser extensions like Cold Turkey, StayFocusd, or Freedom to temporarily blacklist feed algorithms and short-form video sites.",
            "icon": "🌐"
        })
        recommendations.append({
            "title": "Session Separation",
            "text": "Log out of accounts on your study laptop. Adding small friction (like two-factor login) deters impulsive tab opening.",
            "icon": "🛑"
        })
    elif distraction_type == "Notifications":
        recommendations.append({
            "title": "Zero-Notification Protocol",
            "text": "Turn on 'Do Not Disturb' or airplane mode across all devices before opening your textbook or study notes.",
            "icon": "🔕"
        })
        recommendations.append({
            "title": "Batch Communication",
            "text": "Allocate dedicated 10-minute windows between major study blocks to triage messages rather than reacting in real-time.",
            "icon": "📬"
        })
    elif distraction_type == "Noise":
        recommendations.append({
            "title": "Acoustic Shielding",
            "text": "Equip noise-cancelling headphones or play non-vocal audio such as brown noise, binaural beats, or lofi soundscapes to mask ambient sounds.",
            "icon": "🎧"
        })
        recommendations.append({
            "title": "Environment Relocation",
            "text": "Identify quiet campus spaces, study rooms, or library floors reserved specifically for silent study.",
            "icon": "🏛️"
        })
    elif distraction_type == "Talking":
        recommendations.append({
            "title": "Dedicated Boundary Signaling",
            "text": "Wear visible over-ear headphones as a visual 'Do Not Disturb' sign, or communicate your set study hours to family/roommates.",
            "icon": "🗣️"
        })
        recommendations.append({
            "title": "Private Study Corner",
            "text": "Create a distinct physical workspace reserved exclusively for academics where casual socializing is strictly avoided.",
            "icon": "🚪"
        })
    else:  # "Other"
        recommendations.append({
            "title": "Distraction Log Notepad",
            "text": "Keep a blank scratchpad beside your desk. Whenever an unrelated thought or chore enters your mind, jot it down to review after your study block.",
            "icon": "📝"
        })
        recommendations.append({
            "title": "Pre-Study Friction Elimination",
            "text": "Prepare water, notes, stationery, and open necessary files before starting the clock so you have zero excuse to wander.",
            "icon": "⚡"
        })

    # 2. Score-specific advice
    if focus_score < 40.0:
        recommendations.append({
            "title": "Micro-Sprint Protocol (15-Minute Rule)",
            "text": "When focus feels overwhelmed, lower the barrier to entry. Commit to just 15 minutes of uninterrupted work before taking a guilt-free 5-minute break.",
            "icon": "⏱️"
        })
        recommendations.append({
            "title": "Reset Your Workspace",
            "text": "Clear clutter from your desk. Visual clutter silently taxes working memory and invites restless wandering.",
            "icon": "🧹"
        })
    elif focus_score < 60.0:
        recommendations.append({
            "title": "Classic Pomodoro Routine",
            "text": "Try 25 minutes of high-intensity study followed strictly by a 5-minute restorative rest (stand up, stretch, hydrate). Repeat 4 times.",
            "icon": "🍅"
        })
        recommendations.append({
            "title": "Single-Tasking Rule",
            "text": "Close all unrelated tabs and study only one topic or chapter at a time. Multitasking dilutes retention and spikes distraction time.",
            "icon": "🎯"
        })
    elif focus_score < 80.0:
        recommendations.append({
            "title": "50/10 Focus Intervals",
            "text": "You already have good focus stamina! Upgrade to 50-minute deep study blocks with 10-minute breaks to achieve even longer immersion.",
            "icon": "📈"
        })
        recommendations.append({
            "title": "Identify Peak Energy Hours",
            "text": "Schedule your toughest problem sets or revision during your biological peak alertness window (often morning or late afternoon).",
            "icon": "⚡"
        })
    else:
        recommendations.append({
            "title": "Maintain Peak Flow State",
            "text": "Exceptional focus achieved! Protect your current routine and schedule regular restorative breaks to prevent cognitive fatigue.",
            "icon": "🏆"
        })
        recommendations.append({
            "title": "Deliberate Practice",
            "text": "With such high focus retention, channel this deep energy into the hardest practice problems and active recall techniques.",
            "icon": "🧠"
        })

    return recommendations


def get_random_quote() -> Tuple[str, str]:
    """Get a random motivational quote."""
    return random.choice(MOTIVATIONAL_QUOTES)
