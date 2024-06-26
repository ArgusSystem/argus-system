import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { createTableHeader, createTextNode, fetchHTMLElement, mapChildrenToRow } from '../components/utils.js';
import { fetchNotifications } from './api/notifications.js';
import { getUsername } from './session.js';
import { timestampToString } from './format.js';
import { redirectToNotification } from './notifications/utils.js';
import { createRuleContext } from './rule.js';

const NOTIFICATIONS_TO_LOAD = 18;

const NOTIFICATION_COLOR = ['list-group-item-dark', 'list-group-item-warning', 'list-group-item-danger'];

async function createNotificationRow(){
    return await fetchHTMLElement('components/table_rows/notification.html');
}

async function createNotificationHeader() {
    return createTableHeader(await createNotificationRow(), 'Person', 'Place', 'Start Time', 'End Time', 'Restriction');
}

async function createNotificationItemRow(notification, ruleContext) {
    return mapChildrenToRow(await createNotificationRow(),
            createTextNode(notification.person),
            createTextNode(notification.place),
            createTextNode(timestampToString(notification.start_time)),
            createTextNode(timestampToString(notification.end_time)),
            createTextNode(ruleContext.formatToString(notification.restriction.rule))
        );
}

loadPage(Tab.NOTIFICATIONS, async () => {
    const list = document.getElementById('notificationList');
    list.appendChild(await createNotificationHeader());

    const ruleContext = await createRuleContext();

    for (const notification of (await fetchNotifications(getUsername(), NOTIFICATIONS_TO_LOAD))) {
        const row = await createNotificationItemRow(notification, ruleContext);

        if (!notification.read)
            row.classList.add(NOTIFICATION_COLOR[notification.restriction.severity], 'fw-bold');

        row.onclick = async () => await redirectToNotification(notification);
        list.appendChild(row);
    }
});
