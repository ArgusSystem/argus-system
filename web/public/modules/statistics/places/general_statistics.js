import { fetchCameras } from '../../api/cameras.js';
import { clearBody, createHeader, createRow, setActiveRow } from '../../../components/table.js';
import { Map } from '../../../components/map.js';
import { fetchVisits } from '../../api/statistics.js';
import { refreshDetailedStatistics } from './detail_statistics.js';

const HEADERS = ['Camera', 'Area', 'Visits'];

export class GeneralStatistics {

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

        let cameraId = null;

        cameras.forEach((camera, index) => {
            this._map.addMarker(camera);

            const row = createRow(this._table, camera.name, [camera.area, visits[camera.id] | '0']);
            row.onclick = () => {
                this._map.focus(camera.id);
                setActiveRow(this._table, row);
                refreshDetailedStatistics(camera.id, range);
            };

            if (index === 0) {
                setActiveRow(this._table, row);
                cameraId = camera.id;
            }
        });

        return cameraId;
    }
}