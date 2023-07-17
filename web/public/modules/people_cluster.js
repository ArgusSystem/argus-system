import { loadPage } from './page.js';
import { Tab } from './tab.js';
import { params } from './api/params.js';
import { createFaces } from '../components/unknown_faces.js';
import { fetchClusterFaces } from './api/unknown_clusters.js';
import { fetchPeople } from './api/people.js';

function createDropdownOption(element, person) {
    const li = document.createElement('li');
    li.classList.add('dropdown-item')
    li.innerText = person.name;
    element.appendChild(li);
}

loadPage(Tab.PEOPLE, async () => {
    const clusterId = params.id;

    document.getElementById('clusterId').innerText = `Clusters >> ${clusterId}`;

    const optionList = document.getElementById('tagging-options');
    (await fetchPeople()).forEach(person => createDropdownOption(optionList, person));
    await createFaces(await fetchClusterFaces(clusterId));
});