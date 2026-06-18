function destroyChart(id) {
  const existing = Chart.getChart(id);
  if (existing) existing.destroy();
}

function lineChart(canvasId, scores, title) {
  destroyChart(canvasId);
  const labels = scores.map((_, i) => i + 1);
  return new Chart(document.getElementById(canvasId), {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Score",
        data: scores,
        borderColor: "#3b82f6",
        backgroundColor: "#3b82f6",
        tension: 0.1,
        pointRadius: 5
      }]
    },
    options: {
      responsive: true,
      plugins: { title: { display: true, text: title } },
      scales: { y: { beginAtZero: true, suggestedMax: 10 } }
    }
  });
}

function pieChart(canvasId, correct, wrong, title) {
  destroyChart(canvasId);
  return new Chart(document.getElementById(canvasId), {
    type: "pie",
    data: {
      labels: ["Correct", "Wrong"],
      datasets: [{
        data: [correct, wrong],
        backgroundColor: ["#66b3ff", "#ff9999"]
      }]
    },
    options: {
      responsive: true,
      plugins: { title: { display: true, text: title } }
    }
  });
}

function barChart(canvasId, labels, values, title) {
  destroyChart(canvasId);
  return new Chart(document.getElementById(canvasId), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Average Score",
        data: values,
        backgroundColor: "#4682b4",
        borderColor: "#333",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: { title: { display: true, text: title } },
      scales: { y: { beginAtZero: true, suggestedMax: 10 } }
    }
  });
}