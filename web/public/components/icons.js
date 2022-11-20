import { fetchHTMLElement } from './utils.js';

export async function createAlbumIcon() {
    return await fetchHTMLElement('components/icons/album.html');
}