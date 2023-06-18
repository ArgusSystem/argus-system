import { Tab } from './tab.js'
import { loadPage } from './page.js';
import { loadForm } from './restrictions/form.js';

loadPage(Tab.RESTRICTIONS, async () => {
    await loadForm();
});
