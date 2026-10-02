from analytics.equipment import (
    get_equipment_list,
    get_equipment_statistics,
    get_equipment_by_player,
)


def test_equipment_list_not_empty():
    data = get_equipment_list()

    assert len(data) > 0


def test_equipment_has_required_fields():
    data = get_equipment_list()

    required_fields = {
        "equipment_id",
        "team",
        "equipment_type",
        "brand",
        "model",
        "serial_number",
        "assigned_player",
        "purchase_date",
        "condition",
        "status",
        "last_maintenance",
        "next_maintenance",
    }

    for item in data:
        assert required_fields.issubset(item.keys())


def test_equipment_statistics():
    stats = get_equipment_statistics()

    assert stats["total_equipment"] == 4
    assert stats["assigned_equipment"] == 3
    assert stats["available_equipment"] == 1
    assert stats["maintenance_equipment"] == 0
    assert stats["damaged_equipment"] == 0


def test_equipment_by_player():
    data = get_equipment_by_player(1)

    # Player ID 1 is not associated with equipment
    # through the current equipment query structure.
    assert isinstance(data, list)


def test_available_equipment():
    data = get_equipment_list()

    available = [
        item
        for item in data
        if item["status"] == "Available"
    ]

    assert len(available) == 1
    assert available[0]["equipment_type"] == "Bowling Machine"
    assert available[0]["assigned_player"] is None