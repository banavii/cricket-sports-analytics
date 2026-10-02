import streamlit as st
import pandas as pd
import plotly.express as px

from database.connection import SessionLocal
from database.models import (
    Team,
    Player,
    Match,
    Injury,
    TrainingSession,
    Equipment,
)

from analytics.performance import calculate_performance_scores
from analytics.training import get_training_statistics
from analytics.injury import get_injury_statistics
from analytics.matches import get_match_list


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cricket Sports Intelligence",
    page_icon="🏏",
    layout="wide",
)


# --------------------------------------------------
# DATABASE STATISTICS
# --------------------------------------------------

def get_dashboard_statistics():

    session = SessionLocal()

    try:

        total_players = session.query(Player).count()

        total_teams = session.query(Team).count()

        total_matches = session.query(Match).count()

        total_training_sessions = (
            session.query(TrainingSession).count()
        )

        total_equipment = (
            session.query(Equipment).count()
        )

        active_injuries = (
            session.query(Injury)
            .filter(
                Injury.recovery_status == "Recovering"
            )
            .count()
        )

        available_players = (
            total_players - active_injuries
        )

        return {
            "players": total_players,
            "teams": total_teams,
            "matches": total_matches,
            "training_sessions": total_training_sessions,
            "equipment": total_equipment,
            "active_injuries": active_injuries,
            "available_players": available_players,
        }

    finally:
        session.close()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "🏏 Cricket Sports Performance "
    "& Operations Intelligence"
)

st.markdown(
    """
    **A data-driven platform for monitoring player performance,
    training, injuries, matches, and team operations.**
    """
)

st.divider()


# --------------------------------------------------
# LOAD ANALYTICS
# --------------------------------------------------

stats = get_dashboard_statistics()

performance_data = calculate_performance_scores()

training_data = get_training_statistics()

injury_data = get_injury_statistics()

match_data = get_match_list()


performance_df = pd.DataFrame(
    performance_data
)

training_df = pd.DataFrame(
    training_data
)

injury_df = pd.DataFrame(
    injury_data
)

match_df = pd.DataFrame(
    match_data
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("Squad Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Players",
        stats["players"],
    )

with col2:

    st.metric(
        "Teams",
        stats["teams"],
    )

with col3:

    st.metric(
        "Matches",
        stats["matches"],
    )

with col4:

    st.metric(
        "Available Players",
        stats["available_players"],
    )


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Active Injuries",
        stats["active_injuries"],
    )

with col2:

    st.metric(
        "Training Sessions",
        stats["training_sessions"],
    )

with col3:

    st.metric(
        "Equipment",
        stats["equipment"],
    )

with col4:

    if not performance_df.empty:

        average_performance = (
            performance_df["performance_score"].mean()
        )

        st.metric(
            "Avg Performance Score",
            f"{average_performance:.2f}",
        )

    else:

        st.metric(
            "Avg Performance Score",
            "N/A",
        )


st.divider()


# --------------------------------------------------
# PERFORMANCE SECTION
# --------------------------------------------------

st.subheader("📊 Player Performance")

if not performance_df.empty:

    performance_chart_df = (
        performance_df[
            [
                "player_name",
                "performance_score",
            ]
        ]
        .sort_values(
            "performance_score",
            ascending=True,
        )
    )

    fig_performance = px.bar(
        performance_chart_df,
        x="performance_score",
        y="player_name",
        orientation="h",
        title="Player Performance Scores",
        labels={
            "performance_score": "Performance Score",
            "player_name": "Player",
        },
    )

    fig_performance.update_layout(
        height=450,
    )

    st.plotly_chart(
        fig_performance,
        width="stretch",
    )

else:

    st.info("No performance data available.")


st.divider()


# --------------------------------------------------
# PERFORMANCE + CONFIDENCE
# --------------------------------------------------

st.subheader(
    "🎯 Performance Score vs Data Confidence"
)

if not performance_df.empty:

    confidence_order = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
    }

    performance_df["confidence_level"] = (
        performance_df["confidence_label"]
        .map(confidence_order)
    )

    fig_confidence = px.scatter(
        performance_df,
        x="confidence_level",
        y="performance_score",
        text="player_name",
        size="performance_score",
        title="Performance Score and Data Confidence",
        labels={
            "confidence_level": "Confidence Level",
            "performance_score": "Performance Score",
        },
    )

    fig_confidence.update_xaxes(
        tickmode="array",
        tickvals=[1, 2, 3],
        ticktext=[
            "Low",
            "Medium",
            "High",
        ],
    )

    fig_confidence.update_traces(
        textposition="top center"
    )

    fig_confidence.update_layout(
        height=450,
    )

    st.plotly_chart(
        fig_confidence,
        width="stretch",
    )

else:

    st.info("No performance data available.")


st.divider()


# --------------------------------------------------
# TRAINING SECTION
# --------------------------------------------------

st.subheader("🏋️ Training Workload")

if not training_df.empty:

    workload_df = (
        training_df[
            [
                "player_name",
                "average_workload",
            ]
        ]
        .sort_values(
            "average_workload",
            ascending=False,
        )
    )

    fig_workload = px.bar(
        workload_df,
        x="player_name",
        y="average_workload",
        title="Average Training Workload",
        labels={
            "player_name": "Player",
            "average_workload": "Average Workload",
        },
    )

    fig_workload.update_layout(
        height=400,
    )

    st.plotly_chart(
        fig_workload,
        width="stretch",
    )

else:

    st.info("No training data available.")


st.divider()


# --------------------------------------------------
# AVAILABILITY SECTION
# --------------------------------------------------

st.subheader("🩹 Player Availability")

if not injury_df.empty:

    availability_counts = (
        injury_df[
            "availability_status"
        ]
        .value_counts()
        .rename_axis("Status")
        .reset_index(
            name="Players"
        )
    )

    fig_availability = px.pie(
        availability_counts,
        names="Status",
        values="Players",
        title="Current Player Availability",
        hole=0.45,
    )

    fig_availability.update_layout(
        height=400,
    )

    st.plotly_chart(
        fig_availability,
        width="stretch",
    )

else:

    st.info("No injury data available.")


st.divider()


# --------------------------------------------------
# MATCH RESULTS
# --------------------------------------------------

st.subheader("🏏 Match Results")

if not match_df.empty:

    result_counts = (
        match_df[
            "result"
        ]
        .value_counts()
        .rename_axis("Result")
        .reset_index(
            name="Matches"
        )
    )

    fig_results = px.bar(
        result_counts,
        x="Result",
        y="Matches",
        title="Match Result Distribution",
        labels={
            "Result": "Result",
            "Matches": "Number of Matches",
        },
    )

    fig_results.update_layout(
        height=350,
    )

    st.plotly_chart(
        fig_results,
        width="stretch",
    )

else:

    st.info("No match data available.")


st.divider()


# --------------------------------------------------
# TOP PERFORMERS TABLE
# --------------------------------------------------

st.subheader("⭐ Player Performance Summary")

if not performance_df.empty:

    top_players = (
        performance_df[
            [
                "player_name",
                "role",
                "performance_score",
                "confidence_label",
            ]
        ]
        .sort_values(
            "performance_score",
            ascending=False,
        )
        .copy()
    )

    top_players.columns = [
        "Player",
        "Role",
        "Performance Score",
        "Confidence",
    ]

    st.dataframe(
        top_players,
        hide_index=True,
        width="stretch",
    )


st.divider()


# --------------------------------------------------
# PLATFORM STATUS
# --------------------------------------------------

st.subheader("System Status")

col1, col2, col3 = st.columns(3)

with col1:

    st.success(
        "Database Connected"
    )

with col2:

    st.success(
        "Analytics Engine Active"
    )

with col3:

    st.success(
        "Streamlit Application Active"
    )


st.caption(
    "Cricket Sports Performance & Operations Intelligence Platform"
)