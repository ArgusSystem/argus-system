import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";

async function createRoleRow(){
    return await fetchHTMLElement('components/table_rows/role.html');
}

export async function createRoleHeader() {
    return createTableHeader(await createRoleRow(), "Name", "Save", "Delete");
}

function _delete(id){
    return null;
}

function _save(id){
    return null;
}

export async function createRoleItem(role) {
    return mapChildrenToRow(await createRoleRow(),
        createTextNode(role['name']),
        createSaveButton(role['id'], _save),
        createDeleteButton(role['id'], _delete));
}

export async function createNewRoleItem() {
    return mapChildrenToRow(await createRoleRow(),
        createInputTextNode('role_name_input', '*new role name*'),
        await createSaveButton(-1, _save),
        await createDeleteButton(-1, _delete));
}