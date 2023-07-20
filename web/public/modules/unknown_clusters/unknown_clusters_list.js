import { fetchUnknownClusters } from '../api/unknown_clusters.js';
import { createUnknownClusterHeader, createUnknownClusterItem } from '../../components/unknown_cluster.js'

const CLUSTERS_COUNT = 15;

export async function createUnknownClustersList() {
    const list = document.getElementById('clusters-list');

    list.appendChild(await createUnknownClusterHeader());

    const unknown_clusters = await fetchUnknownClusters(CLUSTERS_COUNT);

    for (const cluster of unknown_clusters) {
        list.appendChild(await createUnknownClusterItem(cluster));
    }
}