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
import { deleteRestriction, insertRestriction, updateRestriction } from '../modules/api/restrictions.js';

export const RESTRICTION_SEVERITY_TYPES = [
    {'id':0, 'name':'info'},
    {'id':1, 'name':'warning'},
    {'id':2, 'name':'danger'}
];

export async function createRestrictionsHeader() {
    return createTableHeader(await createRestrictionRow(), "Id", "Role", "Area", "Severity", "Start", "End", "Save", "Delete");
}

async function createRestrictionRow(){
    return await fetchHTMLElement('components/table_rows/restriction.html');
}

function getValues(row) {
    return {
        id: row.querySelector('.restriction-id').innerHTML,
        role: row.querySelector('.restriction-role').querySelector('select#restriction_role_input').value,
        area: row.querySelector('.restriction-area').querySelector('select#restriction_area_input').value,
        severity: row.querySelector('.restriction-severity').querySelector('select#restriction_severity_input').value,
        start_time: row.querySelector('.restriction-time-start').querySelector('input#restriction_start_input').value,
        end_time: row.querySelector('.restriction-time-end').querySelector('input#restriction_end_input').value
    }
}

async function insert(row){
    const {role, area, severity, start_time, end_time} = getValues(row);

    return insertRestriction(role, area, severity, start_time, end_time).then(response => {
        if (response.ok)
            window.location.reload();
    });
}

async function update(row) {
    const {id, role, area, severity, start_time, end_time} = getValues(row);

    return updateRestriction(id, role, area, severity, start_time, end_time);
}


async function remove(row){
    const {id} = getValues(row);

    return deleteRestriction(id).then(response => {
        if (response.ok)
            window.location.reload();
        else
            alert("Restriction is still in use, DELETE failed");
    });
}


export async function createRestrictionsItem(restriction, roles, area_types) {
    const row = await createRestrictionRow();

    return mapChildrenToRow(row,
        createTextNode(restriction['id']),
        createInputDropdownNode("restriction_role_input", roles, restriction['role']),
        createInputDropdownNode("restriction_area_input", area_types, restriction['area']),
        createInputDropdownNode("restriction_severity_input", RESTRICTION_SEVERITY_TYPES,
            RESTRICTION_SEVERITY_TYPES[restriction['severity']]["name"]),
        createInputTextNode('restriction_start_input', '', restriction['start time']),
        createInputTextNode('restriction_end_input', '', restriction['end time']),
        await createSaveButton(row, update),
        await createDeleteButton(row, remove));
}

export async function createNewRestrictionItem(roles, area_types) {
    const row = await createRestrictionRow();

    return mapChildrenToRow(row,
        createTextNode('-1'),
        createInputDropdownNode("restriction_role_input", roles),
        createInputDropdownNode("restriction_area_input", area_types),
        createInputDropdownNode("restriction_severity_input", RESTRICTION_SEVERITY_TYPES),
        createInputTextNode('restriction_start_input', '*start time*'),
        createInputTextNode('restriction_end_input', '*end time*'),
        await createSaveButton(row, insert),
        await createDeleteButton(row, remove));
}