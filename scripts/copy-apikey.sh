#!/bin/bash
echo "Copying IBM Cloud apikey into development environment..."
docker cp ~/.bluemix/apikey.json customers:/home/vscode 
docker exec customers sudo chown vscode:vscode /home/vscode/apikey.json
echo "Complete"
