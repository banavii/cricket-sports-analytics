"""Batting analytics module.

Provides metrics, calculations, and performance evaluation for batting statistics.
"""
from sqlalchemy import func

from database.connection import SessionLocal
from database.models import Player, BattingPerformance


def get_batting_statistics():
    """
    Calculate batting statistics for every player.

    Returns:
        list[dict]: Batting statistics for each player.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Player.player_id,
                Player.name,
                func.sum(BattingPerformance.runs).label("total_runs"),
                func.sum(BattingPerformance.balls).label("total_balls"),
                func.sum(BattingPerformance.fours).label("total_fours"),
                func.sum(BattingPerformance.sixes).label("total_sixes"),
                func.count(BattingPerformance.performance_id).label("matches"),
            )
            .join(
                BattingPerformance,
                Player.player_id == BattingPerformance.player_id,
            )
            .group_by(
                Player.player_id,
                Player.name,
            )
            .all()
        )

        statistics = []

        for row in results:

            total_runs = row.total_runs or 0
            total_balls = row.total_balls or 0
            matches = row.matches or 0

            # Strike Rate
            if total_balls > 0:
                strike_rate = (total_runs / total_balls) * 100
            else:
                strike_rate = 0

            # Dismissals
            dismissals = (
                session.query(BattingPerformance)
                .filter(
                    BattingPerformance.player_id == row.player_id,
                    BattingPerformance.not_out == False,
                )
                .count()
            )

            # Batting Average
            if dismissals > 0:
                batting_average = total_runs / dismissals
            else:
                batting_average = total_runs

            # Runs per match
            if matches > 0:
                runs_per_match = total_runs / matches
            else:
                runs_per_match = 0

            # Boundary runs
            boundary_runs = (
                (row.total_fours or 0) * 4
                + (row.total_sixes or 0) * 6
            )

            # Boundary percentage
            if total_runs > 0:
                boundary_percentage = (
                    boundary_runs / total_runs
                ) * 100
            else:
                boundary_percentage = 0

            # 50s and 100s
            performances = (
                session.query(BattingPerformance.runs)
                .filter(
                    BattingPerformance.player_id == row.player_id
                )
                .all()
            )

            fifties = sum(
                1
                for performance in performances
                if 50 <= performance.runs < 100
            )

            hundreds = sum(
                1
                for performance in performances
                if performance.runs >= 100
            )

            statistics.append(
                {
                    "player_id": row.player_id,
                    "player_name": row.name,
                    "matches": matches,
                    "total_runs": total_runs,
                    "total_balls": total_balls,
                    "batting_average": round(batting_average, 2),
                    "strike_rate": round(strike_rate, 2),
                    "runs_per_match": round(runs_per_match, 2),
                    "fours": row.total_fours or 0,
                    "sixes": row.total_sixes or 0,
                    "boundary_percentage": round(
                        boundary_percentage,
                        2,
                    ),
                    "fifties": fifties,
                    "hundreds": hundreds,
                }
            )

        return statistics

    finally:
        session.close()

def get_batting_trend(player_id):
    """
    Get match-by-match batting performance for a player.

    Args:
        player_id (int): ID of the player.

    Returns:
        list[dict]: Match-level batting performance.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                BattingPerformance.match_id,
                BattingPerformance.runs,
                BattingPerformance.balls,
                BattingPerformance.fours,
                BattingPerformance.sixes,
            )
            .filter(
                BattingPerformance.player_id == player_id
            )
            .order_by(
                BattingPerformance.match_id
            )
            .all()
        )

        trend = []

        for row in results:

            runs = row.runs or 0
            balls = row.balls or 0

            if balls > 0:
                strike_rate = (runs / balls) * 100
            else:
                strike_rate = 0

            trend.append(
                {
                    "match_id": row.match_id,
                    "runs": runs,
                    "balls": balls,
                    "fours": row.fours or 0,
                    "sixes": row.sixes or 0,
                    "strike_rate": round(
                        strike_rate,
                        2,
                    ),
                }
            )

        return trend

    finally:
        session.close()
if __name__ == "__main__":

    statistics = get_batting_statistics()

    for player in statistics:
        print(player)