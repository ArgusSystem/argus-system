import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { createTableHeader, createTextNode, fetchHTMLElement, mapChildrenToRow } from '../components/utils.js';
import { fetchNotifications } from './api/notifications.js';
import { getUsername } from './session.js';
import { timestampToString } from './format.js';
import { redirectToNotification } from './notifications/utils.js';

const NOTIFICATIONS_TO_LOAD = 18;

async function createNotificationRow(){
    return await fetchHTMLElement('components/table_rows/notification.html');
}

async function createNotificationHeader() {
    return createTableHeader(await createNotificationRow(), 'Person', 'Place', 'Time', 'Restriction');
}

async function createNotificationItemRow(notification) {
    return mapChildrenToRow(await createNotificationRow(),
            createTextNode(notification.person),
            createTextNode(notification.place),
            createTextNode(timestampToString(notification.timestamp)),
            createTextNode('')
        );
}

loadPage(Tab.NOTIFICATIONS, async () => {
    const list = document.getElementById('notificationList');
    list.appendChild(await createNotificationHeader());

    for (const notification of (await fetchNotifications(getUsername(), NOTIFICATIONS_TO_LOAD))) {
        const row = await createNotificationItemRow(notification);
        row.onclick = async () => await redirectToNotification(notification);
        list.appendChild(row);
    }
});
