import streamlit as st
import pandas as pd

from analytics.training import get_training_statistics


st.set_page_config(
    page_title="Training & Workload",
    page_icon="🏋️",
    layout="wide",
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🏋️ Training & Workload")

st.markdown(
    "Monitor training attendance, workload, and fitness "
    "across the squad."
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

training_data = get_training_statistics()


if not training_data:
    st.warning("No training data found.")
    st.stop()


df = pd.DataFrame(training_data)


# --------------------------------------------------
# OVERALL METRICS
# --------------------------------------------------

st.subheader("Training Overview")


total_sessions = df["total_sessions"].max()

average_attendance = df[
    "attendance_percentage"
].mean()

average_workload = df[
    "average_workload"
].mean()

average_fitness = df[
    "average_fitness"
].mean()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Training Sessions",
        int(total_sessions),
    )


with col2:
    st.metric(
        "Average Attendance",
        f"{average_attendance:.1f}%",
    )


with col3:
    st.metric(
        "Average Workload",
        f"{average_workload:.1f}",
    )


with col4:
    st.metric(
        "Average Fitness",
        f"{average_fitness:.1f}",
    )


st.divider()


# --------------------------------------------------
# PLAYER SELECTION
# --------------------------------------------------

st.subheader("Player Training Profile")


player_names = sorted(
    df["player_name"].tolist()
)


selected_player = st.selectbox(
    "Select Player",
    player_names,
)


player_data = df[
    df["player_name"] == selected_player
].iloc[0]


# --------------------------------------------------
# SELECTED PLAYER METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Sessions",
        int(player_data["total_sessions"]),
    )


with col2:
    st.metric(
        "Attendance",
        f"{player_data['attendance_percentage']:.1f}%",
    )


with col3:
    st.metric(
        "Average Workload",
        f"{player_data['average_workload']:.1f}",
    )


with col4:
    st.metric(
        "Average Fitness",
        f"{player_data['average_fitness']:.1f}",
    )


st.divider()


# --------------------------------------------------
# PLAYER TRAINING TABLE
# --------------------------------------------------

st.subheader("📋 Training Statistics")


display_df = df[
    [
        "player_name",
        "total_sessions",
        "sessions_attended",
        "sessions_missed",
        "attendance_percentage",
        "total_workload",
        "average_workload",
        "average_fitness",
    ]
].copy()


display_df.columns = [
    "Player",
    "Sessions",
    "Attended",
    "Missed",
    "Attendance %",
    "Total Workload",
    "Avg Workload",
    "Avg Fitness",
]


st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
)


st.divider()


# --------------------------------------------------
# WORKLOAD COMPARISON
# --------------------------------------------------

st.subheader("📊 Average Workload by Player")


workload_df = df[
    [
        "player_name",
        "average_workload",
    ]
].copy()


workload_df = workload_df.sort_values(
    "average_workload",
    ascending=False,
)


workload_chart = workload_df.set_index(
    "player_name"
)


st.bar_chart(
    workload_chart,
    y="average_workload",
)


st.divider()


# --------------------------------------------------
# ATTENDANCE COMPARISON
# --------------------------------------------------

st.subheader("📅 Attendance by Player")


attendance_df = df[
    [
        "player_name",
        "attendance_percentage",
    ]
].copy()


attendance_df = attendance_df.sort_values(
    "attendance_percentage",
    ascending=False,
)


attendance_chart = attendance_df.set_index(
    "player_name"
)


st.bar_chart(
    attendance_chart,
    y="attendance_percentage",
)


st.divider()


# --------------------------------------------------
# FITNESS COMPARISON
# --------------------------------------------------

st.subheader("💪 Average Fitness Rating")


fitness_df = df[
    [
        "player_name",
        "average_fitness",
    ]
].copy()


fitness_df = fitness_df.sort_values(
    "average_fitness",
    ascending=False,
)


fitness_chart = fitness_df.set_index(
    "player_name"
)


st.bar_chart(
    fitness_chart,
    y="average_fitness",
)


st.divider()


st.caption(
    "Cricket Sports Performance & Operations Intelligence Platform"
)