import { loadPage } from './page.js';
import { Tab } from './tab.js';
import {Map} from '../components/map.js'

loadPage(Tab.PEOPLE, async () => {
    const map = new Map();
    map.init();
});