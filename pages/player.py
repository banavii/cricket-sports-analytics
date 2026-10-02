import streamlit as st

from database.connection import SessionLocal
from database.models import Player, Team

from analytics.player_profile import get_player_profile


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