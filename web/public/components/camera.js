import { fetchHTMLElement } from './utils.js'
import { API_URL } from '../modules/api/url.js'


export async function createCamera(camera) {
    const element = await fetchHTMLElement('components/camera/camera.html');
    element.querySelector('#camera-name').innerHTML = camera.name;

    const img = element.querySelector('#camera-img');
    img.setAttribute('src', `${API_URL}/cameras/${camera.id}/frame`);
    img.setAttribute('alt', camera.name);

    const link  = element.querySelector('#video-link');
    link.setAttribute('href', `video.html?camera=${camera.name}`);

    return element;
}
