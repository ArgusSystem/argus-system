import { fetchCameras } from '../api/cameras.js'
import { createCamera } from '../../components/camera.js'


export async function createCameras() {
    const row = document.getElementById('camera-list');

    const cameras = await fetchCameras();

    for (const camera of cameras) {
        row.appendChild(await createCamera(camera));
    }
}