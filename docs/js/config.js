const BASE_PATH = (function () {
  if (location.pathname.includes("/CDAC_python_project")) {
    return "/CDAC_python_project";
  }
  return "";
})();

function page(path) {
  return BASE_PATH + "/" + path;
}

function asset(path) {
  return BASE_PATH + "/" + path;
}