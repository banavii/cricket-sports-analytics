from analytics.injury import get_injury_statistics


def test_injury_statistics_not_empty():
    data = get_injury_statistics()
    assert len(data) > 0


def test_injury_statistics_have_required_fields():
    data = get_injury_statistics()

    required_fields = {
        "player_id",
        "player_name",
        "total_injuries",
        "recovered_injuries",
        "recovering_injuries",
        "severe_injuries",
        "average_recovery_days",
        "availability_status",
    }

    for player in data:
        assert required_fields.issubset(player.keys())


def test_injury_values_are_non_negative():
    data = get_injury_statistics()

    for player in data:
        assert player["total_injuries"] >= 0
        assert player["recovered_injuries"] >= 0
        assert player["recovering_injuries"] >= 0
        assert player["severe_injuries"] >= 0
        assert player["average_recovery_days"] >= 0


def test_arjun_nair_injury():
    data = get_injury_statistics()

    arjun = next(
        player
        for player in data
        if player["player_name"] == "Arjun Nair"
    )

    assert arjun["total_injuries"] == 1
    assert arjun["recovered_injuries"] == 1
    assert arjun["recovering_injuries"] == 0
    assert arjun["availability_status"] == "Available"
