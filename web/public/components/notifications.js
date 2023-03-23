async function fetchNotifications () {
    // TODO:  Actually fetch notifications
    return ['Notification 1', 'Notification 2', 'Notification 3'];
}

function createNotificationNode (text) {
    const li = document.createElement('li');

    li.setAttribute('class', 'dropdown-item fw-bold');
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

    span.setAttribute('style', 'position: absolute;' +
        ' top: -8px;' +
        ' right: 12px;' +
        ' padding: 3px 6px;' +
        ' border-radius: 50%;' +
        ' background: red;' +
        ' color: white;' +
        ' font-size: 0.9em;');

    span.innerText = `${notificationsCount}`;

    return span;
}

export async function createNotificationDropdown () {
    const list = document.getElementById('notificationList');
    const notifications = await fetchNotifications();

    for (let i = 0; i < notifications.length; i++) {
        if (i > 0)
            list.appendChild(createDivider());

        list.appendChild(createNotificationNode(notifications[i]));
    }

    if (notifications.length > 0)
        document
            .getElementById('notificationIcon')
            .appendChild(createBadge(notifications.length));
}