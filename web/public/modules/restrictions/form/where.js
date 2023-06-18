import { extractFromSelect, toSelect } from './utils.js';
import { fetchAreas } from '../../api/areas.js';
import { fetchAreaTypes } from '../../api/area_types.js';
import { fetchCameras } from '../../api/cameras.js';

function getCamerasElement() {
    return $('.select-cameras');
}

function getAreasElement() {
    return $('.select-areas');
}

function getAreaTypesElement() {
    return $('.select-area-types');
}

export function fetchWhere() {
    const where = [];

    for (const [type, element] of Object.entries({
        camera: getCamerasElement(),
        area: getAreasElement(),
        area_types: getAreaTypesElement()
    })) {
        const node = extractFromSelect(element, type);

        if (node)
            where.push(node);
    }

    if (where.length === 0)
        throw new Error('Must select WHERE to target!');

    return where;
}
export async function loadWhere() {
    await fetchCameras().then(data => getCamerasElement().select2({placeholder: 'Camera', data: toSelect(data)}));
    await fetchAreas().then(data => getAreasElement().select2({placeholder: 'Area', data: toSelect(data)}));
    await fetchAreaTypes().then(data => getAreaTypesElement().select2({placeholder: 'Area type', data: toSelect(data)}));
}