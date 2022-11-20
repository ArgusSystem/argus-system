import { createNavigationBar, Tab } from '../components/navbar.js'
import { createPeopleList } from './people/people_list.js'

window.addEventListener('load', async () => {
	await createNavigationBar(Tab.PEOPLE);

    await createPeopleList();

    document.getElementById('cover').hidden = false;
});