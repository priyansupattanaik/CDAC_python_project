import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import storage
from models import QuizUser, Admin
from validators import validate_username, validate_password, validate_answer


def register():
    name = input("Enter full name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if not validate_username(username):
        print("Invalid username. Use 3-20 letters/digits.")
        return
    if not validate_password(password):
        print("Password must be at least 4 characters.")
        return

    if storage.register_user(name, username, password):
        print("Registered successfully!")
    else:
        print("Username already taken.")


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = storage.find_user(username, password)
    if user:
        print("Login successful!")
        u = QuizUser(int(user["id"]), user["name"], user["username"])
        u.set_password(password)
        return u

    print("Invalid credentials.")
    return None


def update_password(user):
    new_pwd = input("Enter new password: ")
    if not validate_password(new_pwd):
        print("Password too short.")
        return

    storage.change_password(user.username, new_pwd)
    user.set_password(new_pwd)
    print("Password updated!")


def delete_account(user):
    ans = input("Delete account permanently? (yes/no): ")
    if ans.lower() == "yes":
        storage.remove_user(user.username)
        print("Account deleted.")
        return True
    return False


def get_scores(username):
    rows = storage.read_results(username)
    if not rows:
        return None
    return pd.DataFrame(rows).astype({"score": int, "total": int})


def show_stats(username):
    df = get_scores(username)
    if df is None:
        print("No quiz data yet.")
        return

    print("--- Your Stats ---")
    print(f"Quizzes taken: {len(df)}")
    print(f"Correct answers: {df['score'].sum()}")
    print(f"Wrong answers: {(df['total'] - df['score']).sum()}")
    print(f"Average score: {round(df['score'].mean(), 2)}")


def show_line_chart(username):
    df = get_scores(username)
    if df is None:
        print("Take a quiz first to see the chart.")
        return

    plt.plot(range(1, len(df) + 1), df["score"], marker="o")
    plt.title("Scores Over Time")
    plt.xlabel("Attempt")
    plt.ylabel("Score")
    plt.show()


def show_pie_chart(username):
    df = get_scores(username)
    if df is None:
        print("Take a quiz first to see the chart.")
        return

    correct = int(df["score"].sum())
    wrong = int((df["total"] - df["score"]).sum())
    plt.pie([correct, wrong], labels=["Correct", "Wrong"], autopct="%1.1f%%")
    plt.title("Overall Accuracy")
    plt.show()


def start_quiz():
    questions = storage.read_questions()
    if not questions:
        print("No questions found!")
        return 0, 0

    score = 0
    for i, row in enumerate(questions, 1):
        print(f"\nQ{i}: {row[0]}")
        print(f"1. {row[1]}")
        print(f"2. {row[2]}")
        print(f"3. {row[3]}")
        print(f"4. {row[4]}")

        while True:
            ans = input("Your answer (1-4): ")
            if validate_answer(ans):
                break
            print("Enter a number between 1 and 4.")

        if row[int(ans)].strip() == row[5].strip():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. Answer is {row[5]}")

    return score, len(questions)


def add_question():
    q = input("Enter question: ")
    o1 = input("Option 1: ")
    o2 = input("Option 2: ")
    o3 = input("Option 3: ")
    o4 = input("Option 4: ")
    ans = input("Correct Answer (1-4): ")

    options = {"1": o1, "2": o2, "3": o3, "4": o4}
    if ans not in options:
        print("Invalid choice.")
        return

    storage.add_question(q, o1, o2, o3, o4, options[ans])
    print("Question added!")


def view_all_students():
    results = storage.read_results()
    if not results:
        print("No records found.")
        return

    users = {u["username"]: u["name"] for u in storage.read_users()}
    df = pd.DataFrame(results).astype({"score": int, "total": int})
    df["name"] = df["username"].map(users).fillna(df["username"])
    df = df[["name", "username", "score", "total"]]
    df.columns = ["Name", "Username", "Score", "Total"]
    print("--- All Student Records ---")
    print(df.to_string(index=False))


def show_student_chart():
    results = storage.read_results()
    if not results:
        print("No data to plot.")
        return

    users = {u["username"]: u["name"] for u in storage.read_users()}
    df = pd.DataFrame(results).astype({"score": int, "total": int})
    df["name"] = df["username"].map(users).fillna(df["username"])

    names = df["name"].unique()
    avg_scores = [df[df["name"] == n]["score"].mean() for n in names]

    x = np.arange(len(names))
    plt.figure(figsize=(8, 5))
    bars = plt.bar(x, avg_scores, color="steelblue", edgecolor="black", width=0.5)
    plt.xticks(x, names)
    plt.title("Average Score per Student")
    plt.xlabel("Student")
    plt.ylabel("Average Score")
    plt.ylim(0, 10)

    for bar, val in zip(bars, avg_scores):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(round(val, 1)), ha="center")

    plt.tight_layout()
    plt.show()


def view_student_metrics():
    students = storage.read_users()
    if not students:
        print("No students registered.")
        return

    print("\n--- Select a Student ---")
    for i, s in enumerate(students, 1):
        print(f"{i}. {s['name']} (@{s['username']})")

    try:
        choice = int(input("Enter student number: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice < 1 or choice > len(students):
        print("Invalid choice.")
        return

    picked = students[choice - 1]
    df = get_scores(picked["username"])
    if df is None:
        print(f"\n{picked['name']} hasn't taken any quizzes yet.")
        return

    print(f"\n--- {picked['name']}'s Metrics ---")
    print(f"Total Quizzes: {len(df)}")
    print(f"Correct Answers: {df['score'].sum()}")
    print(f"Wrong Answers: {(df['total'] - df['score']).sum()}")
    print(f"Average Score: {round(df['score'].mean(), 2)}")

    plt.plot(range(1, len(df) + 1), df["score"], marker="o")
    plt.title(f"{picked['name']}'s Scores Over Time")
    plt.xlabel("Attempt")
    plt.ylabel("Score")
    plt.show()

    correct = int(df["score"].sum())
    wrong = int((df["total"] - df["score"]).sum())
    plt.pie([correct, wrong], labels=["Correct", "Wrong"], autopct="%1.1f%%")
    plt.title(f"{picked['name']}'s Overall Accuracy")
    plt.show()


def student_menu(user):
    while True:
        print("\n--- Student Menu ---")
        user.display()
        print("1. Take Quiz")
        print("2. View Stats")
        print("3. View Line Chart")
        print("4. View Pie Chart")
        print("5. Change Password")
        print("6. Delete Account")
        print("7. Logout")

        try:
            opt = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input.")
            continue

        if opt == 1:
            score, total = start_quiz()
            if total > 0:
                print(f"Final Score: {score}/{total}")
                storage.add_result(user.username, score, total)
        elif opt == 2:
            show_stats(user.username)
        elif opt == 3:
            show_line_chart(user.username)
        elif opt == 4:
            show_pie_chart(user.username)
        elif opt == 5:
            update_password(user)
        elif opt == 6:
            if delete_account(user):
                break
        elif opt == 7:
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View All Students")
        print("2. Student Performance Chart")
        print("3. View Student Metrics")
        print("4. Add Question")
        print("5. Logout")

        try:
            opt = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input.")
            continue

        if opt == 1:
            view_all_students()
        elif opt == 2:
            show_student_chart()
        elif opt == 3:
            view_student_metrics()
        elif opt == 4:
            add_question()
        elif opt == 5:
            print("Admin logged out.")
            break
        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n===== Online Quiz System =====")
        print("1. Register")
        print("2. Login")
        print("3. Admin Login")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Enter a valid number.")
            continue

        if choice == 1:
            register()
        elif choice == 2:
            user = login()
            if user:
                student_menu(user)
        elif choice == 3:
            uname = input("Admin Username: ")
            pwd = input("Admin Password: ")
            admin = Admin()
            if uname == admin.username and pwd == admin.get_password():
                print("Admin login successful!")
                admin_menu()
            else:
                print("Invalid admin credentials.")
        elif choice == 4:
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()