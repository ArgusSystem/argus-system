import {Map} from './map.js'


class SightingsList {
    constructor () {
        this.parent = document.getElementById('sightings-list');

        this.map = new Map();

        this.activeItem = null;
    }

    init() {
        this.map.init();
    }

    add(camera, sighting) {
        const item = document.createElement('button');
        item.setAttribute('type', 'button');
        item.setAttribute('class', 'list-group-item list-group-item-action');

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

        const start_date = new Date(sighting.start_time);
        const end_date = new Date(sighting.end_time);
        const sightingText = `${camera.name} (${start_date.toLocaleTimeString()} - ${end_date.toLocaleTimeString()})`;
        item.appendChild(document.createTextNode(sightingText));

        this.parent.appendChild(item);

        // Update map
        this.map.addMarker(camera);
    }
}

const list = new SightingsList();

export function onSightings(cameras, sightings) {
    document.getElementById('sightings').removeAttribute('hidden');

    list.init();

    sightings.forEach(sighting => {
        list.add(cameras[sighting.camera_id], sighting);
    });
}