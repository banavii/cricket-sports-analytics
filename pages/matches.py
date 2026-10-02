import streamlit as st
import pandas as pd

from analytics.matches import (
    get_match_list,
    get_match_summary,
)


st.set_page_config(
    page_title="Match Analytics",
    page_icon="🏏",
    layout="wide",
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🏏 Match Analytics")

st.markdown(
    "Explore match results, scores, batting performances, "
    "and bowling performances."
)

st.divider()


# --------------------------------------------------
# LOAD MATCHES
# --------------------------------------------------

matches = get_match_list()

if not matches:
    st.warning("No matches found in the database.")
    st.stop()


# --------------------------------------------------
# MATCH SELECTION
# --------------------------------------------------

match_labels = {}

for match in matches:

    label = (
        f"{match['match_date']} — "
        f"{match['team']} vs {match['opponent']}"
    )

    match_labels[label] = match["match_id"]


selected_match_label = st.selectbox(
    "Select Match",
    list(match_labels.keys()),
)


selected_match_id = match_labels[
    selected_match_label
]


# --------------------------------------------------
# GET MATCH SUMMARY
# --------------------------------------------------

summary = get_match_summary(
    selected_match_id
)

if summary is None:
    st.error("Unable to load match information.")
    st.stop()


match = summary["match"]
batting = summary["batting"]
bowling = summary["bowling"]


# --------------------------------------------------
# MATCH HEADER
# --------------------------------------------------

st.divider()

st.header(
    f"{match['team']} vs {match['opponent']}"
)

st.write(
    f"**{match['competition']}** • "
    f"{match['match_type']} • "
    f"{match['venue']}"
)


# --------------------------------------------------
# MATCH INFORMATION
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Date",
        str(match["match_date"]),
    )

with col2:
    st.metric(
        "Result",
        match["result"],
    )

with col3:
    st.metric(
        match["team"],
        match["team_score"],
    )

with col4:
    st.metric(
        match["opponent"],
        match["opponent_score"],
    )


st.divider()


# --------------------------------------------------
# SCORE SUMMARY
# --------------------------------------------------

st.subheader("📊 Score Summary")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        f"### {match['team']}"
    )

    st.metric(
        "Score",
        match["team_score"],
    )


with col2:

    st.markdown(
        f"### {match['opponent']}"
    )

    st.metric(
        "Score",
        match["opponent_score"],
    )


st.divider()


# --------------------------------------------------
# BATTING
# --------------------------------------------------

st.subheader("🏏 Batting Performances")

if batting:

    batting_df = pd.DataFrame(batting)

    batting_df = batting_df[
        [
            "player_name",
            "role",
            "runs",
            "balls",
            "strike_rate",
            "fours",
            "sixes",
            "dismissal_type",
        ]
    ]

    batting_df.columns = [
        "Player",
        "Role",
        "Runs",
        "Balls",
        "Strike Rate",
        "4s",
        "6s",
        "Dismissal",
    ]

    st.dataframe(
        batting_df,
        hide_index=True,
        use_container_width=True,
    )

else:

    st.info(
        "No batting performance data available "
        "for this match."
    )


st.divider()


# --------------------------------------------------
# BOWLING
# --------------------------------------------------

st.subheader("🎯 Bowling Performances")

if bowling:

    bowling_df = pd.DataFrame(bowling)

    bowling_df = bowling_df[
        [
            "player_name",
            "role",
            "balls",
            "runs_conceded",
            "wickets",
            "maidens",
            "dot_balls",
            "economy_rate",
        ]
    ]

    bowling_df.columns = [
        "Player",
        "Role",
        "Balls",
        "Runs Conceded",
        "Wickets",
        "Maidens",
        "Dot Balls",
        "Economy",
    ]

    st.dataframe(
        bowling_df,
        hide_index=True,
        use_container_width=True,
    )

else:

    st.info(
        "No bowling performance data available "
        "for this match."
    )


st.divider()


# --------------------------------------------------
# MATCH DETAILS
# --------------------------------------------------

st.subheader("📋 Match Details")

details_col1, details_col2 = st.columns(2)

with details_col1:

    st.write(
        f"**Competition:** {match['competition']}"
    )

    st.write(
        f"**Match Type:** {match['match_type']}"
    )

    st.write(
        f"**Venue:** {match['venue']}"
    )


with details_col2:

    st.write(
        f"**Date:** {match['match_date']}"
    )

    st.write(
        f"**Team:** {match['team']}"
    )

    st.write(
        f"**Opponent:** {match['opponent']}"
    )


st.caption(
    "Cricket Sports Performance & Operations Intelligence Platform"
)