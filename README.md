# Online Quiz System with Performance Analytics

A Python-based quiz application built for CDAC. Students can register, take quizzes, and view performance charts. Admins can manage questions and monitor student progress.

**Live Documentation:** [https://priyansupattanaik.github.io/CDAC_python_project/](https://priyansupattanaik.github.io/CDAC_python_project/)

> **Enable GitHub Pages (one-time):** Go to [Repository Settings → Pages](https://github.com/priyansupattanaik/CDAC_python_project/settings/pages), set **Source** to **Deploy from a branch**, choose branch **`gh-pages`** and folder **`/ (root)`**, then click **Save**. The site goes live in 1–2 minutes.

## Features

- Student registration and login
- Interactive quiz with multiple-choice questions
- Performance analytics (line chart, pie chart, stats)
- Admin dashboard with leaderboard
- Add new questions to the question bank
- CSV-based storage (no database setup needed)
- CLI and Web (Flask) interfaces

## Tech Stack

- Python 3.11+
- Flask (web interface)
- Pandas, NumPy, Matplotlib (analytics)
- CSV files for data storage

## Project Structure

```
CDAC_python_project/
├── main.py           # CLI application
├── flask_app.py      # Web application
├── storage.py        # CSV read/write
├── validators.py     # Input validation
├── models.py         # User classes
├── users.csv         # Registered users
├── results.csv       # Quiz results
├── questions.csv     # Question bank
├── requirements.txt
├── templates/        # HTML templates
└── docs/             # GitHub Pages documentation
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/priyansupattanaik/CDAC_python_project.git
cd CDAC_python_project
```

### 2. Create virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## How to Run

### Web Application (Recommended)

```bash
python flask_app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### CLI Application

```bash
python main.py
```

## Default Credentials

| Role    | Username | Password |
|---------|----------|----------|
| Admin   | admin    | admin    |

Students must register before logging in.

## Data Files

| File            | Purpose                          |
|-----------------|----------------------------------|
| `users.csv`     | Stores registered student accounts |
| `results.csv`   | Stores quiz attempt scores       |
| `questions.csv` | Stores quiz questions and answers |

## Admin Features

- View global leaderboard
- Average score bar chart per student
- Click any student to view detailed metrics
- Add new questions to the question bank

## Student Features

- Take quiz and get instant score
- View total quizzes, correct/wrong answers, average score
- Performance over time (line chart)
- Overall accuracy (pie chart)
- Update password or delete account

## Author

**Priyansu Pattanaik** — CDAC Python Project

## License

This project is for educational purposes.