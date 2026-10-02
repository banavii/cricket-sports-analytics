import streamlit as st
import pandas as pd

from analytics.injury import get_injury_statistics


st.set_page_config(
    page_title="Injury & Availability",
    page_icon="🩹",
    layout="wide",
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🩹 Injury & Availability")

st.markdown(
    "Monitor injury history, recovery, and current player availability."
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

injury_data = get_injury_statistics()

if not injury_data:
    st.warning("No player injury data found.")
    st.stop()


df = pd.DataFrame(injury_data)


# --------------------------------------------------
# OVERALL METRICS
# --------------------------------------------------

st.subheader("Squad Availability")


total_players = len(df)

total_injuries = int(
    df["total_injuries"].sum()
)

recovering_players = int(
    (df["recovering_injuries"] > 0).sum()
)

available_players = int(
    (df["availability_status"] == "Available").sum()
)


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Players",
        total_players,
    )


with col2:
    st.metric(
        "Available",
        available_players,
    )


with col3:
    st.metric(
        "Unavailable",
        recovering_players,
    )


with col4:
    st.metric(
        "Total Injuries",
        total_injuries,
    )


st.divider()


# --------------------------------------------------
# AVAILABILITY STATUS
# --------------------------------------------------

st.subheader("Current Availability")


available_df = df[
    [
        "player_name",
        "total_injuries",
        "recovering_injuries",
        "availability_status",
    ]
].copy()


available_df.columns = [
    "Player",
    "Total Injuries",
    "Recovering",
    "Availability",
]


st.dataframe(
    available_df,
    hide_index=True,
    use_container_width=True,
)


st.divider()


# --------------------------------------------------
# INJURY STATISTICS
# --------------------------------------------------

st.subheader("📊 Injury Statistics")


injury_stats_df = df[
    [
        "player_name",
        "total_injuries",
        "recovered_injuries",
        "recovering_injuries",
        "severe_injuries",
        "average_recovery_days",
    ]
].copy()


injury_stats_df.columns = [
    "Player",
    "Total Injuries",
    "Recovered",
    "Recovering",
    "Severe Injuries",
    "Avg Recovery Days",
]


st.dataframe(
    injury_stats_df,
    hide_index=True,
    use_container_width=True,
)


st.divider()


# --------------------------------------------------
# PLAYER SELECTION
# --------------------------------------------------

st.subheader("Player Injury Profile")


player_names = sorted(
    df["player_name"].tolist()
)


selected_player = st.selectbox(
    "Select Player",
    player_names,
)


player = df[
    df["player_name"] == selected_player
].iloc[0]


# --------------------------------------------------
# PLAYER INJURY METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Injuries",
        int(player["total_injuries"]),
    )


with col2:
    st.metric(
        "Recovered",
        int(player["recovered_injuries"]),
    )


with col3:
    st.metric(
        "Recovering",
        int(player["recovering_injuries"]),
    )


with col4:
    st.metric(
        "Avg Recovery",
        f"{player['average_recovery_days']:.1f} days",
    )


# --------------------------------------------------
# AVAILABILITY MESSAGE
# --------------------------------------------------

if player["availability_status"] == "Available":

    st.success(
        f"{selected_player} is currently available."
    )

else:

    st.warning(
        f"{selected_player} is currently unavailable "
        "due to an ongoing injury."
    )


st.divider()


# --------------------------------------------------
# RECOVERY COMPARISON
# --------------------------------------------------

st.subheader("⏱️ Average Recovery Duration")


recovery_df = df[
    [
        "player_name",
        "average_recovery_days",
    ]
].copy()


recovery_df = recovery_df[
    recovery_df["average_recovery_days"] > 0
]


if not recovery_df.empty:

    recovery_df = recovery_df.sort_values(
        "average_recovery_days",
        ascending=False,
    )

    recovery_chart = recovery_df.set_index(
        "player_name"
    )

    st.bar_chart(
        recovery_chart,
        y="average_recovery_days",
    )

else:

    st.info(
        "No completed injury recoveries are available."
    )


st.divider()


# --------------------------------------------------
# SEVERE INJURIES
# --------------------------------------------------

st.subheader("⚠️ Severe Injury Records")


severe_df = df[
    [
        "player_name",
        "severe_injuries",
    ]
].copy()


severe_df = severe_df[
    severe_df["severe_injuries"] > 0
]


if not severe_df.empty:

    severe_df.columns = [
        "Player",
        "Severe Injuries",
    ]

    st.dataframe(
        severe_df,
        hide_index=True,
        use_container_width=True,
    )

else:

    st.success(
        "No severe or critical injuries recorded."
    )


st.caption(
    "Cricket Sports Performance & Operations Intelligence Platform"
)