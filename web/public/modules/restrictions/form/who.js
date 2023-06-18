import { fetchPeople } from '../../api/people.js';
import { fetchRoles } from '../../api/roles.js';
import { extractFromSelect, toSelect } from '../../../components/select2.js';
import { select } from './utils.js';


function getPeopleElement() {
    return $('.select-people');
}

function getRolesElement() {
    return $('.select-roles');
}

function getUnknownElement() {
    return document.getElementById('btn-unknown');
}

function getAllElement() {
    return document.getElementById('btn-all');
}

export function fetchWho() {
    let who = [];

    const people = extractFromSelect(getPeopleElement(), 'person');

    if (people)
        who.push(people);

    const roles = extractFromSelect(getRolesElement(), 'role');

    if (roles)
        who.push(roles);

    if (getUnknownElement().checked)
        who.push({type: 'unknown'})

    if (getAllElement().checked)
        who.push({type: 'all'})

    if (who.length === 0)
        throw new Error('Must select WHO to target!');

    return who;
}

export async function loadWho(restrictions) {
    await fetchPeople().then(data => getPeopleElement().select2({placeholder: 'Person', data: toSelect(data)}));
    await fetchRoles().then(data => getRolesElement().select2({placeholder: 'Roles', data: toSelect(data)}));

    if (restrictions) {
        select(restrictions, getPeopleElement(), 'person');
        select(restrictions, getRolesElement(), 'role');

        getUnknownElement().checked = restrictions.some(restriction => restriction.type === 'unknown');
        getAllElement().checked = restrictions.some(restriction => restriction.type === 'all');
    }
 }
