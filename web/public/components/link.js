export function createLink(text, href, klass, isActive) {
    const link = document.createElement('a');

    link.innerText = text;
    link.setAttribute('class', klass);
    link.setAttribute('href', href);

    if (isActive){
        link.setAttribute('aria-current', 'page');
        link.classList.add('active');
    }

    return link;
}