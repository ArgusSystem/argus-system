import { createNavigationBar } from '../components/navbar.js'
import { createRolesList } from './people/roles_list.js'
import { createPeopleList } from './people/people_list.js'
import { train_model_button } from '../components/person.js'
import { isSignedIn } from './session.js'
import { Tab } from './tab.js'
import { redirectToIndex } from './routing.js';

window.addEventListener('load', async () => {
    if (!isSignedIn())
        redirectToIndex();

	await createNavigationBar(Tab.PEOPLE);

	await createRolesList();
    await createPeopleList();

    document.getElementById('train-model-button').onclick = train_model_button;

    document.getElementById('cover').hidden = false;
});