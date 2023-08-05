import { fetchCameras } from '../api/cameras.js';
import { createHeader, createRow, setActiveRow } from '../../components/table.js';
import { Map } from '../../components/map.js';
import { fetchVisits } from '../api/statistics.js';

const HEADERS = ['Camera', 'Area', 'Visits'];

export async function loadPlaces() {
    const table = document.querySelector('table');

    createHeader(table, HEADERS);

    const cameras = await fetchCameras();
    const visits = await fetchVisits();
    const map = new Map();
    map.init();

    cameras.sort((a, b) => (visits[b.id] | 0) - (visits[a.id] | 0));

    cameras.forEach((camera, index) => {
        map.addMarker(camera);

        const row = createRow(table, camera.name, [camera.area, visits[camera.id] | '0']);
        row.onclick = () => {
            map.focus(camera.id);
            setActiveRow(table, row);
        };

        if (index === 0)
            setActiveRow(table, row);
    });
}