import streamlit as st
import pandas as pd

from analytics.equipment import (
    get_equipment_list,
    get_equipment_statistics,
)


st.set_page_config(
    page_title="Equipment Management",
    page_icon="🎒",
    layout="wide",
)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🎒 Equipment Management")

st.markdown(
    "Monitor equipment inventory, assignments, condition, "
    "and maintenance status."
)

st.divider()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

equipment_data = get_equipment_list()

if not equipment_data:
    st.warning("No equipment records found.")
    st.stop()


df = pd.DataFrame(equipment_data)

statistics = get_equipment_statistics()


# --------------------------------------------------
# KEY METRICS
# --------------------------------------------------

st.subheader("Equipment Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Equipment",
        statistics["total_equipment"],
    )

with col2:
    st.metric(
        "Assigned",
        statistics["assigned_equipment"],
    )

with col3:
    st.metric(
        "Available",
        statistics["available_equipment"],
    )

with col4:
    st.metric(
        "Maintenance",
        statistics["maintenance_equipment"],
    )

with col5:
    st.metric(
        "Damaged / Poor",
        statistics["damaged_equipment"],
    )


st.divider()


# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("Filter Inventory")

col1, col2, col3 = st.columns(3)


with col1:

    team_options = [
        "All Teams"
    ] + sorted(
        df["team"].dropna().unique().tolist()
    )

    selected_team = st.selectbox(
        "Team",
        team_options,
    )


with col2:

    status_options = [
        "All Statuses"
    ] + sorted(
        df["status"].dropna().unique().tolist()
    )

    selected_status = st.selectbox(
        "Status",
        status_options,
    )


with col3:

    condition_options = [
        "All Conditions"
    ] + sorted(
        df["condition"].dropna().unique().tolist()
    )

    selected_condition = st.selectbox(
        "Condition",
        condition_options,
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()


if selected_team != "All Teams":

    filtered_df = filtered_df[
        filtered_df["team"] == selected_team
    ]


if selected_status != "All Statuses":

    filtered_df = filtered_df[
        filtered_df["status"] == selected_status
    ]


if selected_condition != "All Conditions":

    filtered_df = filtered_df[
        filtered_df["condition"] == selected_condition
    ]


# --------------------------------------------------
# INVENTORY TABLE
# --------------------------------------------------

st.subheader("📋 Equipment Inventory")

display_df = filtered_df[
    [
        "equipment_id",
        "team",
        "equipment_type",
        "brand",
        "model",
        "assigned_player",
        "condition",
        "status",
        "purchase_date",
        "last_maintenance",
        "next_maintenance",
    ]
].copy()


display_df.columns = [
    "ID",
    "Team",
    "Equipment",
    "Brand",
    "Model",
    "Assigned Player",
    "Condition",
    "Status",
    "Purchase Date",
    "Last Maintenance",
    "Next Maintenance",
]


st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
)


st.caption(
    f"Showing {len(filtered_df)} of "
    f"{len(df)} equipment records."
)


st.divider()


# --------------------------------------------------
# EQUIPMENT BY STATUS
# --------------------------------------------------

st.subheader("📊 Equipment Status")


status_counts = (
    df["status"]
    .value_counts()
    .rename_axis("Status")
    .reset_index(name="Equipment Count")
)


st.dataframe(
    status_counts,
    hide_index=True,
    use_container_width=True,
)


st.divider()


# --------------------------------------------------
# EQUIPMENT BY CONDITION
# --------------------------------------------------

st.subheader("🔧 Equipment Condition")


condition_counts = (
    df["condition"]
    .value_counts()
    .rename_axis("Condition")
    .reset_index(name="Equipment Count")
)


st.dataframe(
    condition_counts,
    hide_index=True,
    use_container_width=True,
)


st.divider()


# --------------------------------------------------
# PLAYER ASSIGNMENTS
# --------------------------------------------------

st.subheader("👤 Player Equipment Assignments")


assigned_df = df[
    df["assigned_player"].notna()
].copy()


if not assigned_df.empty:

    assignment_df = assigned_df[
        [
            "assigned_player",
            "equipment_type",
            "brand",
            "model",
            "condition",
            "status",
        ]
    ].copy()

    assignment_df.columns = [
        "Player",
        "Equipment",
        "Brand",
        "Model",
        "Condition",
        "Status",
    ]

    st.dataframe(
        assignment_df,
        hide_index=True,
        use_container_width=True,
    )

else:

    st.info(
        "No equipment is currently assigned to players."
    )


st.divider()


# --------------------------------------------------
# AVAILABLE EQUIPMENT
# --------------------------------------------------

st.subheader("🟢 Available Equipment")


available_df = df[
    df["status"] == "Available"
].copy()


if not available_df.empty:

    available_display = available_df[
        [
            "equipment_type",
            "brand",
            "model",
            "condition",
            "team",
        ]
    ].copy()

    available_display.columns = [
        "Equipment",
        "Brand",
        "Model",
        "Condition",
        "Team",
    ]

    st.dataframe(
        available_display,
        hide_index=True,
        use_container_width=True,
    )

else:

    st.info(
        "No equipment is currently available."
    )


st.caption(
    "Cricket Sports Performance & Operations Intelligence Platform"
)