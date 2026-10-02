from datetime import date

from sqlalchemy import func

from database.connection import SessionLocal
from database.models import Equipment, Player, Team


def get_equipment_list():
    """
    Return all equipment with team and player information.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Equipment.equipment_id,
                Team.team_name,
                Equipment.equipment_type,
                Equipment.brand,
                Equipment.model,
                Equipment.serial_number,
                Player.name.label("player_name"),
                Equipment.purchase_date,
                Equipment.condition,
                Equipment.status,
                Equipment.last_maintenance,
                Equipment.next_maintenance,
            )
            .join(
                Team,
                Equipment.team_id == Team.team_id,
            )
            .outerjoin(
                Player,
                Equipment.assigned_player_id
                == Player.player_id,
            )
            .order_by(
                Equipment.equipment_id
            )
            .all()
        )

        equipment = []

        for row in results:

            equipment.append(
                {
                    "equipment_id": row.equipment_id,
                    "team": row.team_name,
                    "equipment_type": row.equipment_type,
                    "brand": row.brand,
                    "model": row.model,
                    "serial_number": row.serial_number,
                    "assigned_player": row.player_name,
                    "purchase_date": row.purchase_date,
                    "condition": row.condition,
                    "status": row.status,
                    "last_maintenance": row.last_maintenance,
                    "next_maintenance": row.next_maintenance,
                }
            )

        return equipment

    finally:
        session.close()


def get_equipment_statistics():
    """
    Calculate high-level equipment statistics.
    """

    equipment = get_equipment_list()

    total_equipment = len(equipment)

    assigned_equipment = sum(
        1
        for item in equipment
        if item["assigned_player"] is not None
    )

    available_equipment = sum(
        1
        for item in equipment
        if item["status"] == "Available"
    )

    maintenance_equipment = sum(
        1
        for item in equipment
        if item["status"] == "Maintenance"
    )

    damaged_equipment = sum(
        1
        for item in equipment
        if item["condition"] in [
            "Damaged",
            "Poor",
        ]
    )

    return {
        "total_equipment": total_equipment,
        "assigned_equipment": assigned_equipment,
        "available_equipment": available_equipment,
        "maintenance_equipment": maintenance_equipment,
        "damaged_equipment": damaged_equipment,
    }


def get_equipment_by_player(player_id):
    """
    Return equipment assigned to a specific player.
    """

    equipment = get_equipment_list()

    return [
        item
        for item in equipment
        if item["assigned_player"] is not None
        and item["assigned_player"] == player_id
    ]


if __name__ == "__main__":

    equipment = get_equipment_list()

    statistics = get_equipment_statistics()

    print()
    print("EQUIPMENT MANAGEMENT")
    print("=" * 100)

    print(
        f"Total Equipment:       "
        f"{statistics['total_equipment']}"
    )

    print(
        f"Assigned Equipment:    "
        f"{statistics['assigned_equipment']}"
    )

    print(
        f"Available Equipment:   "
        f"{statistics['available_equipment']}"
    )

    print(
        f"Maintenance:           "
        f"{statistics['maintenance_equipment']}"
    )

    print(
        f"Damaged/Poor:          "
        f"{statistics['damaged_equipment']}"
    )

    print()
    print("EQUIPMENT INVENTORY")
    print("-" * 100)

    for item in equipment:

        assigned_to = (
            item["assigned_player"]
            if item["assigned_player"]
            else "Unassigned"
        )

        print(
            f"{item['equipment_id']:>2} | "
            f"{item['equipment_type']:<15} | "
            f"{item['brand'] or 'N/A':<12} | "
            f"{item['condition']:<10} | "
            f"{item['status']:<12} | "
            f"{assigned_to}"
        )

    print("=" * 100)