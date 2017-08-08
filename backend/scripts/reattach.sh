#!/bin/bash
shellName=server-shell-$( (node -p "require('./config.js').projectName") 2>&1)
screen -r $shellNamescreen -r