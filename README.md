# 🏏 Cricket Sports Performance & Operations Intelligence Platform

A data-driven cricket analytics and operations platform designed to help teams monitor player performance, training workload, injuries, match performance, and equipment management through an interactive Streamlit dashboard.

The system combines **Python, SQL, SQLAlchemy, Pandas, NumPy, Plotly, and Streamlit** to transform cricket performance and operational data into structured analytics and actionable insights.

**Project Status:** Version 1 Completed ✅ | Version 2 In Progress 🚀

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
* Overall player performance
* Data confidence and consistency

This project brings these areas together into a single analytics platform.

The system uses a relational database as the central data layer and provides specialized Python analytics modules that feed an interactive Streamlit dashboard.

Version 1 establishes the core database, analytics engine, player management, operational modules, dashboard, and automated testing framework.

Version 2 continues development by expanding the platform toward more advanced cricket intelligence and data-driven performance analysis.

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
* Analyze match-to-match performance consistency
* Provide player-specific performance insights
* Provide an interactive analytics dashboard
* Maintain automated tests for the analytics layer
* Build a foundation for future advanced analytics and machine learning

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
* Availability status
* Performance score
* Data confidence
* Batting consistency
* Bowling consistency
* Match-by-match performance trends

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

The platform also provides match-by-match batting trends and batting consistency analysis.

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

The platform also provides match-by-match bowling trends and bowling consistency analysis.

### 🏋️ Training Analytics

Training performance is analyzed using:

* Total training sessions
* Sessions attended
* Sessions missed
* Attendance percentage
* Total workload
* Average workload
* Average fitness rating
* Workload status

Training workload is classified relative to the overall squad workload to identify players with comparatively high, moderate, or low workload levels.

This allows training participation and workload to be viewed alongside player performance.

### 🩹 Injury & Availability Analytics

The injury module provides:

* Total injuries
* Recovered injuries
* Recovering injuries
* Severe injuries
* Average recovery duration
* Player availability status

Players with active recovering injuries are identified as unavailable.

The dashboard also provides an overview of current player availability across the squad.

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
* Match summaries

This provides a structured view of team and player performance at match level.

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

Batting → 35%
Bowling → 35%
Training → 30%

### Bowler

Bowling → 60%
Training → 40%

### Batter / Wicketkeeper

Batting → 60%
Training → 40%

The system also calculates **data confidence separately from performance score**.

This is important because a high performance score based on only a small number of matches should not be interpreted with the same confidence as a score supported by a larger sample.

---

## 🧠 Data Confidence

Data confidence represents the amount of performance data available to support a player's calculated performance assessment.

Confidence increases as more recorded performances become available.

The system therefore separates:

**Performance Score + Data Confidence**

rather than combining them into a single metric.

This allows the dashboard to distinguish between:

* Strong performance with strong evidence
* Strong performance with limited evidence
* Lower performance with strong evidence
* Limited data requiring further observation

Data confidence is intended to describe the **strength of the available data sample**, not the quality or ability of the player.

---

## 📈 Performance Consistency

The platform also measures match-to-match performance consistency.

Consistency analysis examines variation in player performance across available matches.

### Batting Consistency

The batting consistency analysis considers:

* Runs
* Strike rate
* Match-to-match variation

### Bowling Consistency

The bowling consistency analysis considers:

* Wickets
* Economy rate
* Match-to-match variation

A consistency score is calculated when sufficient performance records are available.

Players with limited match records receive a lower data-confidence context rather than being treated as equally representative of long-term performance.

Consistency is presented as an additional descriptive metric and does not directly modify the overall performance score.

---

## 🏗️ System Architecture

Streamlit Dashboard
↓
Python Analytics
↓
Player Analytics | Match Analytics | Operations
↓
Batting | Bowling | Matches | Performance | Training | Injury | Equipment
↓
SQLAlchemy ORM
↓
SQLite Database
↓
Cricket Data Models

The architecture separates the application into:

* Presentation layer
* Analytics layer
* Database layer
* Data models
* Automated testing layer

This modular structure allows additional analytics and data sources to be added without redesigning the complete application.

---

## 🗄️ Database Design

The project uses a relational database with the following major entities:

Teams
└── Players
├── Batting Performances
├── Bowling Performances
├── Training Records
├── Injuries
└── Equipment

Matches
├── Batting Performances
└── Bowling Performances

Training Sessions
└── Training Records

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

cricket-sports-analytics/

├── analytics/
│   ├── **init**.py
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
│   ├── **init**.py
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
│   ├── **init**.py
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

The current test suite contains **36 tests**.

### Test Distribution

| Module      |  Tests |
| ----------- | -----: |
| Batting     |      6 |
| Bowling     |      6 |
| Equipment   |      5 |
| Injury      |      4 |
| Matches     |      5 |
| Performance |      5 |
| Training    |      5 |
| **Total**   | **36** |

Current result:

**36 passed**

The tests validate:

* Data availability
* Required fields
* Valid numerical ranges
* Player-specific calculations
* Match-level calculations
* Batting statistics
* Bowling statistics
* Batting consistency
* Bowling consistency
* Training metrics
* Training workload classification
* Equipment statistics
* Performance scoring
* Data confidence
* Injury statistics
* Player profile calculations

Run the complete test suite with:

`python -m pytest -v`

---

## 🚀 Installation

### 1. Clone the repository

`git clone https://github.com/banavii/cricket-sports-analytics.git`

`cd cricket-sports-analytics`

### 2. Create and activate a virtual environment

For example:

`python -m venv venv`

`source venv/bin/activate`

On Windows:

`venv\Scripts\activate`

### 3. Install dependencies

`pip install -r requirements.txt`

---

## 🗃️ Initialize the Database

Create the database tables:

`python -m database.init_db`

Populate the database with development data:

`python -m database.seed`

---

## ▶️ Run the Application

Start the Streamlit dashboard:

`streamlit run app.py`

The application will open in your browser.

---

## 📈 Dashboard

The main dashboard provides an executive-level overview of the cricket team.

It includes:

* Squad overview
* Player performance comparison
* Performance vs data confidence
* Training workload analysis
* Workload vs player performance
* Player availability
* Match result distribution
* Player performance summary
* Player consistency analysis
* System status

Additional pages provide detailed views for:

* Players
* Matches
* Training
* Injuries
* Equipment

---

## 🔬 Current Development Data

The current development dataset contains:

Teams: 2
Players: 8
Matches: 5
Batting: 10
Bowling: 6
Training: 5
Injuries: 2
Equipment: 4

The data is controlled seed data used for development, testing, and dashboard demonstration.

The current dataset is intentionally limited and is not intended to represent a complete real-world cricket dataset.

---

## 🚀 Version 2 — In Progress

Version 1 establishes the core database, analytics engine, operational modules, dashboard, and testing framework.

Development is continuing with Version 2 to expand the platform into a more advanced cricket intelligence system.

### 📚 Historical Cricket Data

Version 2 development includes work toward:

* Integration of larger historical cricket datasets
* Processing of ball-by-ball cricket data
* Expansion beyond controlled development data
* Historical player and match analysis

### 📊 Advanced Cricket Analytics

Planned and ongoing areas include:

* Phase-wise batting analysis
* Phase-wise bowling analysis
* Batter-bowler matchup analysis
* Venue-based performance
* Opponent-specific performance
* Player form analysis
* Advanced player comparison
* Team-level performance trends

### 🧮 Feature Engineering

Development of cricket-specific features from historical match data, including factors such as:

* Runs required
* Balls remaining
* Wickets remaining
* Current run rate
* Required run rate
* Batting and bowling phases
* Match situation
* Player and team performance indicators

### 🤖 Machine Learning

The Version 2 architecture will support investigation of machine learning applications such as:

* Player performance prediction
* Match situation analysis
* Win-probability estimation
* Player form analysis
* Workload-performance relationships

### 🏏 Cricket Win-Probability & Match Analytics

A continuing Version 2 direction is the development of a cricket match analytics engine capable of using the current match state to estimate the chasing team's win probability.

Potential inputs include:

Runs Required
+
Balls Remaining
+
Wickets in Hand
+
Venue
+
Match Context

The system will also expose the underlying cricket statistics and features used by the model.

---

## 🔮 Future Enhancements

Beyond the current Version 2 development direction, potential future improvements include:

### Advanced Analytics

* Real-time match analytics
* Advanced player comparison
* Team strategy analysis
* Venue-specific tactical insights
* Opponent-specific tactical analysis
* Automated performance reports

### Machine Learning

* Advanced player performance models
* Match outcome modelling
* Player workload modelling
* Injury-risk modelling
* Dynamic player form estimation

### Database

* PostgreSQL support
* Production database deployment
* Larger historical datasets
* Scalable data pipelines

### Application

* Authentication and role-based access
* Coach and player accounts
* Exportable reports
* Advanced filtering
* Automated reporting
* Cloud deployment
* Real-time data integration

---

## 📌 Project Status

### Version 1 — Completed ✅

The following components have been implemented and tested:

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
* [x] Data confidence
* [x] Batting consistency analysis
* [x] Bowling consistency analysis
* [x] Player profile integration
* [x] Streamlit dashboard
* [x] Streamlit analytics pages
* [x] Automated testing
* [x] 36/36 tests passing
* [x] Git version control
* [x] GitHub repository

### Version 2 — In Progress 🚧

* [ ] Larger historical cricket datasets
* [ ] Ball-by-ball data processing
* [ ] Advanced cricket feature engineering
* [ ] Advanced player analytics
* [ ] Expanded match analytics
* [ ] Cricket win-probability modelling
* [ ] Machine learning experimentation
* [ ] Advanced visualizations
* [ ] Expanded cricket intelligence features

Version 2 is being developed on top of the existing Version 1 database, analytics, and dashboard architecture.

---

## 👩‍💻 Author

Banavi

GitHub:

[https://github.com/banavii](https://github.com/banavii)

---

## 📄 License

This project is currently intended as a portfolio and academic development project.
