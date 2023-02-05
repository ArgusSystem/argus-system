import { fetchRoles } from '../api/roles.js';
import { createRoleHeader, createRoleItem, createNewRoleItem } from '../../components/role.js'

export async function createRolesList() {
    const list = document.getElementById('roles-list');

    list.appendChild(await createRoleHeader());

   // const roles = await fetchRoles();
    const roles = [];
    for (const role of roles) {
        list.appendChild(await createRoleItem(role));
    }

    list.appendChild(await createNewRoleItem(null));
}