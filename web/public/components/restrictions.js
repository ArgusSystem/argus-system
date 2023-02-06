import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";

async function createRestrictionRow(){
    return await fetchHTMLElement('components/table_rows/restriction.html');
}

export async function createRestrictionsHeader() {
    return createTableHeader(await createRestrictionRow(), "Role", "Area", "Start", "End", "Save", "Delete");
}

function _delete(id){
    return null;
}

function _save(id){
    return null;
}

export async function createRestrictionsItem(restriction) {
    return mapChildrenToRow(await createRestrictionRow(),
        createTextNode(restriction['role']),
        createTextNode(restriction['area']),
        createTextNode(restriction['start time']),
        createTextNode(restriction['end time']),
        createSaveButton(restriction['id'], _save),
        createDeleteButton(restriction['id'], _delete));
}

export async function createNewRestrictionItem() {
    return mapChildrenToRow(await createRestrictionRow(),
        createInputTextNode('restriction_role_input', '*role*'),
        createInputTextNode('restriction_area_input', '*area*'),
        createInputTextNode('restriction_start_input', '*start time*'),
        createInputTextNode('restriction_end_input', '*end time*'),
        await createSaveButton(-1, _save),
        await createDeleteButton(-1, _delete));
}