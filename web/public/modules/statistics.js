import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { loadPlaces } from './statistics/places.js';


loadPage(Tab.STATISTICS, async () => {
    await loadPlaces();
});