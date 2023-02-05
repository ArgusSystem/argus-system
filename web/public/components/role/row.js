import { fetchHTMLElement } from '../utils.js';

export async function createRoleRow() {
    return await fetchHTMLElement('components/role/row.html');
}