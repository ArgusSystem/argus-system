import { fetchUnknownClusters } from '../api/unknown_clusters.js';
import { createUnknownClusterHeader, createUnknownClusterItem } from '../../components/unknown_cluster.js'

export async function createUnknownClustersList() {
    const list = document.getElementById('clusters-list');

    list.appendChild(await createUnknownClusterHeader());

    const unknown_clusters = await fetchUnknownClusters();

    for (const cluster of unknown_clusters) {
        list.appendChild(await createUnknownClusterItem(cluster));
    }
}