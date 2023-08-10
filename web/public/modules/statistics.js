import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { GeneralStatistics } from './statistics/places/general_statistics.js';
import { loadTimeRange } from './history/time-range.js';
import {
    refreshAvgTimeSpent,
    refreshConcurrentVisits,
    refreshTrespassers,
    refreshWeekBarChart
} from './statistics/places/detail_statistics.js';

loadPage(Tab.STATISTICS, async () => {
    const generalStatistics = new GeneralStatistics();

    async function refresh(range) {
        const cameraId = await generalStatistics.refresh(range);
        await refreshWeekBarChart(cameraId, range);
        await refreshAvgTimeSpent(cameraId, range);
        await refreshTrespassers(cameraId, range);
        await refreshConcurrentVisits(cameraId, range);
    }

    loadTimeRange('statistics-range', refresh);
});