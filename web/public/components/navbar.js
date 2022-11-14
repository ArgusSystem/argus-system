export class Tab {
    static HOME = new Tab('Home', 'index.html');
    static LIVE_FEED = new Tab('Live Feed', 'video.html');
    static HISTORY = new Tab('History', 'history.html');

    constructor (name, page) {
        this.name = name;
        this.page = page;
    }

    static values() {
        return Object.keys(Tab).map(attribute => Tab[attribute]);
    }
}

function getCollapseId() {
    return 'navbar-collapse';
}

function createLink(tab) {
    const link = document.createElement('a');
    link.setAttribute('href', tab.page);
    link.setAttribute('class', 'nav-link');
    link.innerHTML = tab.name;
    return link;
}

function createContainer() {
    const container = document.createElement('div');
    container.setAttribute('class', 'container-fluid');
    return container;
}

function createNavBarToggle() {
    const button = document.createElement('button');

    button.setAttribute('class', 'navbar-toggler');

    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-toggle', 'collapse');
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-label', 'Toggle navigation');

    const collapseId = getCollapseId();
    button.setAttribute('data-bs-target', `#${collapseId}`);
    button.setAttribute('aria-controls', collapseId);

    const span = document.createElement('span');
    span.setAttribute('class', 'navbar-toggler-icon');

    button.appendChild(span);

    return button;
}

function createBrand() {
    const link = document.createElement('a');
    link.setAttribute('href', Tab.HOME.page);
    link.setAttribute('class', 'navbar-brand');
    link.innerHTML = 'Argus';
    return link;
}

function createCollapse(activeTab) {
    const collapse = document.createElement('div');
    collapse.setAttribute('id', getCollapseId());
    collapse.setAttribute('class', 'collapse navbar-collapse');

    const nav = document.createElement('div');
    nav.setAttribute('class', 'navbar-nav');

    Tab.values().forEach(tab => {
        const link = createLink(tab);

        if (tab === activeTab){
            link.setAttribute('aria-current', 'page');
            link.classList.add('active');
        }

        nav.appendChild(link);
    });

    collapse.appendChild(nav);

    return collapse;
}

export function createNavigationBar(activeTab) {
    const navBar = document.querySelector('.navbar');
    navBar.classList.add('navbar-expand-lg', 'navbar-dark', 'bg-primary');
    const container = createContainer();

    container.appendChild(createBrand());
    container.appendChild(createNavBarToggle());
    container.appendChild(createCollapse(activeTab));

    navBar.appendChild(container);
}
