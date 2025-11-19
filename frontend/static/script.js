document.addEventListener("DOMContentLoaded", function () {
    const barCtx = document.getElementById('barChart').getContext('2d');
    new Chart(barCtx, {
        type: 'bar',
        data: {
            labels: ['January', 'February', 'March', 'April'],
            datasets: [{
                label: 'Sales',
                data: [120, 150, 180, 200],
                backgroundColor: ['#FF5733', '#33FF57', '#3357FF', '#FF33A8']
            }]
        }
    });

    const pieCtx = document.getElementById('pieChart').getContext('2d');
    new Chart(pieCtx, {
        type: 'pie',
        data: {
            labels: ['Product A', 'Product B', 'Product C'],
            datasets: [{
                data: [3, 4.5, 2.5],
                backgroundColor: ['#FF5733', '#33FF57', '#3357FF']
            }]
        }
    });
});