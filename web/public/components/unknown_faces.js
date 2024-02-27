import { fetchHTMLElement } from './utils.js';
import { timestampToISOString } from '../modules/format.js';
import { getFaceImageUrl } from '../modules/api/faces.js';

let lastSelectedCheckbox = null;

function updateOffcanvas(faceId, imgUrl, camera, timestamp, probability) {
    document.getElementById('face-image').src = imgUrl;
    document.getElementById('offcanvas-label').innerText = `Faces >> ${faceId}`;
    document.getElementById('face-location').innerText = camera;
    document.getElementById('face-time').innerText = timestampToISOString(timestamp);
    document.getElementById('face-probability').innerText = `${probability}`;
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

    element.addEventListener('click', (event) => {
        // If shift was held, toggle all faces from the last selected to this one
        if (event.shiftKey && lastSelectedCheckbox) {
            const checkboxes = document.querySelectorAll('.form-check-input');
            const currentIndex = Array.from(checkboxes).indexOf(checkbox);
            const lastIndex = Array.from(checkboxes).indexOf(lastSelectedCheckbox);

            const start = Math.min(currentIndex, lastIndex);
            const end = Math.max(currentIndex, lastIndex);

            for (let i = start; i <= end; i++) {
                checkboxes[i].checked = checkbox.checked;
            }
        }

        lastSelectedCheckbox = checkbox;
        updateOffcanvas(face.id, url, face.camera, face.timestamp, face.probability);
    });

    return element;
}

export async function createFaces(faces) {
    const grid = document.getElementById('face-grid');

    for (const face of faces) {
        grid.appendChild(await createUnknownFace(face));
    }
}
