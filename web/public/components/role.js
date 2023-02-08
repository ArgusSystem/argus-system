import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";
import { API_URL } from '../modules/api/url.js'

async function createRoleRow(){
    return await fetchHTMLElement('components/table_rows/role.html');
}

export async function createRoleHeader() {
    return createTableHeader(await createRoleRow(), "Id", "Name", "Save", "Delete");
}

function _delete(row){
    let id = row.querySelector('.role-id').innerHTML;
    fetch(`${API_URL}/roles/${id}`, { method: 'DELETE' }).then(async (response) => {
        if (!response.ok) {
            alert("Role is still in use, DELETE failed");
        }
        else{
            // row.parentNode.removeChild(row);
            window.location.reload()
        }
    });
}

function _save(row){
    //console.log("save: ", row);
    let id = row.querySelector('.role-id').innerHTML;
    let name = row.querySelector('.role-name').querySelector('input#role_name_input').value;
    //console.log("save: ", id, name);
    fetch(`${API_URL}/roles/${id}/${name}`, { method: 'POST' }).then((response) => {
        response.json().then(async (body) => {
            if (response.ok && id === '-1') {
                // let list = row.parentNode;
                // list.removeChild(row);
                // list.appendChild(await createRoleItem({ id: body['role_id'], name: name }));
                // list.appendChild(await createNewRoleItem(null));
                window.location.reload()
            }
        });
    });
}

export async function createRoleItem(role) {
    let row = await createRoleRow();
    return mapChildrenToRow(row,
        createTextNode(role['id']),
        createInputTextNode('role_name_input', "", role['name']),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}

export async function createNewRoleItem() {
    let row = await createRoleRow();
    return mapChildrenToRow(row,
        createTextNode('-1'),
        createInputTextNode('role_name_input', '*new role name*'),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}