from datetime import date

from database.connection import SessionLocal
from database.models import (
    Team,
    Player,
    Match,
    BattingPerformance,
    BowlingPerformance,
    TrainingSession,
    TrainingRecord,
    Injury,
    Equipment,
)


def seed_database():
    session = SessionLocal()

    try:
        # --------------------------------------------------
        # 1. TEAMS
        # --------------------------------------------------

        team1 = Team(
            team_name="Bangalore Strikers",
            team_type="Academy",
            season=2026,
            coach_name="Rahul Menon",
        )

        team2 = Team(
            team_name="Bangalore Challengers",
            team_type="Club",
            season=2026,
            coach_name="Priya Sharma",
        )

        session.add_all([team1, team2])
        session.flush()

        # --------------------------------------------------
        # 2. PLAYERS
        # --------------------------------------------------

        players = [
            Player(
                team_id=team1.team_id,
                name="Aarav Sharma",
                date_of_birth=date(2005, 4, 12),
                gender="Male",
                role="Batter",
                batting_style="Right-hand",
                bowling_style=None,
                joined_date=date(2025, 6, 1),
                status="Active",
            ),
            Player(
                team_id=team1.team_id,
                name="Rohan Kumar",
                date_of_birth=date(2004, 8, 21),
                gender="Male",
                role="All-rounder",
                batting_style="Right-hand",
                bowling_style="Right-arm medium",
                joined_date=date(2025, 5, 15),
                status="Active",
            ),
            Player(
                team_id=team1.team_id,
                name="Arjun Nair",
                date_of_birth=date(2006, 1, 10),
                gender="Male",
                role="Bowler",
                batting_style="Left-hand",
                bowling_style="Right-arm fast",
                joined_date=date(2025, 7, 10),
                status="Active",
            ),
            Player(
                team_id=team1.team_id,
                name="Kabir Singh",
                date_of_birth=date(2005, 11, 3),
                gender="Male",
                role="Wicketkeeper",
                batting_style="Right-hand",
                bowling_style=None,
                joined_date=date(2025, 4, 20),
                status="Active",
            ),
            Player(
                team_id=team2.team_id,
                name="Vihaan Rao",
                date_of_birth=date(2003, 7, 18),
                gender="Male",
                role="Batter",
                batting_style="Left-hand",
                bowling_style=None,
                joined_date=date(2024, 8, 1),
                status="Active",
            ),
            Player(
                team_id=team2.team_id,
                name="Aditya Menon",
                date_of_birth=date(2004, 2, 25),
                gender="Male",
                role="All-rounder",
                batting_style="Right-hand",
                bowling_style="Left-arm orthodox",
                joined_date=date(2024, 6, 10),
                status="Active",
            ),
            Player(
                team_id=team2.team_id,
                name="Karan Patel",
                date_of_birth=date(2005, 9, 14),
                gender="Male",
                role="Bowler",
                batting_style="Right-hand",
                bowling_style="Right-arm medium",
                joined_date=date(2025, 1, 5),
                status="Active",
            ),
            Player(
                team_id=team2.team_id,
                name="Dev Shah",
                date_of_birth=date(2006, 5, 30),
                gender="Male",
                role="Wicketkeeper",
                batting_style="Right-hand",
                bowling_style=None,
                joined_date=date(2025, 3, 12),
                status="Active",
            ),
        ]

        session.add_all(players)
        session.flush()

        # --------------------------------------------------
        # 3. MATCHES
        # --------------------------------------------------

        matches = [
            Match(
                team_id=team1.team_id,
                match_date=date(2026, 8, 1),
                opponent="Mysore Warriors",
                venue="M. Chinnaswamy Stadium",
                competition="Karnataka T20 League",
                match_type="T20",
                result="Won",
                team_score=178,
                opponent_score=164,
            ),
            Match(
                team_id=team1.team_id,
                match_date=date(2026, 8, 8),
                opponent="Hubli Tigers",
                venue="KSCA Stadium",
                competition="Karnataka T20 League",
                match_type="T20",
                result="Lost",
                team_score=151,
                opponent_score=169,
            ),
            Match(
                team_id=team1.team_id,
                match_date=date(2026, 8, 15),
                opponent="Mangalore Dragons",
                venue="M. Chinnaswamy Stadium",
                competition="Karnataka T20 League",
                match_type="T20",
                result="Won",
                team_score=191,
                opponent_score=177,
            ),
            Match(
                team_id=team2.team_id,
                match_date=date(2026, 8, 2),
                opponent="Mysore Warriors",
                venue="KSCA Stadium",
                competition="Karnataka T20 League",
                match_type="T20",
                result="Won",
                team_score=165,
                opponent_score=158,
            ),
            Match(
                team_id=team2.team_id,
                match_date=date(2026, 8, 16),
                opponent="Hubli Tigers",
                venue="M. Chinnaswamy Stadium",
                competition="Karnataka T20 League",
                match_type="T20",
                result="Lost",
                team_score=149,
                opponent_score=172,
            ),
        ]

        session.add_all(matches)
        session.flush()

        # --------------------------------------------------
        # 4. BATTING PERFORMANCES
        # --------------------------------------------------

        batting = [
            # Match 1
            BattingPerformance(
                match_id=matches[0].match_id,
                player_id=players[0].player_id,
                runs=72,
                balls=48,
                fours=7,
                sixes=3,
                dismissal_type="Caught",
                not_out=False,
            ),
            BattingPerformance(
                match_id=matches[0].match_id,
                player_id=players[1].player_id,
                runs=41,
                balls=29,
                fours=4,
                sixes=2,
                dismissal_type="Bowled",
                not_out=False,
            ),
            BattingPerformance(
                match_id=matches[0].match_id,
                player_id=players[3].player_id,
                runs=28,
                balls=19,
                fours=3,
                sixes=1,
                dismissal_type=None,
                not_out=True,
            ),

            # Match 2
            BattingPerformance(
                match_id=matches[1].match_id,
                player_id=players[0].player_id,
                runs=31,
                balls=27,
                fours=3,
                sixes=1,
                dismissal_type="LBW",
                not_out=False,
            ),
            BattingPerformance(
                match_id=matches[1].match_id,
                player_id=players[1].player_id,
                runs=54,
                balls=38,
                fours=5,
                sixes=2,
                dismissal_type="Caught",
                not_out=False,
            ),

            # Match 3
            BattingPerformance(
                match_id=matches[2].match_id,
                player_id=players[0].player_id,
                runs=84,
                balls=51,
                fours=9,
                sixes=4,
                dismissal_type=None,
                not_out=True,
            ),
            BattingPerformance(
                match_id=matches[2].match_id,
                player_id=players[1].player_id,
                runs=33,
                balls=22,
                fours=2,
                sixes=2,
                dismissal_type="Caught",
                not_out=False,
            ),

            # Team 2 - Match 4
            BattingPerformance(
                match_id=matches[3].match_id,
                player_id=players[4].player_id,
                runs=67,
                balls=45,
                fours=6,
                sixes=3,
                dismissal_type="Caught",
                not_out=False,
            ),
            BattingPerformance(
                match_id=matches[3].match_id,
                player_id=players[5].player_id,
                runs=38,
                balls=27,
                fours=4,
                sixes=1,
                dismissal_type=None,
                not_out=True,
            ),

            # Team 2 - Match 5
            BattingPerformance(
                match_id=matches[4].match_id,
                player_id=players[4].player_id,
                runs=29,
                balls=25,
                fours=3,
                sixes=1,
                dismissal_type="Bowled",
                not_out=False,
            ),
        ]

        session.add_all(batting)

        # --------------------------------------------------
        # 5. BOWLING PERFORMANCES
        # --------------------------------------------------

        bowling = [
            BowlingPerformance(
                match_id=matches[0].match_id,
                player_id=players[2].player_id,
                balls=24,
                runs_conceded=28,
                wickets=3,
                maidens=0,
                dot_balls=10,
            ),
            BowlingPerformance(
                match_id=matches[0].match_id,
                player_id=players[1].player_id,
                balls=18,
                runs_conceded=24,
                wickets=1,
                maidens=0,
                dot_balls=6,
            ),
            BowlingPerformance(
                match_id=matches[1].match_id,
                player_id=players[2].player_id,
                balls=24,
                runs_conceded=36,
                wickets=1,
                maidens=0,
                dot_balls=7,
            ),
            BowlingPerformance(
                match_id=matches[2].match_id,
                player_id=players[2].player_id,
                balls=24,
                runs_conceded=25,
                wickets=4,
                maidens=1,
                dot_balls=12,
            ),
            BowlingPerformance(
                match_id=matches[3].match_id,
                player_id=players[6].player_id,
                balls=24,
                runs_conceded=31,
                wickets=2,
                maidens=0,
                dot_balls=9,
            ),
            BowlingPerformance(
                match_id=matches[4].match_id,
                player_id=players[6].player_id,
                balls=24,
                runs_conceded=42,
                wickets=1,
                maidens=0,
                dot_balls=6,
            ),
        ]

        session.add_all(bowling)

        # --------------------------------------------------
        # 6. TRAINING SESSIONS
        # --------------------------------------------------

        sessions = [
            TrainingSession(
                team_id=team1.team_id,
                session_date=date(2026, 7, 28),
                session_type="Batting",
                duration_minutes=90,
                intensity=3,
                coach_name="Rahul Menon",
                notes="Top-order batting session",
            ),
            TrainingSession(
                team_id=team1.team_id,
                session_date=date(2026, 7, 30),
                session_type="Bowling",
                duration_minutes=75,
                intensity=4,
                coach_name="Rahul Menon",
                notes="Fast bowling workload",
            ),
            TrainingSession(
                team_id=team1.team_id,
                session_date=date(2026, 8, 4),
                session_type="Fitness",
                duration_minutes=60,
                intensity=4,
                coach_name="Rahul Menon",
                notes="Strength and conditioning",
            ),
            TrainingSession(
                team_id=team2.team_id,
                session_date=date(2026, 7, 29),
                session_type="Fielding",
                duration_minutes=75,
                intensity=3,
                coach_name="Priya Sharma",
                notes="Fielding drills",
            ),
            TrainingSession(
                team_id=team2.team_id,
                session_date=date(2026, 8, 5),
                session_type="Match Simulation",
                duration_minutes=120,
                intensity=5,
                coach_name="Priya Sharma",
                notes="T20 match simulation",
            ),
        ]

        session.add_all(sessions)
        session.flush()

        # --------------------------------------------------
        # 7. TRAINING RECORDS
        # --------------------------------------------------

        training_records = []

        for training_session in sessions:

            if training_session.team_id == team1.team_id:
                team_players = players[:4]
            else:
                team_players = players[4:]

            for player in team_players:

                attendance = True

                workload = (
                    training_session.duration_minutes
                    * training_session.intensity
                )

                training_records.append(
                    TrainingRecord(
                        session_id=training_session.session_id,
                        player_id=player.player_id,
                        attendance=attendance,
                        workload=workload,
                        fitness_rating=4,
                    )
                )

        session.add_all(training_records)

        # --------------------------------------------------
        # 8. INJURIES
        # --------------------------------------------------

        injuries = [
            Injury(
                player_id=players[2].player_id,
                injury_type="Hamstring strain",
                body_part="Left hamstring",
                injury_date=date(2026, 7, 20),
                severity="Moderate",
                recovery_status="Recovered",
                expected_return=date(2026, 7, 30),
                actual_return=date(2026, 7, 29),
                notes="Completed rehabilitation successfully",
            ),
            Injury(
                player_id=players[5].player_id,
                injury_type="Ankle sprain",
                body_part="Right ankle",
                injury_date=date(2026, 8, 10),
                severity="Mild",
                recovery_status="Recovering",
                expected_return=date(2026, 8, 20),
                actual_return=None,
                notes="Light training only",
            ),
        ]

        session.add_all(injuries)

        # --------------------------------------------------
        # 9. EQUIPMENT
        # --------------------------------------------------

        equipment = [
            Equipment(
                team_id=team1.team_id,
                equipment_type="Cricket Bat",
                brand="SS",
                model="TON",
                serial_number="BAT-BS-001",
                assigned_player_id=players[0].player_id,
                purchase_date=date(2026, 1, 10),
                condition="Good",
                status="Assigned",
                last_maintenance=date(2026, 7, 1),
                next_maintenance=date(2026, 10, 1),
            ),
            Equipment(
                team_id=team1.team_id,
                equipment_type="Helmet",
                brand="Masuri",
                model="StemGuard",
                serial_number="HEL-BS-002",
                assigned_player_id=players[1].player_id,
                purchase_date=date(2026, 2, 15),
                condition="Good",
                status="Assigned",
                last_maintenance=date(2026, 7, 15),
                next_maintenance=date(2026, 11, 15),
            ),
            Equipment(
                team_id=team1.team_id,
                equipment_type="Bowling Machine",
                brand="BOLA",
                model="Professional",
                serial_number="BM-BS-003",
                assigned_player_id=None,
                purchase_date=date(2025, 9, 10),
                condition="Excellent",
                status="Available",
                last_maintenance=date(2026, 6, 1),
                next_maintenance=date(2026, 12, 1),
            ),
            Equipment(
                team_id=team2.team_id,
                equipment_type="Cricket Bat",
                brand="SG",
                model="Players Edition",
                serial_number="BAT-BC-001",
                assigned_player_id=players[4].player_id,
                purchase_date=date(2026, 1, 20),
                condition="Good",
                status="Assigned",
                last_maintenance=date(2026, 7, 5),
                next_maintenance=date(2026, 10, 5),
            ),
        ]

        session.add_all(equipment)

        # --------------------------------------------------
        # SAVE EVERYTHING
        # --------------------------------------------------

        session.commit()

        print("Seed data inserted successfully.")

    except Exception as error:
        session.rollback()
        print(f"Error while inserting seed data: {error}")
        raise

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()