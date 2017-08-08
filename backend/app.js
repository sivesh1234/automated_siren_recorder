"use strict";

const app = require("./server");
const IS_DEV = process.env.IS_DEV || process.env.NODE_ENV === "development";

if (IS_DEV) {
    app().listen(8080);
    console.log("app started in dev mode - listening on port 8080");
} else {
    app().listen(80);
    console.log("app started - listening on port 80");
}