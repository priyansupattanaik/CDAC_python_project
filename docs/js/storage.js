const KEYS = {
  users: "quiz_users",
  results: "quiz_results",
  questions: "quiz_questions",
  seeded: "quiz_seeded"
};

function getUsers() {
  return JSON.parse(localStorage.getItem(KEYS.users) || "[]");
}

function saveUsers(users) {
  localStorage.setItem(KEYS.users, JSON.stringify(users));
}

function getResults() {
  return JSON.parse(localStorage.getItem(KEYS.results) || "[]");
}

function saveResults(results) {
  localStorage.setItem(KEYS.results, JSON.stringify(results));
}

function getQuestions() {
  return JSON.parse(localStorage.getItem(KEYS.questions) || "[]");
}

function saveQuestions(questions) {
  localStorage.setItem(KEYS.questions, JSON.stringify(questions));
}

function findUser(username, password) {
  const users = getUsers();
  for (const u of users) {
    if (u.username === username) {
      if (password === undefined || u.password === password) {
        return u;
      }
    }
  }
  return null;
}

function registerUser(name, username, password) {
  const users = getUsers();
  if (users.some((u) => u.username === username)) {
    return false;
  }
  let id = 1;
  if (users.length) {
    id = Math.max(...users.map((u) => u.id)) + 1;
  }
  users.push({ id, name, username, password });
  saveUsers(users);
  return true;
}

function changePassword(username, newPassword) {
  const users = getUsers();
  const user = users.find((u) => u.username === username);
  if (!user) return false;
  user.password = newPassword;
  saveUsers(users);
  return true;
}

function removeUser(username) {
  saveUsers(getUsers().filter((u) => u.username !== username));
  saveResults(getResults().filter((r) => r.username !== username));
}

function addResult(username, score, total) {
  const results = getResults();
  results.push({ username, score, total });
  saveResults(results);
}

function addQuestion(q, o1, o2, o3, o4, answer) {
  const questions = getQuestions();
  questions.push({ question: q, opt1: o1, opt2: o2, opt3: o3, opt4: o4, answer });
  saveQuestions(questions);
}

function getUserResults(username) {
  return getResults().filter((r) => r.username === username);
}

async function initStorage() {
  if (localStorage.getItem(KEYS.seeded)) {
    return;
  }

  try {
    const res = await fetch(asset("data/questions.json"));
    const questions = await res.json();
    saveQuestions(questions);
  } catch (e) {
    console.error("Could not load questions", e);
  }

  const sampleResults = [
    { username: "priyansu1", score: 5, total: 10 },
    { username: "priyansu1", score: 3, total: 10 },
    { username: "priyansu2", score: 3, total: 10 },
    { username: "priyansu", score: 4, total: 10 },
    { username: "abcd", score: 4, total: 10 }
  ];
  saveResults(sampleResults);
  localStorage.setItem(KEYS.seeded, "1");
}