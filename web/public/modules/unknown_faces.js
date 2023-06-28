import { createNavigationBar } from '../components/navbar.js'
import { Tab } from './tab.js'
import {createUnknownClustersList} from "./unknown_clusters/unknown_clusters_list.js";

window.addEventListener('load', async () => {
	await createNavigationBar(Tab.UNKNOWN_FACES);

	await createUnknownClustersList();

	document.getElementById('cover').hidden = false;
});