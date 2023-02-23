import { fetchCameras } from '../api/cameras.js';
import { fetchAreas } from '../api/areas.js';
import { createCamerasHeader, createCamerasItem, createNewCameraItem } from '../../components/cameras.js'

export async function createCamerasList() {
    const list = document.getElementById('cameras-list');

    list.appendChild(await createCamerasHeader());

    const cameras = await fetchCameras();
    const areas = await fetchAreas();
    for (const camera of cameras) {
        list.appendChild(await createCamerasItem(camera, areas));
    }

    list.appendChild(await createNewCameraItem(areas));
}