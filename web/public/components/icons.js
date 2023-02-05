import { fetchHTMLElement } from './utils.js';

export async function createAlbumIcon() {
    return await fetchHTMLElement('components/icons/album.html');
}

export async function createAddIcon() {
    return await fetchHTMLElement('components/icons/add.html');
}

export async function createDeleteIcon() {
    return await fetchHTMLElement('components/icons/delete.html');
}