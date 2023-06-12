import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
} from "./utils.js";
import { daytimeToString, timestampToString } from '../modules/format.js';

async function createRestrictionRow(){
    return await fetchHTMLElement('components/table_rows/restriction.html');
}

export async function createRestrictionsHeader() {
    return createTableHeader(await createRestrictionRow(), "Id", "Who", "Where", "When", "Severity", "Save", "Delete");
}



// function getValues(row) {
//     return {
//         id: row.querySelector('.restriction-id').innerHTML,
//         role: row.querySelector('.restriction-role').querySelector('select#restriction_role_input').value,
//         area: row.querySelector('.restriction-area').querySelector('select#restriction_area_input').value,
//         severity: row.querySelector('.restriction-severity').querySelector('select#restriction_severity_input').value,
//         time_start: row.querySelector('.restriction-time-start').querySelector('input#restriction_start_input').value,
//         time_end: row.querySelector('.restriction-time-end').querySelector('input#restriction_end_input').value
//     }
// }
//
// async function insert(row){
//     const {role, area, severity, time_start, time_end} = getValues(row);
//
//     return insertRestriction(role, area, severity, time_start, time_end).then(response => {
//         if (response.ok)
//             window.location.reload();
//     });
// }
//
// async function update(row) {
//     const {id, role, area, severity, time_start, time_end} = getValues(row);
//
//     return updateRestriction(id, role, area, severity, time_start, time_end);
// }

//
// async function remove(row){
//     const {id} = getValues(row);
//
//     return deleteRestriction(id).then(response => {
//         if (response.ok)
//             window.location.reload();
//         else
//             alert("Restriction is still in use, DELETE failed");
//     });
// }

function format_time(time) {
    let time_str = '';

    if (time.type == 'repeated'){
        time_str += time.value.days.length == 7 ?
            'Everyday' :
            time.value.days.map(d => d.substring(0, 2)).join(',');

        time_str += ` ${daytimeToString(time.value['start_time'])} - ${daytimeToString(time.value['end_time'])}`;
    } else {
        time_str += `${timestampToString(time.value['start_time'])} - ${timestampToString(time.value['end_time'])}`;
    }


    return time_str;
}

export async function createRestrictionsItem(restriction) {
    const row = await createRestrictionRow();

    return mapChildrenToRow(row,
        createTextNode(restriction['id']),
        createTextNode(restriction['rule']['who']['value'].join(', ')),
        createTextNode(restriction['rule']['where']['value'].join(', ')),
        createTextNode(format_time(restriction['rule']['when'])),
        createTextNode(restriction['severity']['name']),
        await createSaveButton(row, () => {}),
        await createDeleteButton(row, () => {})
    );
}

// export async function createNewRestrictionItem(roles, area_types) {
//     const row = await createRestrictionRow();
//
//     return mapChildrenToRow(row,
//         createTextNode('-1'),
//         createInputDropdownNode("restriction_role_input", roles),
//         createInputDropdownNode("restriction_area_input", area_types),
//         createInputDropdownNode("restriction_severity_input", RESTRICTION_SEVERITY_TYPES),
//         createInputTextNode('restriction_start_input', '*start time*'),
//         createInputTextNode('restriction_end_input', '*end time*'),
//         await createSaveButton(row, insert),
//         await createDeleteButton(row, remove));
// }

export async function loadRestrictions(restrictions) {
    const list = document.getElementById('restrictions-list');

    list.appendChild(await createRestrictionsHeader());

    for (const restriction of restrictions) {
        list.appendChild(await createRestrictionsItem(restriction));
    }
}