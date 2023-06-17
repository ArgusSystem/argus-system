import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
} from "./utils.js";
import { daytimeToString, timestampToString } from '../modules/format.js';
import { redirect } from '../modules/routing.js';

async function createRestrictionRow(){
    return await fetchHTMLElement('components/table_rows/restriction.html');
}

export async function createRestrictionsHeader() {
    return createTableHeader(await createRestrictionRow(), "Id", "Who", "Where", "When", "Severity", "Save", "Delete");
}

function to_dict(array) {
    return array.reduce((result, value) => {
        result[value.id] = value.name;
        return result;
    }, {});
}

function format_with(node, mapping) {
    return node.map(n => {
        const type = mapping[n.type];
        return `${type[0]}: [${n.value.map(v => type[1][v]).join(', ')}]`
    }).join(', ');
}


function format_time(node) {
    return node.map(n => {
        if (n.type === 'repeated') {
            const day = n.value.days.length === 7 ?
                'Everyday' :
                n.value.days.map(d => d.substring(0, 2)).join(',');

            return `${day} ${daytimeToString(n.value['start_time'])} - ${daytimeToString(n.value['end_time'])}`;
        } else {
            return `${timestampToString(n.value['start_time'])} - ${timestampToString(n.value['end_time'])}`;
        }
    }).join(', ');
}

export async function createRestrictionsItem(restriction, people, roles, cameras, areas, areaTypes) {
    const row = await createRestrictionRow();

    const mapping = {
        'person': ['People', to_dict(people)],
        'role': ['Roles', to_dict(roles)],
        'camera': ['Cameras', to_dict(cameras)],
        'area': ['Areas', to_dict(areas)],
        'area_type': ['Area types', to_dict(areaTypes)]
    };

    return mapChildrenToRow(row,
        createTextNode(restriction['id']),
        createTextNode(format_with(restriction['rule']['who'], mapping)),
        createTextNode(format_with(restriction['rule']['where'], mapping)),
        createTextNode(format_time(restriction['rule']['when'])),
        createTextNode(restriction['severity']['name']),
        await createSaveButton(row, () => {}),
        await createDeleteButton(row, () => {})
    );
}

export async function loadRestrictions(restrictions, people, roles, cameras, areas, areaTypes) {
    const list = document.getElementById('restrictions-list');

    list.appendChild(await createRestrictionsHeader());

    for (const restriction of restrictions) {
        list.appendChild(await createRestrictionsItem(restriction, people, roles, cameras, areas, areaTypes));
    }

    const newRule = document.getElementById('new-rule');
    newRule.onclick = () => redirect('restriction.html');
}