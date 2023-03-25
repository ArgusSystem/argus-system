export function post(url, body) {
    return fetch(url, {
		method: 'POST',
		headers: {
      		"Content-Type": "application/json",
		},
		body: body
	});
}

export function remove(url) {
	return fetch(url, {method: 'DELETE'});
}