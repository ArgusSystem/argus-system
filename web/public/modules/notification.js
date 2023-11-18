import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { params } from './api/params.js';
import { fetchNotification, getNotificationFaces, markNotificationRead } from './api/notifications.js';
import { createRuleContext } from './rule.js';
import { createDiv, createImg } from '../components/utils.js';
import { getFaceImageUrl } from './api/faces.js';

const FACE_WIDTH = 128;
const FACE_HEIGHT = 170;

function createFaceElement(face) {
    const col = createDiv('col');
    const img = createImg('face');

    img.src = getFaceImageUrl(face['image_key']);
    img.width = FACE_WIDTH;
    img.height = FACE_HEIGHT;

    col.appendChild(img);
    return col;
}

loadPage(Tab.NOTIFICATIONS, async () => {
    const notificationId = params.notificationId;
    document.getElementById('notificationId').innerText = notificationId;

    const notification = await fetchNotification(notificationId);
    const faces = await getNotificationFaces(notificationId);
    const gridElement = document.getElementById('notificationFaces');

    for (const face of faces) {
        gridElement.append(createFaceElement(face));
    }

    document.getElementById('offenderName').innerText = notification.person;
    document.getElementById('offenderPlace').innerText = notification.place;
    document.getElementById('offenderTime').innerText = new Date(notification.timestamp).toLocaleString();

    const ruleContext = await createRuleContext();
    document.getElementById('offenderRule').innerText = ruleContext.formatToString(notification.restriction.rule);

    if (!notification.read)
        await markNotificationRead(notificationId);
});
