import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode,
    createInputDropdownNode
} from "./utils.js";
import { API_URL } from '../modules/api/url.js'

async function createRestrictionRow(){
    return await fetchHTMLElement('components/table_rows/restriction.html');
}

export async function createRestrictionsHeader() {
    return createTableHeader(await createRestrictionRow(), "Id", "Role", "Area", "Start", "End", "Save", "Delete");
}

function _delete(row){
    let id = row.querySelector('.restriction-id').innerHTML;
    fetch(`${API_URL}/restrictions/${id}`, { method: 'DELETE' }).then(async (response) => {
        if (!response.ok) {
            alert("Restriction is still in use, DELETE failed");
        }
        else{
            // row.parentNode.removeChild(row);
            window.location.reload()
        }
    });
}

function _save(row){
    //console.log("save: ", row);
    let id = row.querySelector('.restriction-id').innerHTML;
    let role = row.querySelector('.restriction-role').querySelector('select#restriction_role_input').value;
    let area = row.querySelector('.restriction-area').querySelector('select#restriction_area_input').value;
    let start_time = row.querySelector('.restriction-time-start').querySelector('input#restriction_start_input').value;
    let end_time = row.querySelector('.restriction-time-end').querySelector('input#restriction_end_input').value;
    //console.log("save: ", id, name, type);
    fetch(`${API_URL}/restrictions/${id}/${role}/${area}/${start_time}/${end_time}`, { method: 'POST' }).then((response) => {
        response.json().then(async (body) => {
            if (response.ok && id === '-1') {
                window.location.reload()
            }
        });
    });
}

export async function createRestrictionsItem(restriction, roles, area_types) {
    let row = await createRestrictionRow();
    return mapChildrenToRow(row,
        createTextNode(restriction['id']),
        createInputDropdownNode("restriction_role_input", roles, restriction['role']),
        createInputDropdownNode("restriction_area_input", area_types, restriction['area']),
        createInputTextNode('restriction_start_input', '', restriction['start time']),
        createInputTextNode('restriction_end_input', '', restriction['end time']),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}

export async function createNewRestrictionItem(roles, area_types) {
    let row = await createRestrictionRow();
    return mapChildrenToRow(row,
        createTextNode('-1'),
        createInputDropdownNode("restriction_role_input", roles),
        createInputDropdownNode("restriction_area_input", area_types),
        createInputTextNode('restriction_start_input', '*start time*'),
        createInputTextNode('restriction_end_input', '*end time*'),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}