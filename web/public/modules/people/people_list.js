import { fetchPeople } from '../api/people.js';
import { createPersonHeader, createPersonItem, createNewPersonItem } from '../../components/person.js'
import {fetchRoles} from "../api/roles.js";

export async function createPeopleList() {
    const list = document.getElementById('people-list');

    list.appendChild(await createPersonHeader());

    const people = await fetchPeople();
    const roles = await fetchRoles();

    for (const person of people) {
        list.appendChild(await createPersonItem(person, roles));
    }

    list.appendChild(await createNewPersonItem(roles));
}