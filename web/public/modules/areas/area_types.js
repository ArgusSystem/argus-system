import { fetchAreaTypes } from '../api/area_types.js';
import { createAreaTypesHeader, createAreaTypesItem, createNewAreaTypeItem } from '../../components/area_types.js'

export async function createAreaTypesList() {
    const list = document.getElementById('area-types-list');

    list.appendChild(await createAreaTypesHeader());

    const area_types = await fetchAreaTypes();
    for (const area_type of area_types) {
        list.appendChild(await createAreaTypesItem(area_type));
    }

    list.appendChild(await createNewAreaTypeItem(null));
}