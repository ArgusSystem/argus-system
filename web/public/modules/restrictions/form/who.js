import { fetchPeople } from '../../api/people.js';
import { fetchRoles } from '../../api/roles.js';
import { extractFromSelect, toSelect } from '../../../components/select2.js';
import { select } from './utils.js';

const PERSON = 'person';
const ROLE = 'role';
const UNKNOWN = 'unknown';
const ALL = 'all';

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

    const people = extractFromSelect(getPeopleElement(), PERSON);

    if (people)
        who.push(people);

    const roles = extractFromSelect(getRolesElement(), ROLE);

    if (roles)
        who.push(roles);

    if (getUnknownElement().checked)
        who.push({type: UNKNOWN})

    if (getAllElement().checked)
        who.push({type: ALL})

    if (who.length === 0)
        throw new Error('Must select WHO to target!');

    return who;
}

export async function loadWho(restrictions) {
    await fetchPeople().then(data => getPeopleElement().select2({placeholder: 'Person', data: toSelect(data)}));
    await fetchRoles().then(data => getRolesElement().select2({placeholder: 'Role', data: toSelect(data)}));

    if (restrictions) {
        select(restrictions, getPeopleElement(), PERSON);
        select(restrictions, getRolesElement(), ROLE);

        getUnknownElement().checked = restrictions.some(restriction => restriction.type === UNKNOWN);
        getAllElement().checked = restrictions.some(restriction => restriction.type === ALL);
    }
 }
