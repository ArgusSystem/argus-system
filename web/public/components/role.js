import {createRoleRow} from "./role/row.js";
import {createDeleteIcon, createAddIcon} from "./icons.js";

function mapTextToRow(row, nameCol, deleteCol) {
   row.querySelector('.role-name').appendChild(nameCol);
   row.querySelector('.role-delete').appendChild(deleteCol);
}

export async function createRoleHeader() {
    const row = await createRoleRow();

    row.classList.add('text-bg-secondary');

    mapTextToRow(row,
        document.createTextNode('Name'),
        document.createTextNode('Delete'));

    return row;
}

function deleteRole(role_id){
    return null;
}

function createDeleteRoleButton(role, icon) {
    let button = document.createElement('button');

    button.setAttribute('class', 'btn m-0 p-0');
    button.setAttribute('type', 'button');

    button.onclick = () => deleteRole(role);
    button.appendChild(icon);

    return button;
}

export async function createRoleItem(role) {
    const deleteIcon = await createDeleteIcon();

    const row = await createRoleRow();

    mapTextToRow(row,
        document.createTextNode(role['name']),
        createDeleteRoleButton(role.id, deleteIcon));

    return row;
}

export async function createNewRoleItem() {
    const deleteIcon = await createAddIcon();

    const row = await createRoleRow();

    let role_name_input = document.createElement("input");
    role_name_input.setAttribute('type', 'text');
    role_name_input.setAttribute('id', 'role_name_input');
    role_name_input.setAttribute('placeholder', '*new role name*');

    mapTextToRow(row,
        role_name_input,
        createDeleteRoleButton(-1, deleteIcon));

    return row;
}