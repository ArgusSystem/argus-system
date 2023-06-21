import { Tab } from './tab.js'
import { loadPage } from './page.js';
import { loadForm } from './restrictions/form.js';
import { params } from './api/params.js';
import { fetchRestriction } from './api/restrictions.js';

loadPage(Tab.RESTRICTIONS, async () => {
    const restriction = params.restrictionId ? await fetchRestriction(params.restrictionId) : null;
    await loadForm(restriction);
});
