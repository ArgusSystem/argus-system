const USERNAME = 'username';
const ALIAS = 'alias';

export function signIn(username, alias) {
    localStorage.setItem(USERNAME, username);
    localStorage.setItem(ALIAS, alias)
}

export function getUsername() {
    return localStorage.getItem(USERNAME);
}

export function getAlias() {
    return localStorage.getItem(ALIAS);
}

export function isSignedIn() {
    return getUsername() !== null;
}

export function signOut() {
    localStorage.removeItem(USERNAME);
    localStorage.removeItem(ALIAS)
}

