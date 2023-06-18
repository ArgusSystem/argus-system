export function toSelect(data) {
    return data.map(d => {return {
        id: d.id,
        text: d.name
    }});
}

export function extractFromSelect(element, type) {
    const ids = element.select2('data').map(e => parseInt(e.id));
    return ids.length > 0 ? {type, value: ids} : null;
}