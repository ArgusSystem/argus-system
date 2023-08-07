import { toTimestamp } from '../format.js';

const NOOP = () => {};

export function loadTimeRange(rangeId, onChange=NOOP) {
    const start = moment().subtract(29, 'days');
    const end = moment();
    
    function cb(start, end) {
        $(`#${rangeId} span`).html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        onChange([toTimestamp(start), toTimestamp(end)]);
    }
    
    $(`#${rangeId}`).daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'This Month': [moment().startOf('month'), moment().endOf('month')],
            'This Year': [moment().startOf('year'), moment().endOf('year')]
        }
    }, cb);
    
    cb(start, end);
}