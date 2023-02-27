import { Tab, createNavigationBar } from '../components/navbar.js'
import { createFooter } from '../components/footer.js'

window.addEventListener('load', async () => {
    await createNavigationBar(Tab.HOME);
    await createFooter();

    document.getElementById('cover').hidden = false;
});
