from analytics.matches import (
    get_match_list,
    get_match_details,
    get_batting_performances,
    get_bowling_performances,
    get_match_summary,
)


def test_match_list_not_empty():
    data = get_match_list()

    assert len(data) > 0


def test_match_details():
    data = get_match_details(5)

    assert data is not None
    assert data["match_id"] == 5
    assert data["team"] == "Bangalore Challengers"
    assert data["opponent"] == "Hubli Tigers"
    assert data["result"] == "Lost"
    assert data["team_score"] == 149
    assert data["opponent_score"] == 172


def test_match_batting_performances():
    data = get_batting_performances(5)

    assert len(data) > 0

    vihaan = next(
        player
        for player in data
        if player["player_name"] == "Vihaan Rao"
    )

    assert vihaan["runs"] == 29
    assert vihaan["balls"] == 25


def test_match_bowling_performances():
    data = get_bowling_performances(5)

    assert len(data) > 0

    karan = next(
        player
        for player in data
        if player["player_name"] == "Karan Patel"
    )

    assert karan["wickets"] == 1
    assert karan["runs_conceded"] == 42


def test_match_summary():
    data = get_match_summary(5)

    assert data is not None

    assert data["match"]["match_id"] == 5
    assert data["match"]["team"] == "Bangalore Challengers"
    assert data["match"]["opponent"] == "Hubli Tigers"

    assert len(data["batting"]) > 0
    assert len(data["bowling"]) > 0