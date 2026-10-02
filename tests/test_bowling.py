from analytics.bowling import (
    get_bowling_statistics,
    get_bowling_trend
)

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
def test_bowling_trend():
    trend = get_bowling_trend(3)

    assert len(trend) == 3

    assert trend[0]["match_id"] == 1
    assert trend[0]["wickets"] == 3
    assert trend[0]["economy_rate"] == 7.0

    assert trend[2]["match_id"] == 3
    assert trend[2]["wickets"] == 4
    assert trend[2]["economy_rate"] == 6.25    

def test_bowling_consistency():
    from analytics.bowling import get_bowling_consistency

    # Arjun has 3 bowling matches
    result = get_bowling_consistency(3)

    assert result["player_id"] == 3
    assert result["matches"] == 3
    assert result["average_wickets"] == 2.67
    assert result["average_economy_rate"] == 7.42
    assert result["consistency_score"] == 68.79

    # Rohan has only 1 bowling match,
    # so match-to-match consistency cannot be measured.
    rohan = get_bowling_consistency(2)

    assert rohan["matches"] == 1
    assert rohan["consistency_score"] == 0

    # Karan has 2 bowling matches,
    # so consistency should be calculated.
    karan = get_bowling_consistency(7)

    assert karan["matches"] == 2
    assert 0 <= karan["consistency_score"] <= 100
