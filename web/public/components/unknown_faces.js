import { fetchHTMLElement } from './utils.js';
import { timestampToISOString } from '../modules/format.js';
import { getFaceImageUrl } from '../modules/api/faces.js';

function updateOffcanvas(faceId, imgUrl, camera, timestamp) {
    document.getElementById('face-image').src = imgUrl;
    document.getElementById('offcanvas-label').innerText = `Faces >> ${faceId}`;
    document.getElementById('face-location').innerText = camera;
    document.getElementById('face-time').innerText = timestampToISOString(timestamp);
}

async function createUnknownFace(face){
    const element = await fetchHTMLElement('components/table_rows/unknown_face.html');
    const url = getFaceImageUrl(face.url);

    element.querySelector('img').src = url;

    const checkboxId = `checkbox-${face.id}`;
    const checkbox = element.querySelector('input');
    checkbox.id = checkboxId;
    checkbox.value = face.id;
    element.querySelector('label').setAttribute('for', checkboxId);

    element.onclick = () => updateOffcanvas(face.id, url, face.camera, face.timestamp);

    return element;
}

export async function createFaces(faces) {
    const grid = document.getElementById('face-grid');

    for (const face of faces) {
        grid.appendChild(await createUnknownFace(face));
    }
}
