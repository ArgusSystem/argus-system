import { createNavigationBar } from '../components/navbar.js';
import { createFooter } from '../components/footer.js';
import { isSignedIn } from './session.js';
import { redirectToIndex } from './routing.js';

const NOOP_FUNCTION = () => {};

export class Page {
    static VIDEO = 'video.html';
    static CLUSTER = 'people-cluster.html';
    static CLUSTERS_LIST = 'people-unknown-faces.html';
    static NOTIFICATION = 'notification.html';
    static RESTRICTION = 'restriction.html';
}

export function loadPage(tab, callback = NOOP_FUNCTION) {
    window.addEventListener('load', async () => {
        if (!isSignedIn())
            redirectToIndex();

        await createNavigationBar(tab);
        await createFooter();

        await callback();

        document.getElementById('cover').hidden = false;
    });
}

