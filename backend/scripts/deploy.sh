#!/bin/bash
projectName=$( (node -p "require('./config.js').projectName") 2>&1)
deploySSHPath=$( (node -p "require('./config.js').deploySSHPath") 2>&1)
sshCertificate=$( (node -p "require('./config.js').sshCertificate") 2>&1)

echo "Deploying to ${projectName} on ${deploySSHPath}";
ssh ${sshCertificate} ${deploySSHPath} "cd ${projectName}/backend && scripts/update.sh";
