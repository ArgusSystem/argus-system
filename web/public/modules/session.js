const KEY = 'username';

export function signIn(username) {
    localStorage.setItem(KEY, username);
}

export function getUsername() {
    return localStorage.getItem(KEY);
}

export function isSignedIn() {
    return getUsername() !== null;
}

export function signOut() {
    localStorage.removeItem(KEY);
}

