import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";
import { API_URL } from '../modules/api/url.js'

async function createAreaTypeRow(){
    return await fetchHTMLElement('components/table_rows/area_type.html');
}

export async function createAreaTypesHeader() {
    return createTableHeader(await createAreaTypeRow(), "Id", "Name", "Save", "Delete");
}

function _delete(row){
    let id = row.querySelector('.area-type-id').innerHTML;
    fetch(`${API_URL}/area_types/${id}`, { method: 'DELETE' }).then(async (response) => {
        if (!response.ok) {
            alert("AreaType is still in use, DELETE failed");
        }
        else{
            // row.parentNode.removeChild(row);
            window.location.reload()
        }
    });
}

function _save(row){
    //console.log("save: ", row);
    let id = row.querySelector('.area-type-id').innerHTML;
    let name = row.querySelector('.area-type-name').querySelector('input#area_type_name_input').value;
    console.log("save: ", id, name);
    fetch(`${API_URL}/area_types/${id}/${name}`, { method: 'POST' }).then((response) => {
        response.json().then(async (body) => {
            if (response.ok && id === '-1') {
                window.location.reload()
            }
        });
    });
}

export async function createAreaTypesItem(area_type) {
    let row = await createAreaTypeRow();
    return mapChildrenToRow(row,
        createTextNode(area_type['id']),
        createInputTextNode('area_type_name_input', '', area_type['name']),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}

export async function createNewAreaTypeItem() {
    let row = await createAreaTypeRow();
    return mapChildrenToRow(row,
        createTextNode('-1'),
        createInputTextNode('area_type_name_input', '*new area type name*'),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}