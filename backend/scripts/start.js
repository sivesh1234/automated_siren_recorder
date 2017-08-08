"use strict";

const cp = require('child_process');
const config = require('../config.js');

console.log(cp.execSync(`screen -dmS server-shell-${config.projectName} ` +
    `bash -c 'supervisor app.js'`, { encoding: 'utf8' }));