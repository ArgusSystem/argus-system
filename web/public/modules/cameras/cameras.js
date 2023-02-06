// import { fetchCameras } from '../api/areas.js';
import { createCamerasHeader, createCamerasItem, createNewCameraItem } from '../../components/cameras.js'

export async function createCamerasList() {
    const list = document.getElementById('cameras-list');

    list.appendChild(await createCamerasHeader());

   // const cameras = await fetchCameras();
    const cameras = [];
    for (const camera of cameras) {
        list.appendChild(await createCamerasItem(camera));
    }

    list.appendChild(await createNewCameraItem(null));
}