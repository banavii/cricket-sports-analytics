from analytics.training import get_training_statistics


def test_training_statistics_not_empty():

    data = get_training_statistics()

    assert len(data) > 0


def test_training_statistics_have_required_fields():

    data = get_training_statistics()

    required_fields = {
        "player_id",
        "player_name",
        "total_sessions",
        "sessions_attended",
        "sessions_missed",
        "attendance_percentage",
        "total_workload",
        "average_workload",
        "average_fitness",
    }

    for player in data:
        assert required_fields.issubset(
            player.keys()
        )


def test_training_values_are_non_negative():

    data = get_training_statistics()

    for player in data:

        assert player["total_sessions"] >= 0
        assert player["sessions_attended"] >= 0
        assert player["sessions_missed"] >= 0
        assert player["attendance_percentage"] >= 0
        assert player["total_workload"] >= 0
        assert player["average_workload"] >= 0
        assert player["average_fitness"] >= 0


def test_aarav_sharma_training():
    data = get_training_statistics()

    aarav = next(
        player
        for player in data
        if player["player_name"] == "Aarav Sharma"
    )

    assert aarav["total_sessions"] == 3
    assert aarav["sessions_attended"] == 3
    assert aarav["sessions_missed"] == 0
    assert aarav["attendance_percentage"] == 100.0
