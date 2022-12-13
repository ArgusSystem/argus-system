import { fetchHTMLElement } from './utils.js';

export async function createAlbumIcon() {
    return await fetchHTMLElement('components/icons/album.html');
}

export async function createAddIcon() {
    return await fetchHTMLElement('components/icons/add.html');
}