"use strict";
const IS_DEV = process.env.IS_DEV || process.env.NODE_ENV === "development";
const log = require("loglevel");

module.exports = {
    gcp: {
        projectId: 'small-vivacity-projects',
        topic: 'atomicity-messages',
        subscription: 'atomicity-message-processing',
        processId: 'atomicity-messages',
        bucket: 'atomicity',
        keyFilename: './secrets/Small-Vivacity-Projects-f502d9066757.json',
    },
    redis: {
        host: IS_DEV ? 'localhost' : '10.132.0.2',
        password: 'kzrVt5DZ'
    },
    loggingLevel: log.levels.INFO,
    /* Times, in seconds, for data retention */
    // Data period to be kept for the API
    windowPeriod: 300,
    // How much of backlog data should be kept in addition to windowPeriod. Means Reddis will
    // store at least windowPeriod + backlogPeriod in total
    backlogPeriod: 300,
    // How often should the storage process run
    writeInterval: 600,
    dataProcessInterval: 1,
    projectName: 'atomicity',
    deploySSHPath: 'deployment@35.187.59.56.com'
};