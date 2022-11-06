import {Map} from './map.js'


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

    add(camera, sighting) {
        const start_date = new Date(sighting.start_time);
        const end_date = new Date(sighting.end_time);

        this.#createDayNodeIfNecessary(end_date);


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

        item.appendChild(document.createTextNode(camera.name));
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
}

const list = new SightingsList();

export function onSightings(cameras, sightings) {
    document.getElementById('sightings').removeAttribute('hidden');

    list.init();

    sightings.forEach(sighting => {
        list.add(cameras[sighting.camera_id], sighting);
    });
}