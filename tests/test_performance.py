from analytics.performance import calculate_performance_scores


def test_performance_not_empty():
    data = calculate_performance_scores()
    assert len(data) > 0


def test_performance_has_required_fields():
    data = calculate_performance_scores()

    required_fields = {
        "player_id",
        "player_name",
        "role",
        "performance_score",
        "batting_score",
        "bowling_score",
        "training_score",
        "data_confidence",
        "confidence_label",
        "batting_matches",
        "bowling_matches",
        "training_sessions",
    }

    for player in data:
        assert required_fields.issubset(player.keys())


def test_performance_scores_are_valid():
    data = calculate_performance_scores()

    for player in data:
        assert 0 <= player["performance_score"] <= 100
        assert 0 <= player["batting_score"] <= 100
        assert 0 <= player["bowling_score"] <= 100
        assert 0 <= player["training_score"] <= 100
        assert 0 <= player["data_confidence"] <= 100


def test_aarav_sharma_performance():
    data = calculate_performance_scores()

    aarav = next(
        player
        for player in data
        if player["player_name"] == "Aarav Sharma"
    )

    assert aarav["role"] == "Batter"
    assert aarav["performance_score"] == 87.38
    assert aarav["data_confidence"] == 100
    assert aarav["confidence_label"] == "High"
def test_performance_includes_consistency_metrics():
    from analytics.performance import calculate_performance_scores

    results = calculate_performance_scores()

    assert len(results) > 0

    for player in results:
        assert "batting_consistency" in player
        assert "bowling_consistency" in player

        assert 0 <= player["batting_consistency"] <= 100
        assert 0 <= player["bowling_consistency"] <= 100    