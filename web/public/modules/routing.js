export function redirect(relativeUrl) {
   window.location.href = `/${relativeUrl}`;
}

export function redirectToTab(tab) {
    redirect(tab.page);
}

export function redirectToIndex() {
    redirect('');
}
