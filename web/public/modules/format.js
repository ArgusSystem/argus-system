export function timestampToString(timestamp) {
    return new Date(timestamp).toLocaleString();
}

function formatIntTwoDigits(number) {
    return number.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false})
}

export function daytimeToString(daytime) {
    const hours = Math.floor(daytime / 3600);
    daytime -= hours * 3600;

    const minutes = Math.floor(daytime / 60);
    const seconds = daytime - minutes * 60;

    return `${formatIntTwoDigits(hours)}:${formatIntTwoDigits(minutes)}:${formatIntTwoDigits(seconds)}`;
}