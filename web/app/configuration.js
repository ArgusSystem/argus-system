const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');
const fs = require('fs');
const yaml = require('js-yaml');

const argv = yargs(hideBin(process.argv)).argv;

const filename = argv['c'];
const file = fs.readFileSync(filename, {encoding: 'utf8'});

module.exports = yaml.load(file);
