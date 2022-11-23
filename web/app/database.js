const { Client } = require('pg');
const configuration = require('./configuration');

const client = new Client(configuration.database.url);
client.connect();

module.exports = client;