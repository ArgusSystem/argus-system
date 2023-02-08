import { fetchRestrictions } from '../api/restrictions.js';
import { createRestrictionsHeader, createRestrictionsItem, createNewRestrictionItem } from '../../components/restrictions.js'
import {fetchRoles} from "../api/roles.js";
import {fetchAreaTypes} from "../api/area_types.js";

export async function createRestrictionsList() {
    const list = document.getElementById('restrictions-list');

    list.appendChild(await createRestrictionsHeader());

    const restrictions = await fetchRestrictions();
    const roles = await fetchRoles();
    const area_types = await fetchAreaTypes();
    for (const restriction of restrictions) {
        list.appendChild(await createRestrictionsItem(restriction, roles, area_types));
    }

    list.appendChild(await createNewRestrictionItem(roles, area_types));
}