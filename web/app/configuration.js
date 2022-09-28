const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');
const fs = require('fs');
const yaml = require('js-yaml');

const argv = yargs(hideBin(process.argv)).argv;
let configuration = {};

try {
  const filename = argv.c;
  const file = fs.readFileSync(filename, {encoding: 'utf8'});
  configuration = yaml.load(file);
} catch (e) {
  console.log(e);
}

module.exports = configuration;
