import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE, "users.csv")
RESULTS_FILE = os.path.join(BASE, "results.csv")
QUESTIONS_FILE = os.path.join(BASE, "questions.csv")


def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["id", "name", "username", "password"])

    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["username", "score", "total"])


def read_users():
    rows = []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def write_users(users):
    with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "name", "username", "password"])
        w.writeheader()
        w.writerows(users)


def find_user(username, password=None):
    for u in read_users():
        if u["username"] == username:
            if password is None or u["password"] == password:
                return u
    return None


def register_user(name, username, password):
    users = read_users()
    for u in users:
        if u["username"] == username:
            return False

    uid = 1
    if users:
        uid = max(int(u["id"]) for u in users) + 1

    users.append({
        "id": str(uid),
        "name": name,
        "username": username,
        "password": password
    })
    write_users(users)
    return True


def change_password(username, new_password):
    users = read_users()
    updated = False
    for u in users:
        if u["username"] == username:
            u["password"] = new_password
            updated = True
            break
    if updated:
        write_users(users)
    return updated


def remove_user(username):
    users = [u for u in read_users() if u["username"] != username]
    write_users(users)

    results = [r for r in read_results() if r["username"] != username]
    write_results(results)


def read_results(username=None):
    if not os.path.exists(RESULTS_FILE):
        return []

    rows = []
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if username is None or row["username"] == username:
                rows.append(row)
    return rows


def write_results(results):
    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["username", "score", "total"])
        w.writeheader()
        w.writerows(results)


def add_result(username, score, total):
    results = read_results()
    results.append({"username": username, "score": str(score), "total": str(total)})
    write_results(results)


def read_questions():
    if not os.path.exists(QUESTIONS_FILE):
        return []

    questions = []
    for enc in ("utf-8", "cp1252"):
        try:
            with open(QUESTIONS_FILE, "r", encoding=enc) as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 6:
                        questions.append(row)
            break
        except UnicodeDecodeError:
            questions = []
            continue
    return questions


def add_question(q, o1, o2, o3, o4, answer):
    new_file = not os.path.exists(QUESTIONS_FILE)
    with open(QUESTIONS_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["question", "opt1", "opt2", "opt3", "opt4", "answer"])
        w.writerow([q, o1, o2, o3, o4, answer])


init_files()