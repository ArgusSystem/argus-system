import { createCamera } from '../../components/camera.js'


export async function createCameras(cameras) {
    const row = document.getElementById('camera-list');

    for (const camera of cameras) {
        row.appendChild(await createCamera(camera));
    }
}