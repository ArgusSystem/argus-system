import { API_URL } from '../api/url.js'

function getSlideShowId(person) {
    return `slideshow-${person.id}`;
}

function createItem(person, photo) {
    const item = document.createElement('div');
    item.setAttribute('class', 'carousel-item');

    const img = document.createElement('img');
    img.setAttribute('src', `${API_URL}/people/${person.id}/photos/${photo}`);
    img.setAttribute('alt', person.text);
    img.setAttribute('class', 'd-block');

    item.appendChild(img);

    return item;
}


function createInner(person) {
    const inner = document.createElement('div');
    inner.setAttribute('class', 'carousel-inner');

    person.photos.forEach(photo => inner.appendChild(createItem(person, photo)));

    inner.firstElementChild.classList.add('active');

    return inner;
}

function createPrevButton(person) {
    const button = document.createElement('button');
    button.setAttribute('class', 'carousel-control-prev');
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-target', `#${getSlideShowId(person)}`);
    button.setAttribute('data-bs-slide', 'prev');

    const icon = document.createElement('span');
    icon.setAttribute('class', 'carousel-control-prev-icon');
    icon.setAttribute('aria-hidden', 'true');

    button.appendChild(icon);

    const span = document.createElement('span');
    span.setAttribute('class', 'visually-hidden');
    span.innerHTML = 'Previous';

    button.appendChild(span);

    return button;
}

function createNextButton(person) {
    const button = document.createElement('button');
    button.setAttribute('class', 'carousel-control-next');
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-target', `#${getSlideShowId(person)}`);
    button.setAttribute('data-bs-slide', 'next');

    const icon = document.createElement('span');
    icon.setAttribute('class', 'carousel-control-next-icon');
    icon.setAttribute('aria-hidden', 'true');

    button.appendChild(icon);

    const span = document.createElement('span');
    span.setAttribute('class', 'visually-hidden');
    span.innerHTML = 'Next';

    button.appendChild(span);

    return button;
}

export function createSlideshow(person) {
    const carousel = document.createElement('div');
    carousel.setAttribute('id', getSlideShowId(person));
    carousel.setAttribute('class', 'carousel carousel-dark slide');
    carousel.setAttribute('data-interval', 'false');

    carousel.appendChild(createInner(person));
    carousel.appendChild(createPrevButton(person));
    carousel.appendChild(createNextButton(person));

    return carousel;
}
