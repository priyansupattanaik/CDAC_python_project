from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, uid, name, username):
        self.uid = uid
        self.name = name
        self.username = username
        self._password = None

    def set_password(self, pwd):
        self._password = pwd

    def get_password(self):
        return self._password

    @abstractmethod
    def display(self):
        pass


class QuizUser(User):
    def __init__(self, uid, name, username):
        super().__init__(uid, name, username)
        self.total_quizzes = 0

    def display(self):
        print(f"Student: {self.name} | Username: {self.username}")


class Admin(User):
    def __init__(self):
        super().__init__(0, "Admin", "admin")
        self.set_password("admin")

    def display(self):
        print("--- Admin Dashboard ---")