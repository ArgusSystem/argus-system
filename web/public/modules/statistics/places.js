import { fetchCameras } from '../api/cameras.js';
import { clearBody, createHeader, createRow, setActiveRow } from '../../components/table.js';
import { Map } from '../../components/map.js';
import { fetchVisits } from '../api/statistics.js';

const HEADERS = ['Camera', 'Area', 'Visits'];

export class PlacesStatistics {

    constructor () {
        this._table = document.querySelector('table');
        createHeader(this._table, HEADERS);

        this._map = new Map();
        this._map.init();
    }

    refresh = async (range) => {
        clearBody(this._table);

        const cameras = await fetchCameras();
        const [start, end] = range;
        const visits = await fetchVisits(start, end);

        cameras.sort((a, b) => (visits[b.id] | 0) - (visits[a.id] | 0));

        cameras.forEach((camera, index) => {
            this._map.addMarker(camera);

            const row = createRow(this._table, camera.name, [camera.area, visits[camera.id] | '0']);
            row.onclick = () => {
                this._map.focus(camera.id);
                setActiveRow(this._table, row);
            };

            if (index === 0)
                setActiveRow(this._table, row);
        });
    }
}