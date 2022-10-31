$(document).ready(() => {
	const {protocol, hostname} = window.location;

	fetch(`${protocol}//${hostname}:5000/people`)
		.then((response) => response.json())
		.then((people) => $("#personInput").autocomplete({source: people}))
		.catch((error) => console.error('Failed to fetch people!', error));

	const start = moment().subtract(29, 'days');
	const end = moment();

	function cb(start, end) {
			$('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
	}

	$('#reportrange').daterangepicker({
			startDate: start,
			endDate: end,
			ranges: {
				 'Today': [moment(), moment()],
				 'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
				 'Last 7 Days': [moment().subtract(6, 'days'), moment()],
				 'Last 30 Days': [moment().subtract(29, 'days'), moment()],
				 'This Month': [moment().startOf('month'), moment().endOf('month')],
				 'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
			}
	}, cb);

	cb(start, end);

	const map = L.map('map').setView([51.505, -0.09], 13);

	const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);
});

