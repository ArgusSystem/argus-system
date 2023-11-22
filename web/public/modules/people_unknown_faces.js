import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { createUnknownClustersList } from './unknown_clusters/unknown_clusters_list.js';
import { fitClusters } from './api/unknown_clusters.js';
import { reload } from './routing.js';

loadPage(Tab.PEOPLE, async () => {
    document.getElementById('start-clustering-button').onclick = async () => {
      await fitClusters();
      reload();
    };

    await createUnknownClustersList();
});