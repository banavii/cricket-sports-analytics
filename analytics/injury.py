from datetime import date

from sqlalchemy import func

from database.connection import SessionLocal
from database.models import Player, Injury


def get_injury_statistics():
    """
    Calculate injury and player availability statistics.

    Returns:
        list[dict]: Injury statistics for every player.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Player.player_id,
                Player.name,
                func.count(Injury.injury_id).label(
                    "total_injuries"
                ),
            )
            .outerjoin(
                Injury,
                Player.player_id == Injury.player_id,
            )
            .group_by(
                Player.player_id,
                Player.name,
            )
            .all()
        )

        statistics = []

        for row in results:

            total_injuries = row.total_injuries or 0

            # Get all injuries for this player
            injuries = (
                session.query(Injury)
                .filter(
                    Injury.player_id == row.player_id
                )
                .all()
            )

            recovered = 0
            recovering = 0
            severe_injuries = 0

            total_recovery_days = 0
            recovery_cases = 0

            for injury in injuries:

                # Recovery status
                if injury.recovery_status == "Recovered":
                    recovered += 1

                elif injury.recovery_status == "Recovering":
                    recovering += 1

                # Severity
                if injury.severity in [
                    "Severe",
                    "Critical",
                ]:
                    severe_injuries += 1

                # Recovery duration
                if (
                    injury.actual_return
                    and injury.injury_date
                ):
                    recovery_days = (
                        injury.actual_return
                        - injury.injury_date
                    ).days

                    total_recovery_days += recovery_days
                    recovery_cases += 1

            # Average recovery time
            if recovery_cases > 0:
                average_recovery_days = (
                    total_recovery_days
                    / recovery_cases
                )
            else:
                average_recovery_days = 0

            # Current availability
            current_injury = any(
                injury.recovery_status
                == "Recovering"
                for injury in injuries
            )

            if current_injury:
                availability_status = "Unavailable"
            else:
                availability_status = "Available"

            statistics.append(
                {
                    "player_id": row.player_id,
                    "player_name": row.name,
                    "total_injuries": total_injuries,
                    "recovered_injuries": recovered,
                    "recovering_injuries": recovering,
                    "severe_injuries": severe_injuries,
                    "average_recovery_days": round(
                        average_recovery_days,
                        2,
                    ),
                    "availability_status": availability_status,
                }
            )

        return statistics

    finally:
        session.close()


if __name__ == "__main__":

    statistics = get_injury_statistics()

    print()
    print("PLAYER INJURY & AVAILABILITY")
    print("=" * 80)

    for player in statistics:

        print(
            f"{player['player_name']:<20}"
            f" Injuries: {player['total_injuries']:>2}"
            f" Recovered: {player['recovered_injuries']:>2}"
            f" Recovering: {player['recovering_injuries']:>2}"
            f" Avg Recovery: "
            f"{player['average_recovery_days']:>6.1f} days"
            f" Status: {player['availability_status']}"
        )

    print("=" * 80)