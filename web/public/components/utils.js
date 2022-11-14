const PARSER = new DOMParser();

export function fetchHTMLElement(url) {
    return fetch(url)
        .then(data => data.text())
        .then(html => PARSER.parseFromString(html, 'text/html').body.firstElementChild);
}

