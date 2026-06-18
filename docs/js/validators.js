function validateUsername(username) {
  return /^[a-zA-Z0-9]{3,20}$/.test(username);
}

function validatePassword(password) {
  return password.length >= 4;
}