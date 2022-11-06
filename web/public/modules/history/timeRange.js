function cb(start, end) {
        $('#history-range span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
}

export function loadTimeRange() {
    const start = moment().subtract(29, 'days');
    const end = moment();

    $('#history-range').daterangepicker({
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
}

