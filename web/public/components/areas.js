import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode,
    createInputDropdownNode
} from "./utils.js";
import { API_URL } from '../modules/api/url.js'

async function createAreaRow(){
    return await fetchHTMLElement('components/table_rows/area.html');
}

export async function createAreasHeader() {
    return createTableHeader(await createAreaRow(), "Id", "Name", "Type", "Save", "Delete");
}

function _delete(row){
    let id = row.querySelector('.area-id').innerHTML;
    fetch(`${API_URL}/areas/${id}`, { method: 'DELETE' }).then(async (response) => {
        if (!response.ok) {
            alert("Area is still in use, DELETE failed");
        }
        else{
            // row.parentNode.removeChild(row);
            window.location.reload()
        }
    });
}

function _save(row){
    //console.log("save: ", row);
    let id = row.querySelector('.area-id').innerHTML;
    let name = row.querySelector('.area-name').querySelector('input#area_name_input').value;
    let type = (row.querySelector('.area-type').querySelector('select#area_type_input').value);
    console.log("save: ", id, name, type);
    fetch(`${API_URL}/areas/${id}/${name}/${type}`, { method: 'POST' }).then((response) => {
        response.json().then(async (body) => {
            if (response.ok && id === '-1') {
                window.location.reload()
            }
        });
    });
}

export async function createAreasItem(area, area_types) {
    let row = await createAreaRow();
    return mapChildrenToRow(row,
        createTextNode(area['id']),
        createInputTextNode('area_name_input', '', area['name']),
        createInputDropdownNode("area_type_input", area_types, area['type']),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}

export async function createNewAreaItem(area_types) {
    let row = await createAreaRow();
    return mapChildrenToRow(row,
        createTextNode('-1'),
        createInputTextNode('area_name_input', '*new area name*'),
        createInputDropdownNode("area_type_input", area_types),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}