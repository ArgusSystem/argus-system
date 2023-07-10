import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { createUnknownClustersList } from './unknown_clusters/unknown_clusters_list.js';

loadPage(Tab.PEOPLE, async () => {
    await createUnknownClustersList();
});