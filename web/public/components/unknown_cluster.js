import {
    createTableHeader,
    mapChildrenToRow,
    createTextNode,
    fetchHTMLElement
} from "./utils.js";
import { redirect } from '../modules/routing.js';
import { Page } from '../modules/page.js';

async function createUnknownClusterRow(){
    return await fetchHTMLElement('components/table_rows/unknown_cluster.html');
}

export async function createUnknownClusterHeader() {
    return createTableHeader(await createUnknownClusterRow(), "Id", "Count");
}

export async function createUnknownClusterItem(cluster) {
    const row = await createUnknownClusterRow();

    const id = cluster.id;

    mapChildrenToRow(row,
        createTextNode(id),
        createTextNode(cluster['faces_count']));

    row.onclick = () => redirect(Page.CLUSTER, {id});

    return row;
}