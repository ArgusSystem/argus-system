export function post(url, data) {
    return fetch(url, {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	});
}

export function remove(url) {
	return fetch(url, {method: 'DELETE'});
}