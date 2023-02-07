import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";

async function createAreaTypeRow(){
    return await fetchHTMLElement('components/table_rows/area_type.html');
}

export async function createAreaTypesHeader() {
    return createTableHeader(await createAreaTypeRow(), "Id", "Name", "Save", "Delete");
}

function _delete(id){
    return null;
}

function _save(id){
    return null;
}

export async function createAreaTypesItem(area_type) {
    return mapChildrenToRow(await createAreaTypeRow(),
        createTextNode(area_type['id']),
        createTextNode(area_type['name']),
        createSaveButton(area_type['id'], _save),
        createDeleteButton(area_type['id'], _delete));
}

export async function createNewAreaTypeItem() {
    return mapChildrenToRow(await createAreaTypeRow(),
        createInputTextNode('area_type_id_input', '-1'),
        createInputTextNode('area_type_name_input', '*new area type name*'),
        await createSaveButton(-1, _save),
        await createDeleteButton(-1, _delete));
}