import {
    createTextNode,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
} from "./utils.js";
import { daytimeToString, timestampToString } from '../modules/format.js';
import { redirect, reload } from '../modules/routing.js';
import { createRemoveButton, createUpdateButton } from './management.js';
import { deleteRestriction } from '../modules/api/restrictions.js';

async function createRestrictionRow(){
    return await fetchHTMLElement('components/table_rows/restriction.html');
}

async function createRestrictionsHeader() {
    return createTableHeader(await createRestrictionRow(), "Who", "Where", "When", "Severity", "");
}

function to_dict(array) {
    return array.reduce((result, value) => {
        result[value.id] = value.name;
        return result;
    }, {});
}

function format_with(node, mapping) {
    return node.map(n => {
        if (!(n.type in mapping))
            return n.type.toUpperCase();

        const type = mapping[n.type];
        return `${type[0]}: [${n.value.map(v => type[1][v]).join(', ')}]`;
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

function redirectToRestriction(params={}) {
    redirect('restriction.html', params);
}

function _deleteRestriction(id) {
    return deleteRestriction(id).then(reload);
}

function createManagement(restrictionId) {
    const div = document.createElement('div');
    div.appendChild(createUpdateButton(() => redirectToRestriction({ restrictionId })));
    div.appendChild(createRemoveButton(async () => await _deleteRestriction(restrictionId)));
    return div;
}

async function createRestrictionsItem(restriction, people, roles, cameras, areas, areaTypes) {
    const row = await createRestrictionRow();

    const mapping = {
        'person': ['People', to_dict(people)],
        'role': ['Roles', to_dict(roles)],
        'camera': ['Cameras', to_dict(cameras)],
        'area': ['Areas', to_dict(areas)],
        'area_type': ['Area types', to_dict(areaTypes)]
    };

    return mapChildrenToRow(row,
        createTextNode(format_with(restriction['rule']['who'], mapping)),
        createTextNode(format_with(restriction['rule']['where'], mapping)),
        createTextNode(format_time(restriction['rule']['when'])),
        createTextNode(restriction['severity']['name']),
        createManagement(restriction.id)
    );
}

export async function loadRestrictions(restrictions, people, roles, cameras, areas, areaTypes) {
    const list = document.getElementById('restrictions-list');

    list.appendChild(await createRestrictionsHeader());

    for (const restriction of restrictions) {
        list.appendChild(await createRestrictionsItem(restriction, people, roles, cameras, areas, areaTypes));
    }

    const newRule = document.getElementById('new-rule');
    newRule.onclick = redirectToRestriction;
}