import { createNavigationBar } from '../components/navbar.js'
import { createFooter } from '../components/footer.js'
import { redirectToIndex, Tab } from './tab.js'
import { isSignedIn } from './session.js'

window.addEventListener('load', async () => {
    if (!isSignedIn())
        redirectToIndex();

    await createNavigationBar(Tab.HOME);
    await createFooter();

    document.getElementById('cover').hidden = false;
});
