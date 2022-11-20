const database = require('./database');


async function fetchCameraIds() {
    const res = await database.query('SELECT alias FROM camera;');
    return res.rows.map(row => row.alias);
}

module.exports = fetchCameraIds;