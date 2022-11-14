import { fetchPeople } from './api/people.js';
import { createAccordion } from './people/accordion.js'
import { createNavigationBar, Tab } from '../components/navbar.js'

window.addEventListener('load', async () => {
	await createNavigationBar(Tab.PEOPLE);

    const people = await fetchPeople();

    createAccordion(people);

    document.getElementById('cover').hidden = false;
});