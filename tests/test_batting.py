from analytics.batting import get_batting_statistics


def test_batting_statistics_not_empty():

    data = get_batting_statistics()

    assert len(data) > 0


def test_batting_statistics_have_required_fields():

    data = get_batting_statistics()

    required_fields = {
        "player_id",
        "player_name",
        "matches",
        "total_runs",
        "batting_average",
        "strike_rate",
    }

    for player in data:
        assert required_fields.issubset(
            player.keys()
        )


def test_batting_values_are_non_negative():

    data = get_batting_statistics()

    for player in data:

        assert player["matches"] >= 0
        assert player["total_runs"] >= 0
        assert player["batting_average"] >= 0
        assert player["strike_rate"] >= 0


def test_aarav_sharma_batting():

    data = get_batting_statistics()

    aarav = next(
        player
        for player in data
        if player["player_name"] == "Aarav Sharma"
    )

    assert aarav["matches"] == 3
    assert aarav["total_runs"] == 187
    assert aarav["batting_average"] == 93.50
