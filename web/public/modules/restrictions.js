import { createNavigationBar, Tab } from '../components/navbar.js'
import { createRestrictionsList } from './restrictions/restrictions.js'

window.addEventListener('load', async () => {
	await createNavigationBar(Tab.RESTRICTIONS);

    await createRestrictionsList();

    document.getElementById('cover').hidden = false;
});