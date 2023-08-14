import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { GeneralStatistics } from './statistics/places/general_statistics.js';
import { loadTimeRange } from './history/time-range.js';
import { refreshDetailedStatistics } from './statistics/places/detail_statistics.js';

loadPage(Tab.STATISTICS, async () => {
    const generalStatistics = new GeneralStatistics();

    async function refresh(range) {
        const cameraId = await generalStatistics.refresh(range);
        await refreshDetailedStatistics(cameraId, range);
    }

    loadTimeRange('statistics-range', refresh);
});