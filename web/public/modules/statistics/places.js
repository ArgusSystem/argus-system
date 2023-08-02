import { fetchCameras } from '../api/cameras.js';


const HEADERS = ['Name', 'Area'];

const COL = 'col';
const ROW = 'row';

function tr() {
    return document.createElement('tr');
}

function th(text, scope) {
    const th = document.createElement('th');
    th.setAttribute('scope', scope);
    th.innerText = text;
    return th;
}

function td(text) {
    const td = document.createElement('td');
    td.innerText = text;
    return td;
}

export async function loadPlaces() {
    const headerNode = document.querySelector('thead');
    const headerTr = tr();
    headerNode.appendChild(headerTr)
    HEADERS.forEach(header => headerTr.appendChild(th(header, COL)));

    const bodyNode = document.querySelector('tbody');
    const cameras = await fetchCameras();
    cameras.forEach(camera => {
        const trNode = tr();
        bodyNode.appendChild(trNode);
        trNode.appendChild(th(camera.name, ROW));
        trNode.appendChild(td(camera.area));
    });
}