import { createLink } from './link.js';
import { fetchHTMLElement } from './utils.js';

export class Tab {
    static HOME = new Tab('Home', 'index.html');
    static LIVE_FEED = new Tab('Live Feed', 'cameras.html');
    static HISTORY = new Tab('History', 'history.html');
    static PEOPLE = new Tab('People', 'people.html');

    constructor (name, page) {
        this.name = name;
        this.page = page;
    }

    static values() {
        return Object.keys(Tab).map(attribute => Tab[attribute]);
    }
}

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
}
