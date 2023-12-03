import { createRolesList } from './people/roles_list.js'
import { createPeopleList } from './people/people_list.js'
import { train_model_button } from '../components/person.js'
import { Tab } from './tab.js'
import { loadPage } from './page.js';
import { addLivePhotos } from './api/people.js';
import { reload } from './routing.js';

export async function onUpdateModelClick() {
    await (addLivePhotos().then(reload));
}

loadPage(Tab.PEOPLE, async () => {
	await createRolesList();
    await createPeopleList();

    document.getElementById('train-model-button').onclick = train_model_button;
});