import { markNotificationRead } from '../api/notifications.js';
import { redirect } from '../routing.js';
import { Page } from '../page.js';

export async function redirectToNotification(notification) {
    //if (!notification.read)
    await markNotificationRead(notification.user_id, notification.camera_id, notification.person_id,
        notification.restriction_id, notification.start_time);

    redirect(Page.NOTIFICATION,
        {
            user: notification.user_id,
            camera: notification.camera_id,
            person: notification.person_id,
            restriction: notification.restriction_id,
            startTime: notification.start_time
        });
}