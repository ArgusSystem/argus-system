import { fetchNotifications, fetchNotificationsCount } from '../modules/api/notifications.js';
import { getUsername } from '../modules/session.js';
import { redirect } from '../modules/routing.js';
import { Page } from '../modules/page.js';

const NOTIFICATIONS_TO_LOAD = 10;

function createNotificationNode (text) {
    const li = document.createElement('li');

    li.setAttribute('class', 'dropdown-item fw-bold');
    li.onclick = () => redirect(Page.NOTIFICATION);
    li.innerText = text;

    return li;
}

function createDivider () {
    const li = document.createElement('li');

    const hr = document.createElement('hr');
    hr.setAttribute('class', 'dropdown-divider');
    li.appendChild(hr);

    return li;
}

function createBadge(notificationsCount) {
    const span = document.createElement('span');

    // Resizing depending on notifications count
    const fontSize = 0.9 * ((2/3) ** (Math.floor(Math.log10(notificationsCount))))

    span.setAttribute('style', 'position: absolute;' +
        ' top: -8px;' +
        ' right: 12px;' +
        ' padding: 3px 6px;' +
        ' border-radius: 50%;' +
        ' background: red;' +
        ' color: white;' +
        ` font-size: ${fontSize.toPrecision(2)}em;`);

    span.innerText = notificationsCount;

    return span;
}

function format_notification(notification) {
    return `Persona no autorizada en ${notification['restriction']['area_type']} : ${notification['person']}`
}

export async function createNotificationDropdown () {
    const username = getUsername();

    const list = document.getElementById('notificationList');

    const notificationsCount = await fetchNotificationsCount(username);

    if (notificationsCount > 0)
        document.getElementById('notificationIcon').appendChild(createBadge(notificationsCount));

    const notifications = (await fetchNotifications(username, NOTIFICATIONS_TO_LOAD)).map(format_notification);

    for (let i = 0; i < notifications.length; i++) {
        if (i > 0)
            list.appendChild(createDivider());

        list.appendChild(createNotificationNode(notifications[i]));
    }
}
