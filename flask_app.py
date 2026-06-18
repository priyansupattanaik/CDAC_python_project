import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd

import storage
from validators import validate_username, validate_password

app = Flask(__name__)
app.secret_key = "quiz_secret_key"


def plot_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode()
    plt.close(fig)
    return img


def get_student_df(username):
    rows = storage.read_results(username)
    if not rows:
        return None
    return pd.DataFrame(rows).astype({"score": int, "total": int})


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == "admin" and password == "admin":
            session["username"] = "admin"
            session["role"] = "Admin"
            return redirect(url_for("dashboard"))

        user = storage.find_user(username, password)
        if user:
            session["username"] = user["username"]
            session["name"] = user["name"]
            session["role"] = "Student"
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid credentials.", "error")

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not validate_username(username):
            flash("Username must be 3-20 letters or digits.", "error")
            return redirect(url_for("register"))
        if not validate_password(password):
            flash("Password must be at least 4 characters.", "error")
            return redirect(url_for("register"))

        if storage.register_user(name, username, password):
            flash("Registered! Please login.", "success")
            return redirect(url_for("login"))

        flash("Username already taken.", "error")

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    role = session["role"]
    username = session["username"]
    questions = storage.read_questions()

    if role == "Admin":
        results = storage.read_results()
        if not results:
            return render_template("dashboard.html", role=role, username=username,
                                   empty=True, questions=questions)

        users = {u["username"]: u["name"] for u in storage.read_users()}
        df = pd.DataFrame(results).astype({"score": int, "total": int})
        df["name"] = df["username"].map(users).fillna(df["username"])

        leaderboard = df.groupby(["username", "name"]).agg(
            Attempts=("score", "count"),
            Average_Score=("score", "mean")
        ).reset_index()
        leaderboard["Average Score"] = leaderboard["Average_Score"].round(1)
        leaderboard = leaderboard.sort_values("Average Score", ascending=False)

        leaderboard["Student Profile"] = leaderboard["name"] + " (@" + leaderboard["username"] + ")"
        leaderboard["Student Profile Link"] = leaderboard.apply(
            lambda r: f'<a href="{url_for("student_metrics", username=r["username"])}" '
                      f'style="color:#4a90e2;text-decoration:none;">{r["Student Profile"]}</a>',
            axis=1
        )

        table = leaderboard[["Student Profile Link", "Attempts", "Average Score"]].rename(
            columns={"Student Profile Link": "Student Profile"}
        )
        leaderboard_html = table.to_html(classes="table table-striped table-hover",
                                         index=False, escape=False)

        fig, ax = plt.subplots(figsize=(8, 4))
        labels = leaderboard["Student Profile"].tolist()
        scores = leaderboard["Average Score"].tolist()
        bars = ax.bar(labels, scores, color="steelblue", edgecolor="black")
        ax.set_ylim(0, 10)
        ax.set_title("Average Score per Student")
        ax.set_ylabel("Average Score")
        plt.xticks(rotation=45, ha="right")
        for bar, val in zip(bars, scores):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    f"{val}", ha="center")

        chart1 = plot_to_base64(fig)
        return render_template("dashboard.html", role=role, username=username, empty=False,
                               leaderboard=leaderboard_html, chart1=chart1, questions=questions)

    df = get_student_df(username)
    if df is None:
        return render_template("dashboard.html", role=role, username=username, empty=True)

    total_correct = int(df["score"].sum())
    total_wrong = int((df["total"] - df["score"]).sum())

    fig1, ax1 = plt.subplots(figsize=(5, 3))
    ax1.plot(range(1, len(df) + 1), df["score"], marker="o")
    ax1.set_title("Performance Over Time")
    ax1.set_xlabel("Attempt")
    ax1.set_ylabel("Score")
    ax1.grid(True)
    chart1 = plot_to_base64(fig1)

    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.pie([total_correct, total_wrong], labels=["Correct", "Wrong"],
            autopct="%1.1f%%", colors=["#66b3ff", "#ff9999"], startangle=90)
    ax2.set_title("Overall Accuracy")
    chart2 = plot_to_base64(fig2)

    return render_template("dashboard.html", role=role, username=username, empty=False,
                           quizzes=len(df), correct=total_correct, wrong=total_wrong,
                           avg=round(df["score"].mean(), 1), chart1=chart1, chart2=chart2)


@app.route("/student/<username>")
def student_metrics(username):
    if session.get("role") != "Admin":
        return redirect(url_for("login"))

    user = storage.find_user(username)
    if not user:
        flash("Student not found.", "error")
        return redirect(url_for("dashboard"))

    df = get_student_df(username)
    if df is None:
        return render_template("student_metrics.html", username=username,
                               name=user["name"], empty=True)

    total_correct = int(df["score"].sum())
    total_wrong = int((df["total"] - df["score"]).sum())

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(range(1, len(df) + 1), df["score"], marker="o")
    ax1.set_title(f"{user['name']}'s Performance Over Time")
    ax1.set_xlabel("Attempt")
    ax1.set_ylabel("Score")
    ax1.grid(True)
    chart1 = plot_to_base64(fig1)

    fig2, ax2 = plt.subplots(figsize=(5, 5))
    ax2.pie([total_correct, total_wrong], labels=["Correct", "Wrong"],
            autopct="%1.1f%%", colors=["#66b3ff", "#ff9999"], startangle=90)
    ax2.set_title(f"{user['name']}'s Overall Accuracy")
    chart2 = plot_to_base64(fig2)

    return render_template("student_metrics.html", username=username, name=user["name"],
                           empty=False, quizzes=len(df), correct=total_correct,
                           wrong=total_wrong, avg=round(df["score"].mean(), 1),
                           chart1=chart1, chart2=chart2)


@app.route("/take_quiz", methods=["GET", "POST"])
def take_quiz():
    if session.get("role") != "Student":
        return redirect(url_for("login"))

    questions = storage.read_questions()
    if not questions:
        flash("No questions available.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        score = 0
        for i, q in enumerate(questions):
            ans = request.form.get(f"q_{i}", "").strip()
            if ans == q[5].strip():
                score += 1

        total = len(questions)
        storage.add_result(session["username"], score, total)
        flash(f"Quiz done! Score: {score}/{total}", "success")
        return redirect(url_for("dashboard"))

    return render_template("take_quiz.html", questions=questions,
                           role=session["role"], username=session["username"])


@app.route("/add_question", methods=["GET", "POST"])
def add_question():
    if session.get("role") != "Admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        q = request.form.get("question", "").strip()
        o1 = request.form.get("opt1", "").strip()
        o2 = request.form.get("opt2", "").strip()
        o3 = request.form.get("opt3", "").strip()
        o4 = request.form.get("opt4", "").strip()
        ans_idx = request.form.get("answer", "")

        options = {"1": o1, "2": o2, "3": o3, "4": o4}
        if ans_idx in options:
            storage.add_question(q, o1, o2, o3, o4, options[ans_idx])
            flash("Question added.", "success")
            return redirect(url_for("dashboard"))

        flash("Pick a valid answer option.", "error")

    return render_template("add_question.html", role=session["role"],
                           username=session["username"])


@app.route("/update_password", methods=["GET", "POST"])
def update_password():
    if session.get("role") != "Student":
        return redirect(url_for("login"))

    if request.method == "POST":
        new_pwd = request.form.get("new_password", "")
        if not validate_password(new_pwd):
            flash("Password must be at least 4 characters.", "error")
            return redirect(url_for("update_password"))

        storage.change_password(session["username"], new_pwd)
        flash("Password updated.", "success")
        return redirect(url_for("dashboard"))

    return render_template("update_password.html", role=session["role"],
                           username=session["username"])


@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if session.get("role") != "Student":
        return redirect(url_for("login"))

    if request.method == "POST":
        if request.form.get("confirm") == "yes":
            storage.remove_user(session["username"])
            session.clear()
            flash("Account deleted.", "success")
            return redirect(url_for("login"))
        return redirect(url_for("dashboard"))

    return render_template("delete_account.html", role=session["role"],
                           username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)