// import { fetchAreas } from '../api/areas.js';
import { createAreasHeader, createAreasItem, createNewAreaItem } from '../../components/areas.js'

export async function createAreasList() {
    const list = document.getElementById('areas-list');

    list.appendChild(await createAreasHeader());

   // const areas = await fetchAreas();
    const areas = [];
    for (const area of areas) {
        list.appendChild(await createAreasItem(area));
    }

    list.appendChild(await createNewAreaItem(null));
}