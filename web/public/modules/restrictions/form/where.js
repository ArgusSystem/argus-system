import { fetchAreas } from '../../api/areas.js';
import { fetchAreaTypes } from '../../api/area_types.js';
import { fetchCameras } from '../../api/cameras.js';
import { extractFromSelect, toSelect } from '../../../components/select2.js';
import { select } from './utils.js';

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
        area_type: getAreaTypesElement()
    })) {
        const node = extractFromSelect(element, type);

        if (node)
            where.push(node);
    }

    if (where.length === 0)
        throw new Error('Must select WHERE to target!');

    return where;
}
export async function loadWhere(restrictions) {
    await fetchCameras().then(data => getCamerasElement().select2({placeholder: 'Camera', data: toSelect(data)}));
    await fetchAreas().then(data => getAreasElement().select2({placeholder: 'Area', data: toSelect(data)}));
    await fetchAreaTypes().then(data => getAreaTypesElement().select2({placeholder: 'Area type', data: toSelect(data)}));

    if (restrictions) {
        select(restrictions, getCamerasElement(), 'camera');
        select(restrictions, getAreasElement(), 'area');
        select(restrictions, getAreaTypesElement(), 'area_type');
    }
}