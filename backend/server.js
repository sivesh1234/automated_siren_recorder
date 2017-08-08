"use strict";

const express = require("express");
const Elasticity = require("elasticity");
const config = require('./config');
const moment = require('moment');

function messageProcess({
    raw,
    processed
}) {
    try {
        if (processed && raw) {
            return {
                value: 'processed',
                time: moment().utc().unix(),
                firstRawTime: raw[0].time,
                lastProcessedTime: processed.time
            };
        } else if (raw){
            return {
                value: 'processed',
                time: moment().utc().unix(),
                firstRawTime: raw[0].time,
                lastProcessedTime: 'none'
            };
        } else if (processed) {
            return {
                value: 'processed',
                time: moment().utc().unix(),
                firstRawTime: 'none',
                lastProcessedTime: processed.time
            };
        } else {
            return {
                value: 'processed',
                time: moment().utc().unix(),
                firstRawTime: 'none',
                lastProcessedTime: 'none'
            };
        }
    } catch (err) {
        console.log(err);
    }
}


module.exports = function() {

    const elasticity = Elasticity.start(config, messageProcess);
    const app = express();

    app.get('/raw', function (req, res) {
        elasticity.getCurrent().getRaw().then(raw => {
            res.send(raw);
        });
    });

    app.get('/processed', function (req, res) {
        elasticity.getCurrent().getProcessed().then(processed => {
            res.send(processed);
        });
    });

    return app;
};