import { fetchAvgTimeSpent, fetchWeekDayHistogram } from '../../api/statistics.js';

const PRIMARY_COLOR = 'rgba(13, 110, 253, 0.8)';

export async function refreshWeekBarChart(camera, range) {
    const [start, end] = range;

    new Chart('week-bar-chart', {
        type: 'bar',
        data: {
            labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            datasets: [{
                data: await fetchWeekDayHistogram(camera, start, end),
                backgroundColor: Array(7).fill(PRIMARY_COLOR)
            }]
        },
        options: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Visits Distribution'
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

export async function refreshAvgTimeSpent(camera, range) {
    const [start, end] = range;
    const avgTimeSpent = await fetchAvgTimeSpent(camera, start, end);
    document.getElementById('avg-time-spent').innerText = `Average Time Spent: ${avgTimeSpent}`;
}