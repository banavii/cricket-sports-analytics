from sqlalchemy import Integer, func

from database.connection import SessionLocal
from database.models import (
    Player,
    TrainingRecord,
)


def get_training_statistics():
    """
    Calculate training and fitness statistics for every player.

    Returns:
        list[dict]: Training statistics for each player.
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Player.player_id,
                Player.name,
                func.count(TrainingRecord.record_id).label(
                    "total_sessions"
                ),
                func.sum(
                    TrainingRecord.attendance.cast(Integer)
                ).label("sessions_attended"),
                func.sum(
                    TrainingRecord.workload
                ).label("total_workload"),
                func.avg(
                    TrainingRecord.workload
                ).label("average_workload"),
                func.avg(
                    TrainingRecord.fitness_rating
                ).label("average_fitness"),
            )
            .join(
                TrainingRecord,
                Player.player_id == TrainingRecord.player_id,
            )
            .group_by(
                Player.player_id,
                Player.name,
            )
            .all()
        )

        statistics = []

        for row in results:

            total_sessions = row.total_sessions or 0
            sessions_attended = row.sessions_attended or 0
            total_workload = row.total_workload or 0
            average_workload = row.average_workload or 0
            average_fitness = row.average_fitness or 0

            # Attendance percentage
            if total_sessions > 0:
                attendance_percentage = (
                    sessions_attended / total_sessions
                ) * 100
            else:
                attendance_percentage = 0

            # Sessions missed
            sessions_missed = (
                total_sessions - sessions_attended
            )

            statistics.append(
                {
                    "player_id": row.player_id,
                    "player_name": row.name,
                    "total_sessions": total_sessions,
                    "sessions_attended": sessions_attended,
                    "sessions_missed": sessions_missed,
                    "attendance_percentage": round(
                        attendance_percentage,
                        2,
                    ),
                    "total_workload": round(
                        total_workload,
                        2,
                    ),
                    "average_workload": round(
                        average_workload,
                        2,
                    ),
                    "average_fitness": round(
                        average_fitness,
                        2,
                    ),
                }
            )

        return statistics

    finally:
        session.close()


if __name__ == "__main__":

    statistics = get_training_statistics()

    for player in statistics:
        print(player)