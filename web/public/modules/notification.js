import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { params } from './api/params.js';
import { fetchNotification, markNotificationRead } from './api/notifications.js';

loadPage(Tab.NOTIFICATIONS, async () => {
    const notificationId = params.notificationId;
    document.getElementById('notificationId').innerText = notificationId;

    const notification = await fetchNotification(notificationId);

    document.getElementById('offenderName').innerText = notification.person;
    document.getElementById('offenderPlace').innerText = notification.place;
    document.getElementById('offenderTime').innerText = new Date(notification.timestamp).toLocaleString();

    if (!notification.read)
        await markNotificationRead(notificationId);
});
