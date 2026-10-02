from analytics.bowling import get_bowling_statistics


def test_bowling_statistics_not_empty():

    data = get_bowling_statistics()

    assert len(data) > 0


def test_bowling_statistics_have_required_fields():

    data = get_bowling_statistics()

    required_fields = {
        "player_id",
        "player_name",
        "matches",
        "total_balls",
        "runs_conceded",
        "wickets",
        "economy_rate",
        "bowling_average",
        "bowling_strike_rate",
    }

    for player in data:
        assert required_fields.issubset(
            player.keys()
        )


def test_bowling_values_are_non_negative():

    data = get_bowling_statistics()

    for player in data:

        assert player["matches"] >= 0
        assert player["total_balls"] >= 0
        assert player["runs_conceded"] >= 0
        assert player["wickets"] >= 0
        assert player["economy_rate"] >= 0


def test_karan_patel_bowling():

    data = get_bowling_statistics()

    karan = next(
        player
        for player in data
        if player["player_name"] == "Karan Patel"
    )

    assert karan["matches"] == 2
    assert karan["wickets"] == 3
