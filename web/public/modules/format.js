export function timestampToString(timestamp) {
    return new Date(timestamp).toLocaleString();
}

export function timestampToISOString(timestamp) {
    return new Date(timestamp).toISOString().slice(0,16);
}

function formatIntTwoDigits(number) {
    return number.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false})
}

export function daytimeToString(daytime) {
    const hours = Math.floor(daytime / 3600);
    daytime -= hours * 3600;

    const minutes = Math.floor(daytime / 60);

    return `${formatIntTwoDigits(hours)}:${formatIntTwoDigits(minutes)}`;
}