from analytics.batting import (
    get_batting_statistics,
    get_batting_consistency,
)

from analytics.bowling import (
    get_bowling_statistics,
    get_bowling_consistency,
)

from analytics.training import get_training_statistics

from database.connection import SessionLocal
from database.models import Player


def normalize(value, minimum, maximum, reverse=False):
    """
    Convert a metric to a 0-100 scale.
    """

    if maximum == minimum:
        return 50.0

    score = (
        (value - minimum)
        / (maximum - minimum)
    ) * 100

    if reverse:
        score = 100 - score

    return max(0, min(100, score))


def calculate_data_confidence(
    batting_matches,
    bowling_matches,
    training_sessions,
    role,
):
    """
    Estimate how much data is available for evaluating a player.

    This is NOT a performance score.
    It tells us how much evidence supports the score.
    """

    if role in ["Batter", "Wicketkeeper"]:

        if batting_matches == 0:
            return 25

        elif batting_matches == 1:
            return 50

        elif batting_matches == 2:
            return 75

        else:
            return 100

    elif role == "Bowler":

        if bowling_matches == 0:
            return 25

        elif bowling_matches == 1:
            return 50

        elif bowling_matches == 2:
            return 75

        else:
            return 100

    elif role == "All-rounder":

        batting_confidence = min(
            batting_matches / 3,
            1,
        )

        bowling_confidence = min(
            bowling_matches / 3,
            1,
        )

        combined = (
            (batting_confidence + bowling_confidence)
            / 2
        )

        return round(combined * 100, 2)

    return 25


def calculate_performance_scores():
    """
    Calculate role-aware player performance scores.

    Returns:
        list[dict]: Performance information for all players.
    """

    batting_data = get_batting_statistics()
    bowling_data = get_bowling_statistics()
    training_data = get_training_statistics()

    batting = {
        player["player_id"]: player
        for player in batting_data
    }

    bowling = {
        player["player_id"]: player
        for player in bowling_data
    }

    training = {
        player["player_id"]: player
        for player in training_data
    }

    # --------------------------------------------------
    # GET PLAYER ROLES
    # --------------------------------------------------

    session = SessionLocal()

    try:
        players = session.query(Player).all()

        player_roles = {
            player.player_id: player.role
            for player in players
        }

        player_names = {
            player.player_id: player.name
            for player in players
        }

    finally:
        session.close()

    results = []

    for player_id in player_roles:

        role = player_roles[player_id]

        # --------------------------------------------------
        # CONSISTENCY METRICS
        # --------------------------------------------------

        batting_consistency = get_batting_consistency(
            player_id
        )

        bowling_consistency = get_bowling_consistency(
            player_id
        )

        batting_stats = batting.get(
            player_id,
            {},
        )

        bowling_stats = bowling.get(
            player_id,
            {},
        )

        training_stats = training.get(
            player_id,
            {},
        )

        # --------------------------------------------------
        # RAW METRICS
        # --------------------------------------------------

        runs = batting_stats.get(
            "total_runs",
            0,
        )

        strike_rate = batting_stats.get(
            "strike_rate",
            0,
        )

        batting_average = batting_stats.get(
            "batting_average",
            0,
        )

        wickets = bowling_stats.get(
            "wickets",
            0,
        )

        economy_rate = bowling_stats.get(
            "economy_rate",
            0,
        )

        dot_ball_percentage = bowling_stats.get(
            "dot_ball_percentage",
            0,
        )

        attendance = training_stats.get(
            "attendance_percentage",
            0,
        )

        fitness = training_stats.get(
            "average_fitness",
            0,
        )

        batting_matches = batting_stats.get(
            "matches",
            0,
        )

        bowling_matches = bowling_stats.get(
            "matches",
            0,
        )

        training_sessions = training_stats.get(
            "total_sessions",
            0,
        )

        # --------------------------------------------------
        # BATTING SCORE
        # --------------------------------------------------

        batting_score = 0

        if batting_matches > 0:

            batting_components = [
                normalize(
                    runs,
                    0,
                    200,
                ),
                normalize(
                    strike_rate,
                    80,
                    180,
                ),
                normalize(
                    batting_average,
                    0,
                    80,
                ),
            ]

            batting_score = (
                sum(batting_components)
                / len(batting_components)
            )

        # --------------------------------------------------
        # BOWLING SCORE
        # --------------------------------------------------

        bowling_score = 0

        if bowling_matches > 0:

            bowling_components = [
                normalize(
                    wickets,
                    0,
                    10,
                ),
                normalize(
                    economy_rate,
                    12,
                    4,
                    reverse=True,
                ),
                normalize(
                    dot_ball_percentage,
                    0,
                    50,
                ),
            ]

            bowling_score = (
                sum(bowling_components)
                / len(bowling_components)
            )

        # --------------------------------------------------
        # TRAINING SCORE
        # --------------------------------------------------

        training_score = 0

        if training_sessions > 0:

            training_components = [
                normalize(
                    attendance,
                    0,
                    100,
                ),
                normalize(
                    fitness,
                    1,
                    5,
                ),
            ]

            training_score = (
                sum(training_components)
                / len(training_components)
            )

        # --------------------------------------------------
        # ROLE-BASED WEIGHTS
        # --------------------------------------------------

        if role == "All-rounder":

            batting_weight = 0.35
            bowling_weight = 0.35
            training_weight = 0.30

        elif role == "Bowler":

            batting_weight = 0.00
            bowling_weight = 0.60
            training_weight = 0.40

        elif role in ["Batter", "Wicketkeeper"]:

            batting_weight = 0.60
            bowling_weight = 0.00
            training_weight = 0.40

        else:

            batting_weight = 0.00
            bowling_weight = 0.00
            training_weight = 1.00

        # --------------------------------------------------
        # FINAL PERFORMANCE SCORE
        # --------------------------------------------------

        performance_score = (
            batting_score * batting_weight
            + bowling_score * bowling_weight
            + training_score * training_weight
        )

        # --------------------------------------------------
        # DATA CONFIDENCE
        # --------------------------------------------------

        confidence = calculate_data_confidence(
            batting_matches,
            bowling_matches,
            training_sessions,
            role,
        )

        # --------------------------------------------------
        # CONFIDENCE LABEL
        # --------------------------------------------------

        if confidence >= 75:
            confidence_label = "High"

        elif confidence >= 50:
            confidence_label = "Medium"

        else:
            confidence_label = "Low"

        # --------------------------------------------------
        # FINAL RESULT
        # --------------------------------------------------

        results.append(
            {
                "player_id": player_id,
                "player_name": player_names[player_id],
                "role": role,

                "batting_score": round(
                    batting_score,
                    2,
                ),

                "bowling_score": round(
                    bowling_score,
                    2,
                ),

                "training_score": round(
                    training_score,
                    2,
                ),

                "performance_score": round(
                    performance_score,
                    2,
                ),

                "data_confidence": confidence,

                "confidence_label": confidence_label,

                "batting_matches": batting_matches,

                "bowling_matches": bowling_matches,

                "training_sessions": training_sessions,

                # New consistency metrics
                "batting_consistency": (
                    batting_consistency[
                        "consistency_score"
                    ]
                ),

                "bowling_consistency": (
                    bowling_consistency[
                        "consistency_score"
                    ]
                ),
            }
        )

    # Sort by performance score

    results.sort(
        key=lambda player: player["performance_score"],
        reverse=True,
    )

    return results

def get_workload_vs_performance():
    """
    Compare training workload with player performance.

    Returns:
        list[dict]: Workload and performance information.
    """

    training_statistics = get_training_statistics()

    performance_scores = (
        calculate_performance_scores()
    )

    # Create lookup dictionaries

    training_by_player = {
        player["player_id"]: player
        for player in training_statistics
    }

    performance_by_player = {
        player["player_id"]: player
        for player in performance_scores
    }

    results = []

    for player_id in performance_by_player:

        performance = performance_by_player[player_id]

        training = training_by_player.get(
            player_id,
            {},
        )

        # Determine workload status

        average_workload = training.get(
            "average_workload",
            0,
        )

        all_workloads = [
            player.get("average_workload", 0)
            for player in training_statistics
        ]

        if all_workloads:

            overall_average = (
                sum(all_workloads)
                / len(all_workloads)
            )

        else:

            overall_average = 0

        if overall_average > 0:

            if average_workload >= (
                overall_average * 1.15
            ):

                workload_status = "High"

            elif average_workload <= (
                overall_average * 0.85
            ):

                workload_status = "Low"

            else:

                workload_status = "Moderate"

        else:

            workload_status = "Unknown"

        results.append(
            {
                "player_id": player_id,

                "player_name": performance.get(
                    "player_name"
                ),

                "role": performance.get(
                    "role"
                ),

                "average_workload": average_workload,

                "average_fitness": training.get(
                    "average_fitness",
                    0,
                ),

                "attendance_percentage": training.get(
                    "attendance_percentage",
                    0,
                ),

                "workload_status": workload_status,

                "performance_score": performance.get(
                    "performance_score",
                    0,
                ),

                "data_confidence": performance.get(
                    "data_confidence",
                    0,
                ),

                "confidence_label": performance.get(
                    "confidence_label",
                    "Low",
                ),

                "batting_consistency": performance.get(
                    "batting_consistency",
                    0,
                ),

                "bowling_consistency": performance.get(
                    "bowling_consistency",
                    0,
                ),
            }
        )

    return results
if __name__ == "__main__":

    performance = calculate_performance_scores()

    print()
    print("PLAYER PERFORMANCE SCORES")
    print("=" * 100)

    for player in performance:

        print(
            f"{player['player_name']:<20}"
            f" Role: {player['role']:<12}"
            f" Score: {player['performance_score']:>6.2f}"
            f" Confidence: {player['confidence_label']:<7}"
            f" Bat Consistency: {player['batting_consistency']:>6.2f}"
            f" Bowl Consistency: {player['bowling_consistency']:>6.2f}"
        )

    print("=" * 100)