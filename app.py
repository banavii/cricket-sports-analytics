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

from analytics.performance import (
    calculate_performance_scores,
    get_workload_vs_performance,
)

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
    """Get high-level statistics for the dashboard."""

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
# PLAYER PERFORMANCE
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

    st.info(
        "No performance data available."
    )


st.divider()

# ============================================================
# PLAYER CONSISTENCY ANALYSIS
# ============================================================

st.subheader("Player Consistency Analysis")

consistency_data = calculate_performance_scores()

consistency_df = pd.DataFrame(
    consistency_data
)

if not consistency_df.empty:

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Batting Consistency
    # --------------------------------------------------------

    with col1:

        st.markdown("### Batting Consistency")

        batting_consistency_df = (
            consistency_df[
                consistency_df["batting_consistency"] > 0
            ]
            .sort_values(
                "batting_consistency",
                ascending=False,
            )
        )

        if not batting_consistency_df.empty:

            fig_batting_consistency = px.bar(
                batting_consistency_df,
                x="player_name",
                y="batting_consistency",
                text="batting_consistency",
                hover_data={
                    "player_name": True,
                    "role": True,
                    "batting_consistency": ":.2f",
                    "performance_score": ":.2f",
                    "data_confidence": ":.1f",
                },
                labels={
                    "player_name": "Player",
                    "batting_consistency": (
                        "Batting Consistency"
                    ),
                    "performance_score": (
                        "Performance Score"
                    ),
                    "data_confidence": (
                        "Data Confidence"
                    ),
                    "role": "Role",
                },
            )

            fig_batting_consistency.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
            )

            fig_batting_consistency.update_layout(
                yaxis_title="Consistency Score",
                xaxis_title="Player",
                yaxis_range=[0, 100],
            )

            st.plotly_chart(
                fig_batting_consistency,
                use_container_width=True,
            )

        else:

            st.info(
                "No batting consistency data available."
            )

    # --------------------------------------------------------
    # Bowling Consistency
    # --------------------------------------------------------

    with col2:

        st.markdown("### Bowling Consistency")

        bowling_consistency_df = (
            consistency_df[
                consistency_df["bowling_consistency"] > 0
            ]
            .sort_values(
                "bowling_consistency",
                ascending=False,
            )
        )

        if not bowling_consistency_df.empty:

            fig_bowling_consistency = px.bar(
                bowling_consistency_df,
                x="player_name",
                y="bowling_consistency",
                text="bowling_consistency",
                hover_data={
                    "player_name": True,
                    "role": True,
                    "bowling_consistency": ":.2f",
                    "performance_score": ":.2f",
                    "data_confidence": ":.1f",
                },
                labels={
                    "player_name": "Player",
                    "bowling_consistency": (
                        "Bowling Consistency"
                    ),
                    "performance_score": (
                        "Performance Score"
                    ),
                    "data_confidence": (
                        "Data Confidence"
                    ),
                    "role": "Role",
                },
            )

            fig_bowling_consistency.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside",
            )

            fig_bowling_consistency.update_layout(
                yaxis_title="Consistency Score",
                xaxis_title="Player",
                yaxis_range=[0, 100],
            )

            st.plotly_chart(
                fig_bowling_consistency,
                use_container_width=True,
            )

        else:

            st.info(
                "No bowling consistency data available."
            )

    # --------------------------------------------------------
    # Consistency Summary Table
    # --------------------------------------------------------

    st.markdown("### Consistency Summary")

    consistency_table = consistency_df[
        [
            "player_name",
            "role",
            "performance_score",
            "batting_consistency",
            "bowling_consistency",
            "data_confidence",
        ]
    ].copy()

    consistency_table = consistency_table.rename(
        columns={
            "player_name": "Player",
            "role": "Role",
            "performance_score": (
                "Performance Score"
            ),
            "batting_consistency": (
                "Batting Consistency"
            ),
            "bowling_consistency": (
                "Bowling Consistency"
            ),
            "data_confidence": (
                "Data Confidence"
            ),
        }
    )

    st.dataframe(
        consistency_table,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Consistency scores measure match-to-match "
        "variation in batting and bowling performance. "
        "They are descriptive project metrics and should "
        "be interpreted together with data confidence."
    )

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

    st.info(
        "No performance data available."
    )


st.divider()


# --------------------------------------------------
# TRAINING WORKLOAD
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

    st.info(
        "No training data available."
    )


st.divider()


# --------------------------------------------------
# WORKLOAD VS PERFORMANCE
# --------------------------------------------------

st.subheader(
    "🏋️ Training Workload vs Performance"
)

workload_data = get_workload_vs_performance()

if workload_data:

    workload_performance_df = pd.DataFrame(
        workload_data
    )

    fig_workload_performance = px.scatter(
        workload_performance_df,
        x="average_workload",
        y="performance_score",
        size="data_confidence",
        color="role",
        hover_name="player_name",
        hover_data={
            "average_workload": ":.1f",
            "performance_score": ":.2f",
            "average_fitness": ":.1f",
            "attendance_percentage": ":.1f",
            "data_confidence": ":.1f",
            "role": True,
            "workload_status": True,
        },
        labels={
            "average_workload": "Average Training Workload",
            "performance_score": "Performance Score",
            "average_fitness": "Average Fitness",
            "attendance_percentage": "Attendance",
            "data_confidence": "Data Confidence",
            "role": "Role",
            "workload_status": "Workload Status",
        },
        title="Training Workload vs Player Performance",
    )

    fig_workload_performance.update_layout(
        height=500,
    )

    st.plotly_chart(
        fig_workload_performance,
        width="stretch",
    )

else:

    st.info(
        "No workload or performance data available."
    )


st.divider()


# --------------------------------------------------
# PLAYER AVAILABILITY
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

    st.info(
        "No injury data available."
    )


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

    st.info(
        "No match data available."
    )


st.divider()


# --------------------------------------------------
# TOP PERFORMERS TABLE
# --------------------------------------------------

st.subheader(
    "⭐ Player Performance Summary"
)

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

else:

    st.info(
        "No player performance data available."
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


st.divider()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "Cricket Sports Performance & Operations Intelligence Platform"
)