import {
    createTextNode,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
} from "./utils.js";
import { redirect, reload } from '../modules/routing.js';
import { createRemoveButton, createUpdateButton } from './management.js';
import { deleteRestriction } from '../modules/api/restrictions.js';
import { RuleContext } from '../modules/rule.js';
import { Page } from '../modules/page.js';

async function createRestrictionRow(){
    return await fetchHTMLElement('components/table_rows/restriction.html');
}

async function createRestrictionsHeader() {
    return createTableHeader(await createRestrictionRow(), "Who", "Where", "When", "Severity", "");
}

function redirectToRestriction(params={}) {
    redirect(Page.RESTRICTION, params);
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

    const rule = new RuleContext(people, roles, cameras, areas, areaTypes).formatToStruct(restriction.rule);

    return mapChildrenToRow(row,
        createTextNode(rule.who),
        createTextNode(rule.where),
        createTextNode(rule.when),
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