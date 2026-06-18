function getSession() {
  const raw = sessionStorage.getItem("quiz_session");
  return raw ? JSON.parse(raw) : null;
}

function setSession(data) {
  sessionStorage.setItem("quiz_session", JSON.stringify(data));
}

function clearSession() {
  sessionStorage.removeItem("quiz_session");
}

function requireAuth(role) {
  const session = getSession();
  if (!session) {
    location.href = page("index.html");
    return null;
  }
  if (role && session.role !== role) {
    location.href = page("dashboard.html");
    return null;
  }
  return session;
}

function login(username, password) {
  if (username === "admin" && password === "admin") {
    setSession({ username: "admin", name: "Admin", role: "Admin" });
    return { ok: true };
  }

  const user = findUser(username, password);
  if (user) {
    setSession({ username: user.username, name: user.name, role: "Student" });
    return { ok: true };
  }
  return { ok: false, msg: "Invalid credentials." };
}