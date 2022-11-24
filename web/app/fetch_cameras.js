const database = require('./database');


async function fetchCameras() {
    const res = await database.query('SELECT alias, framerate FROM camera;');

    return res.rows.reduce((accumulator, row) => {
        accumulator[row.alias] = row.framerate;
        return accumulator;
    }, {});
}

module.exports = fetchCameras();