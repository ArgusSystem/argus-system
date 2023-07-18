import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { params } from './api/params.js';
import { createFaces } from '../components/unknown_faces.js';
import { fetchClusterFaces } from './api/unknown_clusters.js';
import { loadReTaggingOptions } from './unknown_clusters/re_tagging.js';


loadPage(Tab.PEOPLE, async () => {
    const clusterId = params.id;

    document.getElementById('clusterId').innerText = `Clusters >> ${clusterId}`;

    await createFaces(await fetchClusterFaces(clusterId));

    await loadReTaggingOptions(clusterId);
});