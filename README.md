# 🏏 Cricket Sports Performance & Operations Intelligence Platform

A data-driven cricket analytics and operations platform designed to help teams monitor player performance, training workload, injuries, match performance, and equipment management through an interactive Streamlit dashboard.

The system combines **Python, SQL, SQLAlchemy, Pandas, NumPy, and Streamlit** to transform cricket performance and operational data into structured analytics and actionable insights.

---

## 📌 Project Overview

Managing a cricket team involves more than tracking runs and wickets.

Coaches and team managers need to monitor:

* Player performance
* Batting and bowling statistics
* Training attendance and workload
* Fitness levels
* Injuries and player availability
* Match-level performance
* Cricket equipment
* Overall player performance and confidence

This project brings these areas together into a single analytics platform.

The system uses a relational database as the central data layer and provides specialized Python analytics modules that feed an interactive Streamlit dashboard.

---

## 🎯 Objectives

The main objectives of the platform are to:

* Analyze batting and bowling performance
* Track player training participation and workload
* Monitor injuries and player availability
* Analyze match-level performance
* Track cricket equipment and assignments
* Calculate role-based player performance scores
* Measure confidence in performance data based on sample size
* Provide an interactive analytics dashboard
* Maintain automated tests for the analytics layer

---

## ✨ Key Features

### 👤 Player Analytics

Provides an integrated player profile containing:

* Player information
* Team
* Playing role
* Batting statistics
* Bowling statistics
* Training metrics
* Injury information
* Performance score
* Data confidence

### 🏏 Batting Analytics

The batting analytics module calculates:

* Matches played
* Total runs
* Total balls faced
* Batting average
* Strike rate
* Runs per match
* Fours
* Sixes
* Boundary percentage
* Fifties
* Hundreds

### 🎯 Bowling Analytics

The bowling module calculates:

* Matches played
* Total balls
* Runs conceded
* Wickets
* Maidens
* Dot balls
* Economy rate
* Bowling average
* Bowling strike rate
* Dot-ball percentage

### 🏋️ Training Analytics

Training performance is analyzed using:

* Total training sessions
* Sessions attended
* Sessions missed
* Attendance percentage
* Total workload
* Average workload
* Average fitness rating

This allows training participation and workload to be viewed alongside match performance.

### 🩹 Injury & Availability Analytics

The injury module provides:

* Total injuries
* Recovered injuries
* Recovering injuries
* Severe injuries
* Average recovery duration
* Player availability status

Players with active recovering injuries are identified as unavailable.

### 🏆 Match Analytics

Match-level analysis includes:

* Match list
* Match details
* Opponent
* Venue
* Competition
* Match type
* Result
* Team score
* Opponent score
* Match batting performances
* Match bowling performances

### 🧤 Equipment Management

The equipment module tracks:

* Equipment type
* Brand
* Model
* Serial number
* Team
* Assigned player
* Condition
* Status
* Purchase date
* Maintenance dates

Equipment statistics include:

* Total equipment
* Assigned equipment
* Available equipment
* Equipment under maintenance
* Damaged equipment

---

## 📊 Performance Scoring

The platform calculates a role-specific performance score using batting, bowling, and training metrics.

Different player roles use different weighting strategies.

### All-rounder

```text
Batting      → 35%
Bowling      → 35%
Training     → 30%
```

### Bowler

```text
Bowling      → 60%
Training     → 40%
```

### Batter / Wicketkeeper

```text
Batting      → 60%
Training     → 40%
```

The system also calculates **data confidence separately from performance score**.

This is important because a high performance score based on only a small number of matches should not be interpreted with the same confidence as a score supported by a larger sample.

---

## 🧠 Data Confidence

Data confidence is based on the amount of performance data available for a player.

For example, batting or bowling confidence increases as the number of recorded matches increases.

The system therefore separates:

```text
Performance Score
        +
Data Confidence
```

rather than combining them into a single metric.

This allows the dashboard to distinguish between:

* Strong performance with strong evidence
* Strong performance with limited evidence
* Lower performance with strong evidence
* Limited data requiring further observation

---

## 🏗️ System Architecture

```text
                    Streamlit Dashboard
                           │
                           ▼
                    Python Services
                           │
          ┌────────────────┼────────────────┐
          │                │                │
     Player Analytics   Match Analytics   Operations
          │                │                │
          ├── Batting      ├── Matches     ├── Training
          ├── Bowling      └── Performance ├── Injury
          └── Profile                       └── Equipment
                           │
                           ▼
                    SQLAlchemy ORM
                           │
                           ▼
                      SQLite DB
                           │
                           ▼
                  Cricket Data Models
```

---

## 🗄️ Database Design

The project uses a relational database with the following major entities:

```text
Teams
  │
  └── Players
        │
        ├── Batting Performances
        ├── Bowling Performances
        ├── Training Records
        ├── Injuries
        └── Equipment

Matches
  │
  ├── Batting Performances
  └── Bowling Performances

Training Sessions
  │
  └── Training Records
```

### Database Tables

The current database contains:

1. `teams`
2. `players`
3. `matches`
4. `batting_performances`
5. `bowling_performances`
6. `training_sessions`
7. `training_records`
8. `injuries`
9. `equipment`

SQLite is currently used for local development.

SQLAlchemy provides the ORM layer between Python and the database.

---

## 📁 Project Structure

```text
cricket-sports-analytics/
│
├── analytics/
│   ├── __init__.py
│   ├── batting.py
│   ├── bowling.py
│   ├── equipment.py
│   ├── injury.py
│   ├── matches.py
│   ├── performance.py
│   ├── player_profile.py
│   └── training.py
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── init_db.py
│   ├── models.py
│   └── seed.py
│
├── pages/
│   ├── equipment.py
│   ├── injury.py
│   ├── matches.py
│   ├── player.py
│   └── training.py
│
├── tests/
│   ├── __init__.py
│   ├── test_batting.py
│   ├── test_bowling.py
│   ├── test_equipment.py
│   ├── test_injury.py
│   ├── test_matches.py
│   ├── test_performance.py
│   └── test_training.py
│
├── data/
│   └── cricket_analytics.db
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

> The SQLite database is ignored by Git and is generated locally from the database setup and seed scripts.

---

## 🛠️ Technology Stack

### Programming

* Python 3.12

### Data & Analytics

* Pandas
* NumPy

### Database

* SQLite
* SQLAlchemy

### Dashboard

* Streamlit
* Plotly

### Testing

* Pytest

### Version Control

* Git
* GitHub

---

## 🧪 Testing

The analytics layer is covered by automated tests using `pytest`.

Current test coverage includes:

| Module      |  Tests |
| ----------- | -----: |
| Batting     |      4 |
| Bowling     |      4 |
| Equipment   |      5 |
| Injury      |      4 |
| Matches     |      5 |
| Performance |      4 |
| Training    |      4 |
| **Total**   | **30** |

Current result:

```text
30 passed
```

The tests validate:

* Data availability
* Required fields
* Valid numerical ranges
* Player-specific calculations
* Match-level calculations
* Equipment statistics
* Performance scoring
* Injury statistics
* Training metrics

Run the complete test suite with:

```bash
python -m pytest -v
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/banavii/cricket-sports-analytics.git
cd cricket-sports-analytics
```

### 2. Create and activate a virtual environment

For example:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🗃️ Initialize the Database

Create the database tables:

```bash
python -m database.init_db
```

Populate the database with development data:

```bash
python -m database.seed
```

---

## ▶️ Run the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📈 Dashboard

The main dashboard provides an executive-level overview of the cricket team.

It includes:

* Player performance comparison
* Performance vs data confidence
* Average training workload
* Player availability
* Match result distribution
* Player performance summary

Additional pages provide detailed views for:

* Players
* Matches
* Training
* Injuries
* Equipment

---

## 🔬 Current Development Data

The current development dataset contains:

```text
Teams:       2
Players:     8
Matches:     5
Batting:    10
Bowling:     6
Training:    5
Injuries:    2
Equipment:   4
```

The data is controlled seed data used for development, testing, and dashboard demonstration.

---

## 🔮 Future Enhancements

Potential future improvements include:

### Advanced Analytics

* Player performance trends over time
* Phase-wise batting and bowling analysis
* Venue-based performance
* Opponent-specific performance
* Player comparison tools
* Team-level performance trends

### Machine Learning

A future ML layer could use historical player and match data to investigate:

* Performance prediction
* Player workload and performance relationships
* Injury-risk indicators
* Match performance prediction
* Player form analysis

### Database

* PostgreSQL support
* Production database deployment
* Larger historical datasets

### Application

* Authentication and role-based access
* Coach and player accounts
* Exportable reports
* Advanced filtering
* Automated reporting
* Cloud deployment

---

## 📌 Project Status

**Current status: Active Development**

Completed:

* [x] Database architecture
* [x] SQLAlchemy models
* [x] Seed data
* [x] Batting analytics
* [x] Bowling analytics
* [x] Training analytics
* [x] Injury analytics
* [x] Match analytics
* [x] Equipment analytics
* [x] Player performance scoring
* [x] Player profile integration
* [x] Streamlit dashboard
* [x] Streamlit analytics pages
* [x] Automated testing
* [x] 30/30 tests passing
* [x] Git version control
* [x] GitHub repository

---

## 👩‍💻 Author

**Banavi**

GitHub:
[https://github.com/banavii](https://github.com/banavii)

---

## 📄 License

This project is currently intended as a portfolio and academic development project.
