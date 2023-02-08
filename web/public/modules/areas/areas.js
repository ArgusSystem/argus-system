import { fetchAreas } from '../api/areas.js';
import { createAreasHeader, createAreasItem, createNewAreaItem } from '../../components/areas.js'
import {fetchAreaTypes} from "../api/area_types.js";

export async function createAreasList() {
    const list = document.getElementById('areas-list');

    list.appendChild(await createAreasHeader());

    const areas = await fetchAreas();
    const area_types = await fetchAreaTypes();

    console.log(area_types);
    for (const area of areas) {
        list.appendChild(await createAreasItem(area, area_types));
    }

    list.appendChild(await createNewAreaItem(area_types));
}