const {protocol, hostname} = window.location;

export function fetchPeople() {
    return fetch(`${protocol}//${hostname}:5000/people`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}
