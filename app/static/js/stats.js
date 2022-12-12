function cateChart(labels, data) {
  const ctx = document.getElementById("cateChart");

  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Số lượng",
          data: data,
          borderWidth: 1,
          // backgroundColor: ["#ff6384", "#36a2eb", "#cc65fe", "#ffce56"],
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}

function revenueChart(labels, data) {
  const ctx = document.getElementById("revenueChart");

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Doanh thu",
          data: data,
          borderWidth: 1,
          backgroundColor: ["red", "green", "blue", "gold", "brown"],
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}
