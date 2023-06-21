import { Tab } from './tab.js'
import { loadPage } from './page.js';
import { loadRestrictions } from '../components/restrictions.js';
import { fetchRestrictions } from './api/restrictions.js';
import { fetchRoles } from './api/roles.js';
import { fetchPeople } from './api/people.js';
import { fetchCameras } from './api/cameras.js';
import { fetchAreas } from './api/areas.js';
import { fetchAreaTypes } from './api/area_types.js';

loadPage(Tab.RESTRICTIONS, async () => {
    await loadRestrictions(
        await fetchRestrictions(),
        await fetchPeople(),
        await fetchRoles(),
        await fetchCameras(),
        await fetchAreas(),
        await fetchAreaTypes());
});
