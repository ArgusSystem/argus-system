import { fetchPeople } from '../api/people.js';
import { createPersonHeader, createPersonItem, createNewPersonItem } from '../../components/person.js'

export async function createPeopleList() {
    const list = document.getElementById('people-list');

    list.appendChild(await createPersonHeader());

    const people = await fetchPeople();

    for (const person of people) {
        list.appendChild(await createPersonItem(person));
    }
    list.appendChild(await createNewPersonItem(null));
}