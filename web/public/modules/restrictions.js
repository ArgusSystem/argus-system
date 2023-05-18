import { createNavigationBar } from '../components/navbar.js'
import { createRestrictionsList } from './restrictions/restrictions.js'
import { isSignedIn } from './session.js'
import { Tab } from './tab.js'
import { redirectToIndex } from './routing.js';

window.addEventListener('load', async () => {
    if (!isSignedIn())
        redirectToIndex();

	await createNavigationBar(Tab.RESTRICTIONS);

    await createRestrictionsList();

    document.getElementById('cover').hidden = false;
});