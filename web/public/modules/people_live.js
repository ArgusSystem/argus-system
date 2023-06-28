import { loadPage } from './page.js';
import { Tab } from './tab.js';
import {Map} from '../components/map.js'
import { fetchCameras } from './api/cameras.js';
import { fetchPeople } from './api/people.js';
import { timestampToString } from './format.js';

function createDiv(klass, text=null) {
    const div = document.createElement('div');
    div.classList.add(klass);

    if (text)
        div.innerText = text;

    return div;
}

function createPersonItem(person) {
    const listItem = createDiv('list-group-item');

    const row = createDiv('row');
    listItem.appendChild(row);

    row.appendChild(createDiv('col', person.name));
    row.appendChild(createDiv('col', person.last_seen.place));
    row.appendChild(createDiv('col', timestampToString(person.last_seen.time)));

    return listItem;
}

loadPage(Tab.PEOPLE, async () => {
    const map = new Map();
    map.init();

    const cameras = await fetchCameras().then(cameras => cameras
        .reduce((r, c) => Object.assign(r, {[c.name]: c}), cameras));


    const people = await fetchPeople();

    const list = document.getElementById('live-people');

    for (const person of people
        .filter(p => p.last_seen !== null)
        .sort((a, b) => b.last_seen.time - a.last_seen.time)) {
        map.addMarker(cameras[person.last_seen.place]);
        list.appendChild(createPersonItem(person));
    }
});