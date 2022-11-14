import { Tab, createNavigationBar } from '../components/navbar.js'

window.addEventListener('load', async () => {
    await createNavigationBar(Tab.HOME);

    document.getElementById('cover').hidden = false;
});
