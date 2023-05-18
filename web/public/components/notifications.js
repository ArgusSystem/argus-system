import { fetchNotifications, fetchNotificationsCount } from '../modules/api/notifications.js';
import { getUsername } from '../modules/session.js';
import { redirectToTab } from '../modules/routing.js';
import { Tab } from '../modules/tab.js';
import { redirectToNotification } from '../modules/notifications/utils.js';

const NOTIFICATIONS_TO_LOAD = 10;

const SEVERITY_TO_COLOR = ['text-primary', 'text-warning', 'text-danger']

function createWarningIcon(severity) {
    const icon = document.createElement('i');
    icon.classList.add('fa', 'fa-exclamation-triangle', 'd-inline', SEVERITY_TO_COLOR[severity]);
    icon.setAttribute('aria-hidden', 'true');
    return icon;
}

function createListNode() {
    const li = document.createElement('li');
    li.setAttribute('class', `dropdown-item`);
    return li;
}

function createNotificationNode (notification) {
    const li = createListNode();

    if (!notification.read)
        li.classList.add('fw-bold');

    li.appendChild(createWarningIcon(notification.severity));

    li.onclick = async () => redirectToNotification(notification);

    const p = document.createElement('p');
    p.innerText = notification.text;
    p.classList.add('d-inline', 'px-2')
    li.appendChild(p);

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

function createSeeAll() {
    const li = createListNode();
    li.classList.add('text-center');
    li.innerText = 'All Notifications';
    li.onclick = () => redirectToTab(Tab.NOTIFICATIONS);
    return li;
}

function toNotificationInformation(notification) {
    return {
        id: notification['id'],
        read: notification.read,
        severity: notification.restriction.severity,
        text: `Persona no autorizada en ${notification['restriction']['area_type']} : ${notification['person']}`
    }
}

export async function createNotificationDropdown () {
    const username = getUsername();

    const list = document.getElementById('notificationDropdown');

    const notificationsCount = await fetchNotificationsCount(username);

    if (notificationsCount > 0)
        document.getElementById('notificationIcon').appendChild(createBadge(notificationsCount));

    const notifications = (await fetchNotifications(username, NOTIFICATIONS_TO_LOAD)).map(toNotificationInformation);

    for (let i = 0; i < notifications.length; i++) {
        if (i > 0)
            list.appendChild(createDivider());

        list.appendChild(createNotificationNode(notifications[i]));
    }

    list.appendChild(createDivider());
    list.appendChild(createSeeAll());
}
