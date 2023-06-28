import { createAlbumIcon } from './icons.js';
import { API_URL } from '../modules/api/url.js'
import {
    createTableHeader,
    mapChildrenToRow,
    createTextNode,
    fetchHTMLElement
} from "./utils.js";

async function createUnknownClusterRow(){
    return await fetchHTMLElement('components/table_rows/unknown_cluster.html');
}

export async function createUnknownClusterHeader() {
    return createTableHeader(await createUnknownClusterRow(), "Id", "Name", "Role", "Created At", "Last seen",
        "Photos", "Add Photos", "Save", "Delete");
}

function createSlideshowItem(cluster, face, index) {
    const item = document.createElement('div');
    item.setAttribute('class', 'carousel-item');

    const img = document.createElement('img');
    img.setAttribute('src', `${API_URL}/faces/${face}`);
    // img.setAttribute('alt', 'sample text');
    img.setAttribute('class', 'm-auto w-auto d-block');

    const title = document.createElement('h3');
    title.textContent = (index+1).toString() + " - " + face;
    title.style.textAlign = 'center';

    item.appendChild(title);
    item.appendChild(img);

    return item;
}

function populateSlideshow(cluster) {
    const slideshow = document.querySelector('.carousel-inner');
    slideshow.replaceChildren();

    console.log(cluster);
    for (let i = 0; i < cluster.faces.length; ++i) {
        slideshow.appendChild(createSlideshowItem(cluster, cluster.faces[i], i));
    }

    slideshow.firstElementChild.classList.add('active');
}

function createAlbumButton(cluster, icon) {
    let button = document.createElement('button');

    button.setAttribute('class', 'btn m-0 p-0');
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-toggle', 'modal');
    button.setAttribute('data-bs-target', '#slideshowModal');
    button.onclick = () => populateSlideshow(cluster);
    button.appendChild(icon);

    return button;
}

export async function createUnknownClusterItem(cluster) {
    const albumIcon = await createAlbumIcon();

    const row = await createUnknownClusterRow();

    mapChildrenToRow(row,
        createTextNode(cluster['id']),
        createAlbumButton(cluster, albumIcon));

    return row;
}