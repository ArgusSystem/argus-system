import {Map} from '../../components/map.js'
import {createAlbumIcon} from "../../components/icons.js";
import {fetchHTMLElement} from "../../components/utils.js";
import {getFaceImageUrl} from "../api/faces.js";
import {API_URL} from "../api/url.js";
import {loadReTaggingOptions} from "../history/re_tagging.js";

let lastSelectedCheckbox = null;

class SightingsList {
    constructor () {
        this.parent = document.getElementById('sightings-list');

        this.map = new Map();

        this.activeItem = null;
        this.lastDay = null;
    }

    init() {
        this.parent.replaceChildren();
        this.activeItem = null;
        this.lastDay = null;
        this.map.init();
    }

    async add(camera, sighting) {
        const start_date = new Date(sighting.start_time);
        const end_date = new Date(sighting.end_time);

        this.#createDayNodeIfNecessary(end_date);


        const item = document.createElement('button');
        item.setAttribute('type', 'button');

        const color = sighting.severity ?? 'light';
        item.setAttribute('class', `list-group-item-action list-group-item-${color}`);

        // Only on first item added
        if (this.activeItem === null) {
            item.classList.add('active');
            this.activeItem = item;
        }

        const that = this;
        item.onclick =() => {
            that.activeItem.classList.remove('active');
            item.classList.add('active');
            that.activeItem = item;
            this.map.focus(camera.id);
        };

        item.appendChild(document.createTextNode(camera.name));
        var albumButton = await this.#createAlbumButton(sighting);
        item.appendChild(albumButton);
        item.appendChild(this.#createDateNode(start_date, end_date));

        this.parent.appendChild(item);

        // Update map
        this.map.addMarker(camera);
    }

    #createDayNodeIfNecessary(date) {
        const day = date.toLocaleDateString();

        if (this.lastDay === null || day !== this.lastDay) {
            const item = document.createElement('button');
            item.setAttribute('type', 'button');
            item.setAttribute('class', 'list-group-item list-group-item-dark text-muted');

            const text = document.createElement('em');
            text.appendChild(document.createTextNode(day));

            item.appendChild(text);

            this.parent.appendChild(item);
            this.lastDay = day;
        }
    }

    #createDateNode(start_date, end_date) {
        const span = document.createElement('span');
        span.setAttribute('class', 'sighting-time');
        span.innerText = `${start_date.toLocaleTimeString()} - ${end_date.toLocaleTimeString()}`;
        return span;
    }

    async #createAlbumButton(sighting) {
        let button = document.createElement('button');

        button.setAttribute('class', 'btn');
        button.setAttribute('type', 'button');
        button.setAttribute('data-bs-toggle', 'modal');
        button.setAttribute('data-bs-target', '#faces-modal');
        button.onclick = async () => create_album_callback(sighting) ;
        button.appendChild(await createAlbumIcon());

        return button;
    }
}

async function create_album_callback(sighting) {
    await createFaces(await fetchKnownFaces(
            sighting.camera_id,
            sighting.person_id,
            sighting.start_time,
            sighting.end_time
        ));

    await loadReTaggingOptions();
}

const list = new SightingsList();

export async function onSightings(cameras, sightings) {
    document.getElementById('sightings').removeAttribute('hidden');

    list.init();

    sightings.forEach(sighting => {
        list.add(cameras[sighting.camera_id], sighting);
    });
}

async function createSightingFace(face){
    const element = await fetchHTMLElement('components/table_rows/unknown_face.html');

    element.querySelector('img').src = getFaceImageUrl(face.url);

    const checkboxId = `checkbox-${face.id}`;
    const checkbox = element.querySelector('input');
    checkbox.id = checkboxId;
    checkbox.value = face.id;
    element.querySelector('label').setAttribute('for', checkboxId);

    element.addEventListener('click', (event) => {
        // If the click event originated from the checkbox, don't toggle again
        if (!event.target.matches('input[type="checkbox"]')) {
            checkbox.checked = !checkbox.checked;
        }
        // If shift was held, toggle all faces from the last selected to this one
        if (event.shiftKey && lastSelectedCheckbox) {
            const checkboxes = document.querySelectorAll('.form-check-input');
            const currentIndex = Array.from(checkboxes).indexOf(checkbox);
            const lastIndex = Array.from(checkboxes).indexOf(lastSelectedCheckbox);

            const start = Math.min(currentIndex, lastIndex);
            const end = Math.max(currentIndex, lastIndex);

            for (let i = start; i <= end; i++) {
                checkboxes[i].checked = checkbox.checked;
            }
        }
        lastSelectedCheckbox = checkbox;
    });

    return element;
}

async function createFaces(faces) {
    const parent = document.getElementById('face-grid-parent');
    parent.removeChild(parent.firstChild);

    let grid = document.createElement('div');
    grid.id = 'face-grid';
    grid.className = 'row row-cols-auto g-2';
    parent.appendChild(grid);

    for (const face of faces) {
        grid.appendChild(await createSightingFace(face));
    }
}

function fetchKnownFaces(camera, person, start_time, end_time) {
    return fetch(`${API_URL}/known_faces/${camera}/${person}/${start_time}/${end_time}`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch known faces!', error));
}