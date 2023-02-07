import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";

async function createAreaRow(){
    return await fetchHTMLElement('components/table_rows/area.html');
}

export async function createAreasHeader() {
    return createTableHeader(await createAreaRow(), "Id", "Name", "Type", "Save", "Delete");
}

function _delete(id){
    return null;
}

function _save(id){
    return null;
}

export async function createAreasItem(area) {
    return mapChildrenToRow(await createAreaRow(),
        createTextNode(area['id']),
        createTextNode(area['name']),
        createTextNode(area['type']),
        createSaveButton(area['id'], _save),
        createDeleteButton(area['id'], _delete));
}

export async function createNewAreaItem() {
    return mapChildrenToRow(await createAreaRow(),
        createInputTextNode('area_id_input', '-1'),
        createInputTextNode('area_name_input', '*new area name*'),
        createInputTextNode('area_type_input', '*area type*'),
        await createSaveButton(-1, _save),
        await createDeleteButton(-1, _delete));
}