function calcStats(rows) {
  const scores = rows.map((r) => r.score);
  const totals = rows.map((r) => r.total);
  let correct = 0;
  let wrong = 0;
  scores.forEach((s, i) => {
    correct += s;
    wrong += totals[i] - s;
  });
  const avg = scores.length ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1) : 0;
  return { count: rows.length, correct, wrong, avg, scores };
}

function renderStudentDashboard(session) {
  const rows = getUserResults(session.username);
  document.getElementById("studentActions").style.display = "block";
  document.getElementById("adminActions").style.display = "none";
  document.getElementById("adminQuestions").style.display = "none";

  if (!rows.length) {
    document.getElementById("content").innerHTML =
      '<div class="empty-state"><h3>No Data Available!</h3><p>Take a quiz to see your stats.</p></div>';
    return;
  }

  const s = calcStats(rows);
  document.getElementById("content").innerHTML = `
    <div class="stats-grid">
      <div class="stat-card"><h3>Total Quizzes</h3><p>${s.count}</p></div>
      <div class="stat-card"><h3>Correct Answers</h3><p>${s.correct}</p></div>
      <div class="stat-card"><h3>Wrong Answers</h3><p>${s.wrong}</p></div>
      <div class="stat-card"><h3>Average Score</h3><p>${s.avg}</p></div>
    </div>
    <div class="charts">
      <div class="chart-card"><canvas id="lineChart"></canvas></div>
      <div class="chart-card"><canvas id="pieChart"></canvas></div>
    </div>`;

  lineChart("lineChart", s.scores, "Performance Over Time");
  pieChart("pieChart", s.correct, s.wrong, "Overall Accuracy");
}

function renderAdminDashboard() {
  document.getElementById("studentActions").style.display = "none";
  document.getElementById("adminActions").style.display = "block";
  document.getElementById("adminQuestions").style.display = "block";

  const results = getResults();
  const users = getUsers();
  const nameMap = {};
  users.forEach((u) => { nameMap[u.username] = u.name; });

  renderQuestionBank();

  if (!results.length) {
    document.getElementById("content").innerHTML =
      '<div class="empty-state"><h3>No quiz records yet.</h3></div>';
    return;
  }

  const grouped = {};
  results.forEach((r) => {
    if (!grouped[r.username]) grouped[r.username] = [];
    grouped[r.username].push(r.score);
  });

  const leaderboard = Object.keys(grouped).map((uname) => {
    const scores = grouped[uname];
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
    const name = nameMap[uname] || uname;
    return { uname, name, attempts: scores.length, avg: avg.toFixed(1), profile: name + " (@" + uname + ")" };
  }).sort((a, b) => b.avg - a.avg);

  let tableRows = "";
  leaderboard.forEach((row) => {
    tableRows += `<tr>
      <td><a class="profile-link" href="${page("student-metrics.html")}?username=${row.uname}">${row.profile}</a></td>
      <td>${row.attempts}</td>
      <td>${row.avg}</td>
    </tr>`;
  });

  document.getElementById("content").innerHTML = `
    <div class="chart-card" style="margin-bottom:30px;">
      <canvas id="barChart"></canvas>
    </div>
    <h3 style="color:#2c3e50;">Global Leaderboard</h3>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Student Profile</th><th>Attempts</th><th>Average Score</th></tr></thead>
        <tbody>${tableRows}</tbody>
      </table>
    </div>`;

  barChart("barChart", leaderboard.map((r) => r.profile), leaderboard.map((r) => parseFloat(r.avg)),
    "Average Score per Student");
}

function renderQuestionBank() {
  const questions = getQuestions();
  const tbody = document.getElementById("qBody");
  if (!questions.length) {
    tbody.innerHTML = '<tr><td colspan="3" style="text-align:center;padding:20px;">No questions yet.</td></tr>';
    return;
  }
  tbody.innerHTML = questions.map((q, i) =>
    `<tr><td>${i + 1}</td><td style="white-space:pre-line;">${q.question}</td><td style="color:#27ae60;font-weight:bold;">${q.answer}</td></tr>`
  ).join("");
}