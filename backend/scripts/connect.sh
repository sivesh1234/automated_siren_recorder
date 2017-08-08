#!/bin/bash
deploySSHPath=$( (node -p "require('./config.js').deploySSHPath") 2>&1)
sshCertificate=$( (node -p "require('./config.js').sshCertificate") 2>&1)

ssh ${sshCertificate} ${deploySSHPath}