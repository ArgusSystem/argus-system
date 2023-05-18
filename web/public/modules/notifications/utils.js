import { markNotificationRead } from '../api/notifications.js';
import { redirect } from '../routing.js';
import { Page } from '../page.js';

export async function redirectToNotification(notification) {
    if (!notification.read)
        await markNotificationRead(notification.id);

    redirect(Page.NOTIFICATION, {notificationId: notification.id});
}