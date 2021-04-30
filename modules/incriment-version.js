const fs = require('fs');                                 // work with the file system
var package = require('../package.json');
var newVersion = require('version-incrementer').increment(package.version);
var updated = JSON.stringify({...package, version: newVersion}, null, 2);

fs.writeFile('package.json', updated, e => {
  if (e) throw e;
  console.log(newVersion);
});
