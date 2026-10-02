import streamlit as st

from database.connection import SessionLocal
from database.models import Player, Team

from analytics.player_profile import get_player_profile
from analytics.batting import get_batting_trend
from analytics.bowling import get_bowling_trend


st.set_page_config(
    page_title="Player Analytics",
    page_icon="👤",
    layout="wide",
)


# --------------------------------------------------
# DATABASE HELPERS
# --------------------------------------------------

def get_players():
    """Retrieve all players from the database."""

    session = SessionLocal()

    try:
        players = (
            session.query(Player)
            .order_by(Player.name)
            .all()
        )

        return players

    finally:
        session.close()


def get_teams():
    """Retrieve all teams from the database."""

    session = SessionLocal()

    try:
        teams = (
            session.query(Team)
            .order_by(Team.team_name)
            .all()
        )

        return teams

    finally:
        session.close()


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("👤 Player Analytics")

st.markdown(
    "Explore player performance, training, injury, and availability data."
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

players = get_players()
teams = get_teams()


if not players:
    st.warning("No players found in the database.")
    st.stop()


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    team_options = ["All Teams"] + [
        team.team_name
        for team in teams
    ]

    selected_team = st.selectbox(
        "Select Team",
        team_options,
    )


# Filter players by team
if selected_team == "All Teams":

    filtered_players = players

else:

    selected_team_id = next(
        team.team_id
        for team in teams
        if team.team_name == selected_team
    )

    filtered_players = [
        player
        for player in players
        if player.team_id == selected_team_id
    ]


with col2:

    player_options = {
        player.name: player.player_id
        for player in filtered_players
    }

    selected_player_name = st.selectbox(
        "Select Player",
        list(player_options.keys()),
    )


selected_player_id = player_options[
    selected_player_name
]


# --------------------------------------------------
# GET PLAYER PROFILE
# --------------------------------------------------

profile = get_player_profile(
    selected_player_id
)

if profile is None:

    st.error("Unable to load player profile.")

    st.stop()


player = profile["player"]
performance = profile["performance"]
batting = profile["batting"]
bowling = profile["bowling"]
training = profile["training"]
injury = profile["injury"]


st.divider()


# --------------------------------------------------
# PLAYER HEADER
# --------------------------------------------------

st.header(player["name"])

st.write(
    f"**{player['team']}**  •  "
    f"**{player['role']}**  •  "
    f"**{player['status']}**"
)


# --------------------------------------------------
# KEY METRICS
# --------------------------------------------------

st.subheader("Player Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    if performance:

        st.metric(
            "Performance Score",
            f"{performance['performance_score']:.2f}",
        )

    else:

        st.metric(
            "Performance Score",
            "N/A",
        )


with col2:

    if performance:

        st.metric(
            "Confidence",
            performance["confidence_label"],
        )

    else:

        st.metric(
            "Confidence",
            "N/A",
        )


with col3:

    if injury:

        st.metric(
            "Availability",
            injury["availability_status"],
        )

    else:

        st.metric(
            "Availability",
            "Available",
        )


with col4:

    if injury:

        st.metric(
            "Total Injuries",
            injury["total_injuries"],
        )

    else:

        st.metric(
            "Total Injuries",
            0,
        )


st.divider()


# --------------------------------------------------
# PLAYER INFORMATION
# --------------------------------------------------

st.subheader("Player Information")

col1, col2, col3 = st.columns(3)

with col1:

    st.write(
        f"**Role:** {player['role']}"
    )

    st.write(
        f"**Gender:** {player['gender']}"
    )


with col2:

    st.write(
        f"**Batting Style:** "
        f"{player['batting_style'] or 'N/A'}"
    )

    st.write(
        f"**Bowling Style:** "
        f"{player['bowling_style'] or 'N/A'}"
    )


with col3:

    st.write(
        f"**Team:** {player['team']}"
    )

    st.write(
        f"**Status:** {player['status']}"
    )


st.divider()


# --------------------------------------------------
# BATTING
# --------------------------------------------------

st.subheader("🏏 Batting Performance")

if batting:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Matches",
            batting["matches"],
        )

    with col2:
        st.metric(
            "Runs",
            batting["total_runs"],
        )

    with col3:
        st.metric(
            "Average",
            f"{batting['batting_average']:.2f}",
        )

    with col4:
        st.metric(
            "Strike Rate",
            f"{batting['strike_rate']:.2f}",
        )

else:

    st.info("No batting data available.")


# --------------------------------------------------
# BOWLING
# --------------------------------------------------

st.subheader("🎯 Bowling Performance")

if bowling:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Matches",
            bowling["matches"],
        )

    with col2:
        st.metric(
            "Wickets",
            bowling["wickets"],
        )

    with col3:
        st.metric(
            "Economy",
            f"{bowling['economy_rate']:.2f}",
        )

    with col4:
        st.metric(
            "Bowling SR",
            f"{bowling['bowling_strike_rate']:.2f}",
        )

else:

    st.info("No bowling data available.")

# --------------------------------------------------
# PERFORMANCE TRENDS
# --------------------------------------------------

st.divider()

st.subheader("📈 Performance Trends")


# --------------------------------------------------
# BATTING TREND
# --------------------------------------------------

if batting:

    batting_trend = get_batting_trend(
        selected_player_id
    )

    if batting_trend:

        st.markdown("### 🏏 Batting Trend")

        import pandas as pd
        import plotly.graph_objects as go

        batting_df = pd.DataFrame(
            batting_trend
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=batting_df["match_id"],
                y=batting_df["runs"],
                mode="lines+markers",
                name="Runs",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=batting_df["match_id"],
                y=batting_df["strike_rate"],
                mode="lines+markers",
                name="Strike Rate",
                yaxis="y2",
            )
        )

        fig.update_layout(
            title="Batting Performance by Match",
            xaxis_title="Match",
            yaxis=dict(
                title="Runs",
            ),
            yaxis2=dict(
                title="Strike Rate",
                overlaying="y",
                side="right",
            ),
            hovermode="x unified",
            height=450,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info(
            "No batting trend data available."
        )


# --------------------------------------------------
# BOWLING TREND
# --------------------------------------------------

if bowling:

    bowling_trend = get_bowling_trend(
        selected_player_id
    )

    if bowling_trend:

        st.markdown("### 🎯 Bowling Trend")

        bowling_df = pd.DataFrame(
            bowling_trend
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=bowling_df["match_id"],
                y=bowling_df["wickets"],
                name="Wickets",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=bowling_df["match_id"],
                y=bowling_df["economy_rate"],
                mode="lines+markers",
                name="Economy Rate",
                yaxis="y2",
            )
        )

        fig.update_layout(
            title="Bowling Performance by Match",
            xaxis_title="Match",
            yaxis=dict(
                title="Wickets",
            ),
            yaxis2=dict(
                title="Economy Rate",
                overlaying="y",
                side="right",
            ),
            hovermode="x unified",
            height=450,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:

        st.info(
            "No bowling trend data available."
        )
# --------------------------------------------------
# TRAINING
# --------------------------------------------------

st.subheader("🏋️ Training & Fitness")

if training:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Attendance",
            f"{training['attendance_percentage']:.1f}%",
        )

    with col2:
        st.metric(
            "Sessions",
            training["total_sessions"],
        )

    with col3:
        st.metric(
            "Avg Workload",
            f"{training['average_workload']:.1f}",
        )

    with col4:
        st.metric(
            "Avg Fitness",
            f"{training['average_fitness']:.1f}",
        )

else:

    st.info("No training data available.")


# --------------------------------------------------
# INJURY
# --------------------------------------------------

st.subheader("🩹 Injury & Availability")

if injury:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Injuries",
            injury["total_injuries"],
        )

    with col2:
        st.metric(
            "Recovered",
            injury["recovered_injuries"],
        )

    with col3:
        st.metric(
            "Recovering",
            injury["recovering_injuries"],
        )

    with col4:
        st.metric(
            "Avg Recovery",
            f"{injury['average_recovery_days']:.1f} days",
        )

    if injury["availability_status"] == "Available":

        st.success("Player is currently available.")

    else:

        st.warning(
            "Player is currently unavailable due to injury."
        )

else:

    st.success("No injury records found.")


st.divider()

st.caption(
    "Cricket Sports Performance & Operations Intelligence Platform"
)