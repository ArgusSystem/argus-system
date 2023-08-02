import { createLink } from './link.js';
import { fetchHTMLElement } from './utils.js';
import { Tab } from '../modules/tab.js';
import { getUsername, signOut } from '../modules/session.js';
import { createNotificationDropdown } from './notifications.js';


async function addTabs(activeTab) {
    const tabs = document.getElementById('tabs');

    for (const tab of Tab.values()) {
        const link = await createLink(tab.name, tab.page, 'nav-link', tab === activeTab);
        tabs.appendChild(link);
    }
}

async function loadNavigationBar() {
    document
        .getElementById('navigation-bar')
        .appendChild(await fetchHTMLElement('components/navbar/navbar.html'));

    document.querySelector('.navbar-brand').setAttribute('href', Tab.HOME.page);
}

export async function createNavigationBar(activeTab) {
    await loadNavigationBar();
    await addTabs(activeTab);
    await createNotificationDropdown();

    document.getElementById('userNameNavBar').innerText = `Hola, ${getUsername()}!`;
    document.getElementById('logOutLink').onclick = () => {
        signOut();
        return true;
    }
}
