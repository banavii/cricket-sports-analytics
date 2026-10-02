from sqlalchemy import func

from database.connection import SessionLocal
from database.models import (
    Match,
    Team,
    Player,
    BattingPerformance,
    BowlingPerformance,
)


def get_match_list():
    """
    Return all matches with basic match information.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Match.match_id,
                Match.match_date,
                Team.team_name,
                Match.opponent,
                Match.venue,
                Match.competition,
                Match.match_type,
                Match.result,
                Match.team_score,
                Match.opponent_score,
            )
            .join(
                Team,
                Match.team_id == Team.team_id,
            )
            .order_by(
                Match.match_date.desc()
            )
            .all()
        )

        matches = []

        for row in results:

            matches.append(
                {
                    "match_id": row.match_id,
                    "match_date": row.match_date,
                    "team": row.team_name,
                    "opponent": row.opponent,
                    "venue": row.venue,
                    "competition": row.competition,
                    "match_type": row.match_type,
                    "result": row.result,
                    "team_score": row.team_score,
                    "opponent_score": row.opponent_score,
                }
            )

        return matches

    finally:
        session.close()


def get_match_details(match_id):
    """
    Return complete details for one match.
    """

    session = SessionLocal()

    try:

        match = (
            session.query(Match)
            .filter(
                Match.match_id == match_id
            )
            .first()
        )

        if not match:
            return None

        team = (
            session.query(Team)
            .filter(
                Team.team_id == match.team_id
            )
            .first()
        )

        return {
            "match_id": match.match_id,
            "match_date": match.match_date,
            "team": team.team_name if team else None,
            "opponent": match.opponent,
            "venue": match.venue,
            "competition": match.competition,
            "match_type": match.match_type,
            "result": match.result,
            "team_score": match.team_score,
            "opponent_score": match.opponent_score,
        }

    finally:
        session.close()


def get_batting_performances(match_id):
    """
    Return all batting performances for a match.
    """

    session = SessionLocal()

    try:

        results = (
            session.query(
                Player.name,
                Player.role,
                BattingPerformance.runs,
                BattingPerformance.balls,
                BattingPerformance.fours,
                BattingPerformance.sixes,
                BattingPerformance.dismissal_type,
                BattingPerformance.not_out,
            )
            .join(
                Player,
                BattingPerformance.player_id
                == Player.player_id,
            )
            .filter(
                BattingPerformance.match_id == match_id
            )
            .order_by(
                BattingPerformance.runs.desc()
            )
            .all()
        )

        performances = []

        for row in results:

            if row.balls > 0:
                strike_rate = (
                    row.runs / row.balls
                ) * 100
            else:
                strike_rate = 0

            performances.append(
                {
                    "player_name": row.name,
                    "role": row.role,
                    "runs": row.runs,
                    "balls": row.balls,
                    "fours": row.fours,
                    "sixes": row.sixes,
                    "strike_rate": round(
                        strike_rate,
                        2,
                    ),
                    "dismissal_type": (
                        row.dismissal_type
                        if row.dismissal_type
                        else "Not Out"
                    ),
                    "not_out": row.not_out,
                }
            )

        return performances

    finally:
        session.close()


def get_bowling_performances(match_id):
    """
    Return all bowling performances for a match.
    """

    session = SessionLocal()

    try:

        results = (
            session.query(
                Player.name,
                Player.role,
                BowlingPerformance.balls,
                BowlingPerformance.runs_conceded,
                BowlingPerformance.wickets,
                BowlingPerformance.maidens,
                BowlingPerformance.dot_balls,
            )
            .join(
                Player,
                BowlingPerformance.player_id
                == Player.player_id,
            )
            .filter(
                BowlingPerformance.match_id == match_id
            )
            .order_by(
                BowlingPerformance.wickets.desc()
            )
            .all()
        )

        performances = []

        for row in results:

            if row.balls > 0:
                economy = (
                    row.runs_conceded
                    / row.balls
                ) * 6
            else:
                economy = 0

            performances.append(
                {
                    "player_name": row.name,
                    "role": row.role,
                    "balls": row.balls,
                    "runs_conceded": row.runs_conceded,
                    "wickets": row.wickets,
                    "maidens": row.maidens,
                    "dot_balls": row.dot_balls,
                    "economy_rate": round(
                        economy,
                        2,
                    ),
                }
            )

        return performances

    finally:
        session.close()


def get_match_summary(match_id):
    """
    Return a complete summary for one match.
    """

    match = get_match_details(match_id)

    if not match:
        return None

    batting = get_batting_performances(
        match_id
    )

    bowling = get_bowling_performances(
        match_id
    )

    return {
        "match": match,
        "batting": batting,
        "bowling": bowling,
    }


if __name__ == "__main__":

    matches = get_match_list()

    print()
    print("MATCH ANALYTICS")
    print("=" * 100)

    for match in matches:

        print(
            f"{match['match_id']:>2} | "
            f"{match['match_date']} | "
            f"{match['team']} vs "
            f"{match['opponent']:<20} | "
            f"{match['result']:<10} | "
            f"{match['team_score']} - "
            f"{match['opponent_score']}"
        )

    print("=" * 100)

    if matches:

        match_id = matches[0]["match_id"]

        summary = get_match_summary(
            match_id
        )

        print()
        print(
            f"MATCH DETAILS - ID {match_id}"
        )
        print("-" * 100)

        match = summary["match"]

        print(
            f"Date:         {match['match_date']}"
        )
        print(
            f"Team:         {match['team']}"
        )
        print(
            f"Opponent:     {match['opponent']}"
        )
        print(
            f"Venue:        {match['venue']}"
        )
        print(
            f"Competition:  {match['competition']}"
        )
        print(
            f"Match Type:   {match['match_type']}"
        )
        print(
            f"Result:       {match['result']}"
        )
        print(
            f"Score:        {match['team_score']} - "
            f"{match['opponent_score']}"
        )

        print()
        print("BATTING PERFORMANCES")
        print("-" * 100)

        for player in summary["batting"]:

            print(
                f"{player['player_name']:<20}"
                f" Runs: {player['runs']:>3}"
                f" Balls: {player['balls']:>3}"
                f" SR: {player['strike_rate']:>6.2f}"
                f" 4s: {player['fours']:>2}"
                f" 6s: {player['sixes']:>2}"
            )

        print()
        print("BOWLING PERFORMANCES")
        print("-" * 100)

        for player in summary["bowling"]:

            print(
                f"{player['player_name']:<20}"
                f" Wickets: {player['wickets']:>2}"
                f" Runs: {player['runs_conceded']:>3}"
                f" Economy: {player['economy_rate']:>5.2f}"
                f" Dot Balls: {player['dot_balls']:>3}"
            )

        print("=" * 100)