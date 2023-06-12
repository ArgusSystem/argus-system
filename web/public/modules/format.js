export function timestampToString(timestamp) {
    return new Date(timestamp).toLocaleString();
}

export function daytimeToString(daytime) {
    const hours = Math.floor(daytime / 3600);
    daytime -= hours;

    const minutes = Math.floor(daytime / 60);
    const seconds = daytime - minutes;

    return `${hours}:${minutes}:${seconds}`;
}