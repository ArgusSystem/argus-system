const PRIMARY_COLOR = 'rgba(13, 110, 253, 0.8)';

export async function refreshWeekBarChart(camera, range) {
    const yValues = [55, 49, 44, 24, 15, 7, 8];

    new Chart('week-bar-chart', {
        type: 'bar',
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            datasets: [{
                data: yValues,
                backgroundColor: Array(7).fill(PRIMARY_COLOR)
            }]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Daily Visits'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}