import { Tab } from './tab.js'
import { loadPage } from './page.js';
import { loadRestrictions } from '../components/restrictions.js';
import { fetchRestrictions } from './api/restrictions.js';

loadPage(Tab.RESTRICTIONS, async () => {
    await loadRestrictions(await fetchRestrictions());
});
