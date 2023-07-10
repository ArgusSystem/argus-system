import {
    createTableHeader,
    mapChildrenToRow,
    createTextNode,
    fetchHTMLElement
} from "./utils.js";

async function createUnknownClusterRow(){
    return await fetchHTMLElement('components/table_rows/unknown_cluster.html');
}

export async function createUnknownClusterHeader() {
    return createTableHeader(await createUnknownClusterRow(), "Id", "Count");
}

export async function createUnknownClusterItem(cluster) {
    const row = await createUnknownClusterRow();

    mapChildrenToRow(row,
        createTextNode(cluster['id']),
        createTextNode(cluster['faces_count']));

    return row;
}