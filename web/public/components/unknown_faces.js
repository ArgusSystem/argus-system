import { fetchHTMLElement } from './utils.js';
import { API_URL } from '../modules/api/url.js';

async function createUnknownFace(url){
    const face = await fetchHTMLElement('components/table_rows/unknown_face.html');
    face.querySelector('img').src = url;
    return face;
}

export async function createFaces(faces) {
    const grid = document.getElementById('face-grid');

    for (const {url} of faces) {
        grid.appendChild(await createUnknownFace(`${API_URL}/faces/${url}`));
    }
}
