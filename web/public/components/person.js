import { createPersonRow } from './person/row.js';
import { createAlbumIcon } from './icons.js';
import { API_URL } from '../modules/api/url.js'

function mapTextToRow(row, nameCol, createdAtCol, lastSeenCol, photosCol) {
   row.querySelector('.person-name').appendChild(nameCol);
   row.querySelector('.person-created_at').appendChild(createdAtCol);
   row.querySelector('.person-last_seen').appendChild(lastSeenCol);
   row.querySelector('.person-photos').appendChild(photosCol);
}

export async function createPersonHeader() {
    const row = await createPersonRow();

    row.classList.add('text-bg-secondary');

    mapTextToRow(row,
        document.createTextNode('Name'),
        document.createTextNode('Created At'),
        document.createTextNode('Last Seen'),
        document.createTextNode('Photos'));

    return row;
}

function createSlideshowItem(person, photo) {
    const item = document.createElement('div');
    item.setAttribute('class', 'carousel-item');

    const img = document.createElement('img');
    img.setAttribute('src', `${API_URL}/people/${person.id}/photos/${photo}`);
    img.setAttribute('alt', person.text);
    img.setAttribute('class', 'm-auto w-auto d-block');

    item.appendChild(img);

    return item;
}

function populateSlideshow(person) {
    const slideshow = document.querySelector('.carousel-inner');
    slideshow.replaceChildren();

    for (const photo of person.photos) {
        slideshow.appendChild(createSlideshowItem(person, photo));
    }

    slideshow.firstElementChild.classList.add('active');
}

function createButton(person, icon) {
    const button = document.createElement('button');

    button.setAttribute('class', 'btn m-0 p-0');
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-toggle', 'modal');
    button.setAttribute('data-bs-target', '#slideshowModal');
    button.onclick = () => populateSlideshow(person);
    button.appendChild(icon);

    return button;
}



export async function createPersonItem(person) {
    const albumIcon = await createAlbumIcon();

    const row = await createPersonRow();

    mapTextToRow(row,
        document.createTextNode(person['text']),
        document.createTextNode(person['created_at']),
        document.createTextNode(person['last_seen'] || '-'),
        createButton(person, albumIcon));

    return row;
}