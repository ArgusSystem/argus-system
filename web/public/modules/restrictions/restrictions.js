// import { fetchRestrictions } from '../api/restrictions.js';
import { createRestrictionsHeader, createRestrictionsItem, createNewRestrictionItem } from '../../components/restrictions.js'

export async function createRestrictionsList() {
    const list = document.getElementById('restrictions-list');

    list.appendChild(await createRestrictionsHeader());

   // const restrictions = await fetchRestrictions();
    const restrictions = [];
    for (const restriction of restrictions) {
        list.appendChild(await createRestrictionsItem(restriction));
    }

    list.appendChild(await createNewRestrictionItem(null));
}