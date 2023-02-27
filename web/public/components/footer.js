import { fetchHTMLElement } from './utils.js'

export async function createFooter() {
    const footer = await fetchHTMLElement('components/footer/footer.html');
    document.getElementById('footer').appendChild(footer);
}