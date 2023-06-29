import { loadPage } from './page.js';
import { Tab } from './tab.js';
import {Map} from '../components/map.js'
import { fetchCameras } from './api/cameras.js';
import { fetchPeople, getLastSeenPhotoURL } from './api/people.js';
import { timestampToString, toTimestamp } from './format.js';

function createDiv(klass, text=null) {
    const div = document.createElement('div');
    div.classList.add(klass);

    if (text)
        div.innerText = text;

    return div;
}

function createImageIcon(url) {
    const icon = document.createElement('i');
    icon.classList.add('fa', 'fa-image');
    icon.setAttribute('data-bs-toggle', 'modal');
    icon.setAttribute('data-bs-target', '#last-seen-photo-modal');
    icon.onclick = () => document.getElementById('person-modal').src = url;
    return icon;
}

function createPersonItem(person) {
    const listItem = createDiv('list-group-item');

    const row = createDiv('row');
    listItem.appendChild(row);

    row.appendChild(createDiv('col', person.name));
    row.appendChild(createDiv('col', person.last_seen.place));
    row.appendChild(createDiv('col', timestampToString(person.last_seen.time)));
    const icon = createDiv('col-1');
    icon.appendChild(createImageIcon(getLastSeenPhotoURL(person.last_seen.url)));
    row.appendChild(icon);

    return listItem;
}

async function refreshMap(map) {
    map.init();

    const cameras = await fetchCameras().then(cameras => cameras
        .reduce((r, c) => Object.assign(r, {[c.name]: c}), cameras));


    const people = await fetchPeople();

    const list = document.getElementById('live-person-item');
    list.replaceChildren();

    // Filter up to 5 minutes or set to 0 to avoid filtering
    const timeLowerBound = Date.now() - 5 * 60 * 1000;

    for (const person of people
        .filter(p => p.last_seen !== null && p.last_seen.time > timeLowerBound)
        .sort((a, b) => b.last_seen.time - a.last_seen.time)) {
        map.addMarker(cameras[person.last_seen.place]);
        list.appendChild(createPersonItem(person));
    }
}

loadPage(Tab.PEOPLE, async () => {
    const map = new Map();
    await refreshMap(map);

    // Refresh data every 30 seconds
    setInterval(async () => refreshMap(map), 30_000);
});