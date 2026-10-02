"""
Bowling analytics module.

Provides metrics, calculations, and performance evaluation
for bowling statistics.
"""

from sqlalchemy import func

from database.connection import SessionLocal
from database.models import Player, BowlingPerformance


def get_bowling_statistics():
    """
    Calculate bowling statistics for every player.

    Returns:
        list[dict]: Bowling statistics for each player.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Player.player_id,
                Player.name,
                func.sum(
                    BowlingPerformance.balls
                ).label("total_balls"),
                func.sum(
                    BowlingPerformance.runs_conceded
                ).label("runs_conceded"),
                func.sum(
                    BowlingPerformance.wickets
                ).label("wickets"),
                func.sum(
                    BowlingPerformance.maidens
                ).label("maidens"),
                func.sum(
                    BowlingPerformance.dot_balls
                ).label("dot_balls"),
                func.count(
                    BowlingPerformance.performance_id
                ).label("matches"),
            )
            .join(
                BowlingPerformance,
                Player.player_id
                == BowlingPerformance.player_id,
            )
            .group_by(
                Player.player_id,
                Player.name,
            )
            .all()
        )

        statistics = []

        for row in results:

            total_balls = (
                row.total_balls or 0
            )

            runs_conceded = (
                row.runs_conceded or 0
            )

            wickets = row.wickets or 0
            maidens = row.maidens or 0
            dot_balls = row.dot_balls or 0
            matches = row.matches or 0

            if total_balls > 0:

                economy_rate = (
                    runs_conceded
                    / total_balls
                ) * 6

            else:

                economy_rate = 0

            if wickets > 0:

                bowling_average = (
                    runs_conceded
                    / wickets
                )

                bowling_strike_rate = (
                    total_balls
                    / wickets
                )

            else:

                bowling_average = 0
                bowling_strike_rate = 0

            if total_balls > 0:

                dot_ball_percentage = (
                    dot_balls
                    / total_balls
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
    Get match-by-match bowling performance
    for a player.

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
                BowlingPerformance.player_id
                == player_id
            )
            .order_by(
                BowlingPerformance.match_id
            )
            .all()
        )

        trend = []

        for row in results:

            balls = row.balls or 0
            runs_conceded = (
                row.runs_conceded or 0
            )

            if balls > 0:

                economy_rate = (
                    runs_conceded
                    / balls
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


def get_bowling_consistency(player_id):
    """
    Calculate match-to-match bowling consistency.

    Consistency is based on variation in wickets
    and economy rate.

    A minimum of two matches is required to
    measure match-to-match consistency.

    Args:
        player_id (int): ID of the player.

    Returns:
        dict: Bowling consistency metrics.
    """

    trend = get_bowling_trend(player_id)

    # --------------------------------------------------
    # LOW-DATA CASE
    # --------------------------------------------------

    if len(trend) < 2:

        if not trend:
            average_wickets = 0
            average_economy_rate = 0

        else:
            average_wickets = (
                trend[0]["wickets"]
            )

            average_economy_rate = (
                trend[0]["economy_rate"]
            )

        return {
            "player_id": player_id,
            "matches": len(trend),
            "average_wickets": round(
                average_wickets,
                2,
            ),
            "wickets_std_dev": 0,
            "average_economy_rate": round(
                average_economy_rate,
                2,
            ),
            "economy_rate_std_dev": 0,
            "consistency_score": 0,
        }

    # --------------------------------------------------
    # EXTRACT METRICS
    # --------------------------------------------------

    wickets = [
        match["wickets"]
        for match in trend
    ]

    economy_rates = [
        match["economy_rate"]
        for match in trend
    ]

    # --------------------------------------------------
    # AVERAGES
    # --------------------------------------------------

    average_wickets = (
        sum(wickets)
        / len(wickets)
    )

    average_economy_rate = (
        sum(economy_rates)
        / len(economy_rates)
    )

    # --------------------------------------------------
    # STANDARD DEVIATION
    # --------------------------------------------------

    wickets_variance = (
        sum(
            (
                wicket
                - average_wickets
            ) ** 2
            for wicket in wickets
        )
        / len(wickets)
    )

    wickets_std_dev = (
        wickets_variance ** 0.5
    )

    economy_variance = (
        sum(
            (
                economy
                - average_economy_rate
            ) ** 2
            for economy in economy_rates
        )
        / len(economy_rates)
    )

    economy_rate_std_dev = (
        economy_variance ** 0.5
    )

    # --------------------------------------------------
    # COEFFICIENT OF VARIATION
    # --------------------------------------------------

    if average_wickets > 0:

        wickets_cv = (
            wickets_std_dev
            / average_wickets
        )

    else:

        wickets_cv = 1

    if average_economy_rate > 0:

        economy_rate_cv = (
            economy_rate_std_dev
            / average_economy_rate
        )

    else:

        economy_rate_cv = 1

    # --------------------------------------------------
    # CONSISTENCY SCORE
    # --------------------------------------------------

    variation_score = (
        wickets_cv
        + economy_rate_cv
    ) / 2

    consistency_score = (
        100
        * (1 - variation_score)
    )

    consistency_score = max(
        0,
        min(
            100,
            consistency_score,
        ),
    )

    return {
        "player_id": player_id,
        "matches": len(trend),
        "average_wickets": round(
            average_wickets,
            2,
        ),
        "wickets_std_dev": round(
            wickets_std_dev,
            2,
        ),
        "average_economy_rate": round(
            average_economy_rate,
            2,
        ),
        "economy_rate_std_dev": round(
            economy_rate_std_dev,
            2,
        ),
        "consistency_score": round(
            consistency_score,
            2,
        ),
    }


if __name__ == "__main__":

    statistics = get_bowling_statistics()

    for player in statistics:
        print(player)