import { fetchHTMLElement } from '../utils.js';

export async function createPersonRow() {
    return await fetchHTMLElement('components/person/row.html');
}