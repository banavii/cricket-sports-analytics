"""Bowling analytics module.

Provides metrics, calculations, and performance evaluation for bowling statistics.
"""
from sqlalchemy import func

from database.connection import SessionLocal
from database.models import Player, BowlingPerformance


def get_bowling_statistics():
    """
    Calculate bowling statistics for every player
    who has bowling performance records.

    Returns:
        list[dict]: Bowling statistics for each player.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Player.player_id,
                Player.name,
                func.sum(BowlingPerformance.balls).label("total_balls"),
                func.sum(BowlingPerformance.runs_conceded).label(
                    "runs_conceded"
                ),
                func.sum(BowlingPerformance.wickets).label("wickets"),
                func.sum(BowlingPerformance.maidens).label("maidens"),
                func.sum(BowlingPerformance.dot_balls).label("dot_balls"),
                func.count(BowlingPerformance.performance_id).label(
                    "matches"
                ),
            )
            .join(
                BowlingPerformance,
                Player.player_id == BowlingPerformance.player_id,
            )
            .group_by(
                Player.player_id,
                Player.name,
            )
            .all()
        )

        statistics = []

        for row in results:

            total_balls = row.total_balls or 0
            runs_conceded = row.runs_conceded or 0
            wickets = row.wickets or 0
            maidens = row.maidens or 0
            dot_balls = row.dot_balls or 0
            matches = row.matches or 0

            # Economy Rate
            # Runs conceded per 6 legal balls
            if total_balls > 0:
                economy_rate = (
                    runs_conceded / total_balls
                ) * 6
            else:
                economy_rate = 0

            # Bowling Average
            # Runs conceded per wicket
            if wickets > 0:
                bowling_average = (
                    runs_conceded / wickets
                )
            else:
                bowling_average = 0

            # Bowling Strike Rate
            # Balls required per wicket
            if wickets > 0:
                bowling_strike_rate = (
                    total_balls / wickets
                )
            else:
                bowling_strike_rate = 0

            # Dot Ball Percentage
            if total_balls > 0:
                dot_ball_percentage = (
                    dot_balls / total_balls
                ) * 100
            else:
                dot_ball_percentage = 0

            statistics.append(
                {
                    "player_id": row.player_id,
                    "player_name": row.name,
                    "matches": matches,
                    "total_balls": total_balls,
                    "runs_conceded": runs_conceded,
                    "wickets": wickets,
                    "maidens": maidens,
                    "dot_balls": dot_balls,
                    "economy_rate": round(
                        economy_rate,
                        2,
                    ),
                    "bowling_average": round(
                        bowling_average,
                        2,
                    ),
                    "bowling_strike_rate": round(
                        bowling_strike_rate,
                        2,
                    ),
                    "dot_ball_percentage": round(
                        dot_ball_percentage,
                        2,
                    ),
                }
            )

        return statistics

    finally:
        session.close()
def get_bowling_trend(player_id):
    """
    Get match-by-match bowling performance for a player.

    Args:
        player_id (int): ID of the player.

    Returns:
        list[dict]: Match-level bowling performance.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                BowlingPerformance.match_id,
                BowlingPerformance.balls,
                BowlingPerformance.runs_conceded,
                BowlingPerformance.wickets,
                BowlingPerformance.maidens,
                BowlingPerformance.dot_balls,
            )
            .filter(
                BowlingPerformance.player_id == player_id
            )
            .order_by(
                BowlingPerformance.match_id
            )
            .all()
        )

        trend = []

        for row in results:

            balls = row.balls or 0
            runs_conceded = row.runs_conceded or 0

            if balls > 0:
                economy_rate = (
                    runs_conceded / balls
                ) * 6
            else:
                economy_rate = 0

            trend.append(
                {
                    "match_id": row.match_id,
                    "balls": balls,
                    "runs_conceded": runs_conceded,
                    "wickets": row.wickets or 0,
                    "maidens": row.maidens or 0,
                    "dot_balls": row.dot_balls or 0,
                    "economy_rate": round(
                        economy_rate,
                        2,
                    ),
                }
            )

        return trend

    finally:
        session.close()

if __name__ == "__main__":

    statistics = get_bowling_statistics()

    for player in statistics:
        print(player)