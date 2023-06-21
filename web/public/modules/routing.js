export function redirect(relativeUrl, parameters = {}) {
    const queryString = new URLSearchParams(parameters).toString();
    window.location.href = `/${relativeUrl}?${queryString}`;
}

export function redirectToTab(tab) {
    redirect(tab.page);
}

export function redirectToIndex() {
    redirect('');
}

export function reload() {
    window.location.reload();
}
