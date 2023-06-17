import { Tab } from './tab.js'
import { loadPage } from './page.js';
import { fetchPeople } from './api/people.js';
import { fetchRoles } from './api/roles.js';
import { fetchCameras } from './api/cameras.js';
import { fetchAreas } from './api/areas.js';
import { fetchAreaTypes } from './api/area_types.js';

function toSelect(data) {
    return data.map(d => {return {
        id: d.id,
        text: d.name
    }});
}


loadPage(Tab.RESTRICTIONS, async () => {
    await fetchPeople().then(data => $('.select-people').select2({placeholder: 'Person', data: data}));
    await fetchRoles().then(data => $('.select-roles').select2({placeholder: 'Role', data: toSelect(data)}));
    await fetchCameras().then(data => $('.select-cameras').select2({placeholder: 'Camera', data: toSelect(data)}));
    await fetchAreas().then(data => $('.select-areas').select2({placeholder: 'Area', data: toSelect(data)}));
    await fetchAreaTypes().then(data => $('.select-area-types').select2({placeholder: 'Area type', data: toSelect(data)}));
});
