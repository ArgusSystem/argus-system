import { fetchCameras } from '../api/cameras.js';
import { createHeader, createRow, setActiveRow } from '../../components/table.js';
import { Map } from '../../components/map.js';

const HEADERS = ['Camera', 'Area'];

export async function loadPlaces() {
    const table = document.querySelector('table');

    createHeader(table, HEADERS);

    const cameras = await fetchCameras();
    const map = new Map();
    map.init();

    cameras.forEach((camera, index) => {
        map.addMarker(camera);

        const row = createRow(table, camera.name, [camera.area]);
        row.onclick = () => {
            map.focus(camera.id);
            setActiveRow(table, row);
        };

        if (index === 0)
            setActiveRow(table, row);
    });
}