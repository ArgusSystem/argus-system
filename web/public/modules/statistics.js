import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { PlacesStatistics } from './statistics/places.js';
import { loadTimeRange } from './history/time-range.js';

loadPage(Tab.STATISTICS, async () => {
    const statistics = new PlacesStatistics();
    loadTimeRange('statistics-range', statistics.refresh);
});