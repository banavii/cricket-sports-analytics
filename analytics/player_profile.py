from database.connection import SessionLocal
from database.models import Player, Team

from analytics.batting import get_batting_statistics
from analytics.bowling import get_bowling_statistics
from analytics.training import get_training_statistics
from analytics.performance import calculate_performance_scores
from analytics.injury import get_injury_statistics


def get_player_profile(player_id):
    """
    Combine player information with all available analytics.

    Returns:
        dict: Complete player profile.
    """

    session = SessionLocal()

    try:
        player = (
            session.query(Player)
            .filter(Player.player_id == player_id)
            .first()
        )

        if not player:
            return None

        team = (
            session.query(Team)
            .filter(Team.team_id == player.team_id)
            .first()
        )

        # Get analytics from existing modules
        batting_data = get_batting_statistics()
        bowling_data = get_bowling_statistics()
        training_data = get_training_statistics()
        performance_data = calculate_performance_scores()
        injury_data = get_injury_statistics()

        # Find this player's records
        batting = next(
            (
                item
                for item in batting_data
                if item["player_id"] == player_id
            ),
            None,
        )

        bowling = next(
            (
                item
                for item in bowling_data
                if item["player_id"] == player_id
            ),
            None,
        )

        training = next(
            (
                item
                for item in training_data
                if item["player_id"] == player_id
            ),
            None,
        )

        performance = next(
            (
                item
                for item in performance_data
                if item["player_id"] == player_id
            ),
            None,
        )

        injury = next(
            (
                item
                for item in injury_data
                if item["player_id"] == player_id
            ),
            None,
        )

        profile = {
            "player": {
                "player_id": player.player_id,
                "name": player.name,
                "role": player.role,
                "gender": player.gender,
                "batting_style": player.batting_style,
                "bowling_style": player.bowling_style,
                "status": player.status,
                "team": team.team_name if team else None,
            },

            "batting": batting,

            "bowling": bowling,

            "training": training,

            "performance": performance,

            "injury": injury,
        }

        return profile

    finally:
        session.close()


if __name__ == "__main__":

    player_id = 1

    profile = get_player_profile(player_id)

    if profile is None:
        print("Player not found.")

    else:
        player = profile["player"]

        print()
        print("PLAYER PROFILE")
        print("=" * 80)

        print(f"Name:           {player['name']}")
        print(f"Team:           {player['team']}")
        print(f"Role:           {player['role']}")
        print(f"Gender:         {player['gender']}")
        print(f"Batting Style:  {player['batting_style']}")
        print(f"Bowling Style:  {player['bowling_style']}")
        print(f"Status:         {player['status']}")

        print()
        print("PERFORMANCE")
        print("-" * 80)

        if profile["performance"]:
            performance = profile["performance"]

            print(
                f"Performance Score: "
                f"{performance['performance_score']:.2f}"
            )

            print(
                f"Confidence:        "
                f"{performance['confidence_label']}"
            )

        print()
        print("BATTING")
        print("-" * 80)

        if profile["batting"]:
            batting = profile["batting"]

            print(f"Matches:       {batting['matches']}")
            print(f"Runs:          {batting['total_runs']}")
            print(f"Average:       {batting['batting_average']:.2f}")
            print(f"Strike Rate:   {batting['strike_rate']:.2f}")

        else:
            print("No batting data available.")

        print()
        print("BOWLING")
        print("-" * 80)

        if profile["bowling"]:
            bowling = profile["bowling"]

            print(f"Matches:       {bowling['matches']}")
            print(f"Wickets:       {bowling['wickets']}")
            print(f"Economy:       {bowling['economy_rate']:.2f}")
            print(
                f"Strike Rate:   "
                f"{bowling['bowling_strike_rate']:.2f}"
            )

        else:
            print("No bowling data available.")

        print()
        print("TRAINING")
        print("-" * 80)

        if profile["training"]:
            training = profile["training"]

            print(
                f"Attendance:    "
                f"{training['attendance_percentage']:.2f}%"
            )

            print(
                f"Avg Workload:  "
                f"{training['average_workload']:.2f}"
            )

            print(
                f"Avg Fitness:   "
                f"{training['average_fitness']:.2f}"
            )

        else:
            print("No training data available.")

        print()
        print("INJURY & AVAILABILITY")
        print("-" * 80)

        if profile["injury"]:
            injury = profile["injury"]

            print(
                f"Total Injuries:      "
                f"{injury['total_injuries']}"
            )

            print(
                f"Recovered:           "
                f"{injury['recovered_injuries']}"
            )

            print(
                f"Recovering:          "
                f"{injury['recovering_injuries']}"
            )

            print(
                f"Avg Recovery Days:   "
                f"{injury['average_recovery_days']:.2f}"
            )

            print(
                f"Availability:        "
                f"{injury['availability_status']}"
            )

        else:
            print("No injury data available.")

        print("=" * 80)