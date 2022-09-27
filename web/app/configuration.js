const args = require('args-parser')(process.argv)
const fs = require('fs')
const yaml = require('js-yaml')

let configuration = {};

try {
  const filename = args['c'] ?? args['configuration_file'];
  const file = fs.readFileSync(filename, {encoding: 'utf8'});
  configuration = yaml.load(file);
} catch (e) {
  console.log(e);
}

module.exports = configuration;
