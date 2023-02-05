import { createNavigationBar, Tab } from '../components/navbar.js'
import { createPeopleList } from './people/people_list.js'
import { train_model_button } from '../components/person.js'

window.addEventListener('load', async () => {
	await createNavigationBar(Tab.PEOPLE);

    await createPeopleList();

    document.getElementById('train-model-button').onclick = train_model_button;

    document.getElementById('cover').hidden = false;
});